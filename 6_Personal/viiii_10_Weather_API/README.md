# Weather API Flask Application

A modern, responsive weather application built with Flask that provides real-time weather information using the WeatherAPI.com service. The application features user authentication and a beautiful, gradient-based UI design.

## 🌟 Features

- **User Authentication**: Secure login system with session management
- **Real-time Weather Data**: Current weather conditions from WeatherAPI.com
- **Responsive Design**: Modern glass-morphism UI that works on all devices
- **Comprehensive Weather Info**: Temperature, humidity, wind, pressure, UV index, and more
- **Search Functionality**: Search by city name, zip code, or coordinates
- **Error Handling**: Graceful error handling for invalid cities or API issues

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **API**: WeatherAPI.com
- **Styling**: Custom CSS with backdrop-filter effects
- **Authentication**: Flask sessions

## 📋 Prerequisites

- Python 3.7+
- Flask
- Requests library
- WeatherAPI.com account and API key

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
git clone <repository-url>
cd viiii_10_Weather_API
```

### 2. Install Dependencies

```bash
pip install flask requests
```

### 3. WeatherAPI.com Setup

This project uses **WeatherAPI.com** for weather data. The API credentials are already configured:

- **Website**: https://www.weatherapi.com/
- **Email**: sadiba9440@nrlord.com
- **Password**: Test@123

The API key is already included in the code: `f6e90512cb514514a82150007252110`

### 4. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🔐 Login Credentials

The application has built-in demo users:

| Username | Password |
|----------|----------|
| admin    | weather123 |
| user     | weather123 |

## 📁 Project Structure

```
viiii_10_Weather_API/
├── app.py                 # Main Flask application
├── templates/
│   ├── base.html         # Base template with shared styles
│   ├── login.html        # Login page
│   └── home.html         # Main weather dashboard
└── README.md             # Project documentation
```

## 🔧 Code Overview

### Main Application (app.py)

```python
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# WeatherAPI.com configuration
WEATHER_API_KEY = 'f6e90512cb514514a82150007252110'
WEATHER_API_BASE = 'http://api.weatherapi.com/v1'

# Simple user database
USERS = {
    'admin': 'weather123',
    'user': 'weather123'
}
```

### Authentication Decorator

```python
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function
```

### Weather API Endpoint

```python
@app.route('/api/weather')
@login_required
def get_weather():
    city = request.args.get('city', '')
    
    if not city:
        return jsonify({'error': 'City name is required'}), 400
    
    try:
        url = f'{WEATHER_API_BASE}/current.json'
        params = {
            'key': WEATHER_API_KEY,
            'q': city,
            'aqi': 'yes'
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
                'humidity': data['current']['humidity'],
                'pressure': data['current']['pressure_mb'],
                'description': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon'],
                'wind_speed': data['current']['wind_kph'],
                'wind_dir': data['current']['wind_dir'],
                'uv': data['current']['uv'],
                # ... more weather data
            })
    except Exception as e:
        return jsonify({'error': 'Failed to fetch weather data'}), 500
```

### Frontend JavaScript

```javascript
async function searchWeather() {
    const city = cityInput.value.trim();
    
    if (!city) {
        showError('Please enter a city name');
        return;
    }

    try {
        const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
        const data = await response.json();

        if (response.ok) {
            displayWeather(data);
        } else {
            showError(data.error || 'Failed to fetch weather data');
        }
    } catch (err) {
        showError('Network error. Please try again.');
    }
}
```

## 🎨 UI Features

### Glass Morphism Design

The application uses modern CSS with backdrop-filter effects:

```css
.login-box {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
```

### Gradient Background

```css
body {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
    color: #fff;
}
```

### Responsive Grid Layout

```css
.weather-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
}
```

## 📡 API Endpoints

| Endpoint | Method | Description | Authentication |
|----------|--------|-------------|----------------|
| `/` | GET | Redirect to login or home | No |
| `/login` | GET/POST | User login page | No |
| `/logout` | GET | User logout | No |
| `/home` | GET | Weather dashboard | Required |
| `/api/weather` | GET | Get weather data | Required |

### Weather API Response Example

```json
{
    "city": "London",
    "region": "City of London, Greater London",
    "country": "United Kingdom",
    "temp": 15,
    "temp_f": 59,
    "feels_like": 14,
    "feels_like_f": 57,
    "humidity": 72,
    "pressure": 1013,
    "description": "Partly cloudy",
    "icon": "//cdn.weatherapi.com/weather/64x64/day/116.png",
    "wind_speed": 13,
    "wind_mph": 8,
    "wind_dir": "WSW",
    "cloud": 75,
    "uv": 4,
    "vis_km": 10,
    "last_updated": "2025-10-21 14:30",
    "localtime": "2025-10-21 14:32"
}
```

## 🔧 Configuration

### Environment Variables (Optional)

You can optionally use environment variables:

```python
import os

app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')
WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY', 'f6e90512cb514514a82150007252110')
```

### Security Considerations

For production deployment:

1. Change the secret key
2. Use environment variables for API keys
3. Implement proper user management
4. Add HTTPS
5. Use a proper database instead of in-memory user storage

## 🚀 Deployment

### Local Development

```bash
# Set Flask environment
set FLASK_ENV=development  # Windows
export FLASK_ENV=development  # Linux/Mac

# Run the application
python app.py
```

### Production Deployment

```bash
# Install production WSGI server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🎯 Usage Examples

### Search by City Name
```
London
New York
Tokyo
```

### Search by Coordinates
```
40.7128,-74.0060  # New York
51.5074,-0.1278   # London
```

### Search by Zip Code
```
10001  # New York
SW1A   # London
```

## 🛠️ Customization

### Adding New Weather Parameters

To add new weather data points, modify the weather API endpoint:

```python
return jsonify({
    'city': data['location']['name'],
    # ... existing fields
    'air_quality': data.get('current', {}).get('air_quality', {}),
    'moon_phase': data.get('astronomy', {}).get('astro', {}).get('moon_phase', ''),
    # Add more fields as needed
})
```

### Styling Customization

Modify the CSS in `base.html` and individual templates to change:
- Color schemes
- Layout structure  
- Animation effects
- Responsive breakpoints

## 🐛 Troubleshooting

### Common Issues

1. **API Key Issues**: Ensure the WeatherAPI.com account is active
2. **City Not Found**: Check spelling and try different formats
3. **Session Issues**: Clear browser cookies and restart the application
4. **Import Errors**: Ensure all required packages are installed

### Debug Mode

Enable debug mode for development:

```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

## 📄 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

1. Fork the project
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

**WeatherAPI.com Credentials:**
- Website: https://www.weatherapi.com/
- Email: sadiba9440@nrlord.com  
- Password: Test@123

**Demo Login:**
- Username: admin or user
- Password: weather123