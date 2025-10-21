from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Simple user database (password: weather123)
USERS = {
    'admin': 'weather123',
    'user': 'weather123'
}

WEATHER_API_KEY = 'f6e90512cb514514a82150007252110'
WEATHER_API_BASE = 'http://api.weatherapi.com/v1'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html', username=session['username'])

@app.route('/api/weather')
@login_required
def get_weather():
    city = request.args.get('city', '')
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400
    
    try:
        # Using WeatherAPI.com current weather endpoint
        url = f'{WEATHER_API_BASE}/current.json'
        params = {
            'key': WEATHER_API_KEY,
            'q': city,
            'aqi': 'yes'  # Include air quality data
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if response.status_code == 200:
            return jsonify({
                'city': data['location']['name'],
                'region': data['location']['region'],
                'country': data['location']['country'],
                'temp': round(data['current']['temp_c']),
                'temp_f': round(data['current']['temp_f']),
                'feels_like': round(data['current']['feelslike_c']),
                'feels_like_f': round(data['current']['feelslike_f']),
                'humidity': data['current']['humidity'],
                'pressure': data['current']['pressure_mb'],
                'description': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon'],
                'wind_speed': data['current']['wind_kph'],
                'wind_mph': data['current']['wind_mph'],
                'wind_dir': data['current']['wind_dir'],
                'cloud': data['current']['cloud'],
                'uv': data['current']['uv'],
                'vis_km': data['current']['vis_km'],
                'last_updated': data['current']['last_updated'],
                'localtime': data['location']['localtime']
            })
        else:
            error_msg = data.get('error', {}).get('message', 'City not found')
            return jsonify({'error': error_msg}), 404
            
    except Exception as e:
        return jsonify({'error': 'Failed to fetch weather data'}), 500

if __name__ == '__main__':
    app.run(debug=True)