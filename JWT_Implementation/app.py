from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from dotenv import load_dotenv
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from functools import wraps
import os
import base64
import sqlalchemy

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 30)))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Store encryption keys temporarily
encryption_keys = {}

def custom_jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            encrypted_token = request.cookies.get('access_token_cookie')
            if not encrypted_token:
                flash('Please log in to access this page')
                return redirect(url_for('login'))

            username = session.get('username')
            if not username:
                flash('Session expired. Please log in again')
                return redirect(url_for('login'))

            encryption_key = encryption_keys.get(username)
            if not encryption_key:
                flash('Session expired. Please log in again')
                return redirect(url_for('login'))

            # Decrypt the token
            decrypted_token = decrypt_token(encrypted_token, encryption_key)
            if not decrypted_token:
                flash('Invalid token. Please log in again')
                return redirect(url_for('login'))

            # Store the decrypted token in request context
            request.headers._list.append(('Authorization', f'Bearer {decrypted_token}'))
            
            # Verify JWT token
            verify_jwt_in_request()
            
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            flash('Authentication failed. Please log in again')
            return redirect(url_for('login'))
    return decorated_function

# User Model with added public key field
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    public_key = db.Column(db.String(500), nullable=True)  # Make it nullable

    def __repr__(self):
        return f'<User {self.username}>'

# Generate server's ECDH key pair
server_private_key = ec.generate_private_key(ec.SECP256R1())
server_public_key = server_private_key.public_key()

# Initialize database
def init_db():
    with app.app_context():
        # Drop all tables if they exist
        db.drop_all()
        # Create all tables
        db.create_all()
        print("Database initialized successfully!")

# Initialize the database
init_db()

def derive_key(shared_key):
    """Derive a key using HKDF"""
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b'handshake data',
    )
    return hkdf.derive(shared_key)

def encrypt_token(token, key):
    """Encrypt token using ChaCha20-Poly1305"""
    chacha = ChaCha20Poly1305(key)
    nonce = os.urandom(12)
    ciphertext = chacha.encrypt(nonce, token.encode(), None)
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def decrypt_token(encrypted_token, key):
    """Decrypt token using ChaCha20-Poly1305"""
    try:
        data = base64.b64decode(encrypted_token.encode('utf-8'))
        nonce = data[:12]
        ciphertext = data[12:]
        chacha = ChaCha20Poly1305(key)
        return chacha.decrypt(nonce, ciphertext, None).decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        return None

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('signup'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        client_public_key = request.form.get('public_key')

        # Debug logging
        print("\nLogin attempt details:")
        print(f"Username provided: {bool(username)}")
        print(f"Password provided: {bool(password)}")
        print(f"Public key provided: {bool(client_public_key)}")
        if client_public_key:
            print(f"Public key length: {len(client_public_key)}")
            print(f"Public key preview: {client_public_key[:20]}...")

        # Validate all required fields
        missing_fields = []
        if not username:
            missing_fields.append("Username")
        if not password:
            missing_fields.append("Password")
        if not client_public_key:
            missing_fields.append("Security key")

        if missing_fields:
            error_message = f"Missing required fields: {', '.join(missing_fields)}"
            print(f"Validation error: {error_message}")
            flash(error_message)
            return redirect(url_for('login'))

        # Proceed with authentication
        try:
            user = User.query.filter_by(username=username).first()
            if not user or not check_password_hash(user.password, password):
                print("Authentication failed: Invalid credentials")
                flash('Invalid username or password')
                return redirect(url_for('login'))

            # Process client's public key
            try:
                # Convert client's public key from base64 to bytes
                client_public_key_bytes = base64.b64decode(client_public_key)
                print(f"Successfully decoded public key, length: {len(client_public_key_bytes)} bytes")
                
                # Load client's public key
                client_public_key_obj = ec.EllipticCurvePublicKey.from_encoded_point(
                    ec.SECP256R1(),
                    client_public_key_bytes
                )
                
                # Generate shared key
                shared_key = server_private_key.exchange(
                    ec.ECDH(),
                    client_public_key_obj
                )
                
                # Derive encryption key
                encryption_key = HKDF(
                    algorithm=hashes.SHA256(),
                    length=32,
                    salt=None,
                    info=b'handshake data',
                ).derive(shared_key)
                
                # Store encryption key
                encryption_keys[username] = encryption_key
                print("Key exchange successful")
                
                # Create and encrypt access token
                access_token = create_access_token(identity=username)
                encrypted_token = encrypt_token(access_token, encryption_key)
                
                # Store username in session
                session['username'] = username
                
                response = make_response(redirect(url_for('dashboard')))
                response.set_cookie('access_token_cookie', encrypted_token, httponly=True)
                print("Login successful, redirecting to dashboard")
                return response
                
            except Exception as e:
                print(f"Key exchange error: {str(e)}")
                flash('Error during security handshake. Please try again.')
                return redirect(url_for('login'))

        except Exception as e:
            print(f"Login error: {str(e)}")
            flash('An error occurred during login. Please try again.')
            return redirect(url_for('login'))

    # Handle GET request
    try:
        # Export server's public key
        server_public_bytes = server_public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )
        server_public_key_b64 = base64.b64encode(server_public_bytes).decode('utf-8')
        print(f"\nServing login page with server public key (preview): {server_public_key_b64[:20]}...")
        return render_template('login.html', server_public_key=server_public_key_b64)
    except Exception as e:
        print(f"Error preparing login page: {str(e)}")
        flash('Error initializing security. Please refresh the page.')
        return redirect(url_for('login'))

@app.route('/dashboard')
@custom_jwt_required
def dashboard():
    current_user = get_jwt_identity()
    return render_template('dashboard.html', username=current_user)

@app.route('/verify_token')
def verify_token():
    token = request.args.get('token')
    if not token:
        return jsonify({"valid": False}), 401
    try:
        verify_jwt_in_request()
        return jsonify({"valid": True}), 200
    except:
        return jsonify({"valid": False}), 401

@app.route('/logout')
def logout():
    username = session.get('username')
    if username:
        # Clear encryption key
        encryption_keys.pop(username, None)
        session.pop('username', None)
    
    response = make_response(redirect(url_for('login')))
    response.delete_cookie('access_token_cookie')
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5225, host='0.0.0.0') 