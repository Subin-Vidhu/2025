# 🏦 Bank Loan Interest Calculator

A comprehensive loan calculator application with both web interface and command-line functionality. Calculate loan payments, interest amounts, and detailed amortization schedules. Runs as a Windows service for 24/7 availability.

## 📋 Overview

This dual-mode loan calculator provides:
- **Web Interface**: Modern, responsive HTML interface with real-time calculations
- **Command Line Tool**: Python script for direct calculations
- **Multiple Repayment Options**: Same payments, different payments, or no payments until end
- **Detailed Amortization**: Month-by-month payment breakdown
- **Windows Service**: Automatic startup and background operation
- **Network Access**: Accessible from any device on your network

## 🚀 Features

### Calculation Modes
1. **Same Amount Payments**: Fixed monthly payments throughout loan term
2. **Different Amount Payments**: Customize each month's payment individually  
3. **No Payments Until End**: Simple interest calculation with lump sum at end

### Key Capabilities
- Calculate monthly loan payments and interest
- Generate detailed amortization schedules
- Handle variable payment amounts
- Support for different loan terms and interest rates
- Real-time web calculations with interactive interface
- Mobile-responsive design for any device
- Automatic Windows service integration

### Technical Features
- **Dual Interface**: Web UI + Command line
- **HTTP Server**: Python built-in server
- **Service Management**: NSSM for Windows service integration
- **Cross-Platform Access**: Works on any device with web browser
- **Automatic Startup**: Starts with Windows boot
- **Virtual Environment**: Isolated Python environment

## 📁 Project Structure

```
viiii_9_Bank_loan_Interest/
├── main.py              # Python command-line calculator
├── main.html            # Web interface with JavaScript calculations
├── start_server.bat     # Batch script to start HTTP server
└── Readme.md           # This documentation file
```

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.6+** installed on your system
- **Virtual Environment** at `D:\2025\venv\` (or modify paths in batch file)
- **NSSM (Non-Sucking Service Manager)** for Windows service management
- **Administrator privileges** for service installation

### Step 1: Download NSSM
1. Download NSSM from: https://nssm.cc/download
2. Extract to `C:\Program Files\nssm-2.24\` (or your preferred location)
3. Add NSSM to your system PATH or navigate to the directory

### Step 2: Set Up Python Environment
```cmd
# Create virtual environment (if not exists)
python -m venv D:\2025\venv

# Activate virtual environment
D:\2025\venv\Scripts\activate

# No additional packages needed - uses built-in modules
```

### Step 3: Test the Applications

#### Test Command Line Version
```cmd
cd D:\2025\6_Personal\viiii_9_Bank_loan_Interest
python main.py
```

#### Test Web Server
```cmd
# Run the batch file manually
start_server.bat

# Or start server directly
python -m http.server 8080 --bind 0.0.0.0

# Access via browser: http://localhost:8080/main.html
```

### Step 4: Install as Windows Service
```cmd
# Open Command Prompt as Administrator
cd "C:\Program Files\nssm-2.24\win64"

# Install the service
nssm install LoanCalculator "C:\Windows\System32\cmd.exe" "/c D:\2025\6_Personal\viiii_9_Bank_loan_Interest\start_server.bat"

# Start the service
nssm start LoanCalculator
```

## 🔧 Service Management Commands

### Basic Service Operations
```cmd
# Start the service
nssm start LoanCalculator

# Stop the service
nssm stop LoanCalculator

# Restart the service
nssm restart LoanCalculator

# Check service status
nssm status LoanCalculator
```

### Service Configuration
```cmd
# Edit service configuration
nssm edit LoanCalculator

# Remove the service (if needed)
nssm remove LoanCalculator confirm

# Reinstall with different settings
nssm remove LoanCalculator confirm
nssm install LoanCalculator "C:\Windows\System32\cmd.exe" "/c D:\2025\6_Personal\viiii_9_Bank_loan_Interest\start_server.bat"
```

### Windows Service Manager
```cmd
# Open Services management console
services.msc

# Look for "LoanCalculator" service to manage via GUI
```

## 🌐 Usage Instructions

### Web Interface Access
1. **Local Access**: `http://localhost:8080/main.html`
2. **Network Access**: `http://YOUR_IP_ADDRESS:8080/main.html` from other devices
3. **Service Status**: Verify service is running in Task Manager or services.msc

### Using the Web Calculator
1. **Enter Loan Details**:
   - Principal loan amount (₹)
   - Annual interest rate (%)
   - Loan duration (months)

2. **Select Repayment Type**:
   - **Same Amount**: Enter fixed monthly payment
   - **Different Amounts**: Enter custom amount for each month
   - **No Payments**: Calculate lump sum payment at end

3. **View Results**:
   - Summary cards with key totals
   - Detailed month-by-month schedule
   - Total interest calculations

### Command Line Usage
```cmd
python main.py

# Follow prompts:
# - Enter principal loan amount
# - Enter annual interest rate (in %)
# - Enter number of months
# - Choose repayment type (S/D/N)
# - Enter payment amounts as requested
```

## 🔧 Configuration Options

### Modify Server Settings
Edit `start_server.bat` to change:
```batch
# Change port (default: 8080)
python -m http.server 9000 --bind 0.0.0.0

# Change binding (localhost only)
python -m http.server 8080 --bind 127.0.0.1

# Change virtual environment path
set VENV_PATH=D:\your\custom\venv\Scripts
```

### Service Configuration
```cmd
# Set custom display name
nssm set LoanCalculator DisplayName "Bank Loan Calculator Service"

# Set description
nssm set LoanCalculator Description "Web-based loan calculator with amortization schedules"

# Set startup type
nssm set LoanCalculator Start SERVICE_AUTO_START
```

## 🔍 Troubleshooting

### Common Issues

**Service Won't Start**
```cmd
# Check Python and virtual environment
D:\2025\venv\Scripts\python.exe --version

# Test batch file manually
D:\2025\6_Personal\viiii_9_Bank_loan_Interest\start_server.bat

# Check Windows Event Viewer for errors
eventvwr.msc
```

**Port Already in Use**
```cmd
# Find process using port 8080
netstat -ano | findstr :8080

# Kill the process if needed
taskkill /PID <process_id> /F

# Or change port in start_server.bat
```

**Web Interface Not Loading**
```cmd
# Verify server is running
curl http://localhost:8080

# Check if main.html exists
dir D:\2025\6_Personal\viiii_9_Bank_loan_Interest\main.html

# Test direct file access
http://localhost:8080/main.html
```

**Virtual Environment Issues**
```cmd
# Recreate virtual environment
rmdir /s D:\2025\venv
python -m venv D:\2025\venv

# Update batch file paths if needed
```

### Log Files & Debugging
- **Windows Event Log**: Check Application and System logs
- **Command Prompt**: Run batch file manually to see errors
- **Browser Console**: F12 Developer Tools for JavaScript errors
- **Network Tab**: Check for failed resource loads

## 📊 Technical Details

### File Descriptions
- **`main.py`**: Command-line loan calculator with amortization schedule generation
- **`main.html`**: Complete web application with JavaScript calculations and responsive design
- **`start_server.bat`**: Batch wrapper that activates virtual environment and starts HTTP server
- **`Readme.md`**: Comprehensive documentation and setup instructions

### Calculation Logic
Both interfaces use the same core calculation:
- **Monthly Interest Rate**: Annual rate ÷ 12
- **Monthly Interest**: Opening balance × Monthly rate
- **Total Due**: Opening balance + Monthly interest
- **Closing Balance**: Total due - Payment amount
- **Early Payoff**: Handled when payment ≥ total due

### Network Configuration
- **Default Port**: 8080
- **Binding**: 0.0.0.0 (all interfaces)
- **Protocol**: HTTP (upgrade to HTTPS for production)
- **Access**: LAN-accessible by default

## 🔒 Security Considerations

### Network Security
- **Firewall**: Configure Windows Firewall for port 8080
- **Access Control**: Consider restricting to specific IP ranges
- **HTTPS**: Implement SSL/TLS for sensitive financial data
- **Authentication**: Add login system for multi-user environments

### Service Security
- **Privileges**: Service runs with system privileges by default
- **Dedicated Account**: Consider creating service-specific user account
- **File Permissions**: Restrict access to application directory
- **Updates**: Keep Python and dependencies current

### Data Security
- **No Data Storage**: Calculator doesn't store loan information
- **Session Privacy**: Each calculation is independent
- **Network Traffic**: Consider VPN for remote access
- **Audit Trail**: Add logging for calculation history if needed

## 🚀 Advanced Configuration

### Custom Port & Binding
```batch
# In start_server.bat, modify:
python -m http.server 9090 --bind 192.168.1.100
```

### Service Startup Options
```cmd
# Automatic startup (default)
nssm set LoanCalculator Start SERVICE_AUTO_START

# Manual startup only
nssm set LoanCalculator Start SERVICE_DEMAND_START

# Delayed automatic startup
nssm set LoanCalculator Start SERVICE_AUTO_START
nssm set LoanCalculator DelayedAutoStart 1
```

### Environment Variables
```cmd
# Set environment variables for service
nssm set LoanCalculator AppEnvironmentExtra PYTHON_ENV=production PORT=8080
```

### Resource Limits
```cmd
# Set memory limits (optional)
nssm set LoanCalculator AppPriority NORMAL_PRIORITY_CLASS
```

## 📈 Monitoring & Maintenance

### Performance Monitoring
- **Task Manager**: Monitor CPU and memory usage
- **Resource Monitor**: Detailed system resource analysis
- **Network Usage**: Check connections and bandwidth
- **Browser Performance**: F12 Developer Tools for web performance

### Regular Maintenance
- **Service Health**: Check service status weekly
- **Log Cleanup**: Clear Windows Event logs periodically
- **Security Updates**: Update Python and Windows regularly
- **Backup**: Save application directory and service configuration
- **Testing**: Verify calculations with known loan examples

### Health Checks
```cmd
# Quick service status
sc query LoanCalculator

# Test web access
curl -I http://localhost:8080/main.html

# Check listening ports
netstat -an | findstr :8080
```

## 🤝 Support & Development

### Making Changes

#### Modify Calculations
1. **Web Version**: Edit JavaScript in `main.html`
2. **Command Line**: Modify `main.py`
3. **Test Changes**: Run both versions manually
4. **Restart Service**: `nssm restart LoanCalculator`

#### UI Improvements
1. **Edit CSS/HTML**: Update `main.html`
2. **Test in Browser**: Refresh page to see changes
3. **Mobile Testing**: Use browser developer tools
4. **Cross-browser**: Test in Edge, Chrome, Firefox

#### Server Configuration
1. **Stop Service**: `nssm stop LoanCalculator`
2. **Edit Batch File**: Modify `start_server.bat`
3. **Test Manually**: Run batch file to verify
4. **Start Service**: `nssm start LoanCalculator`

### Adding Features
- **New Calculation Types**: Add to both main.py and main.html
- **Data Export**: Add CSV/PDF export functionality
- **User Accounts**: Implement authentication system
- **Database Storage**: Add loan history and user profiles
- **API Endpoints**: Create REST API for mobile apps

### Backup Strategy
```cmd
# Backup entire application
xcopy "D:\2025\6_Personal\viiii_9_Bank_loan_Interest" "D:\Backups\LoanCalculator_%DATE%" /E /I

# Export service configuration  
nssm dump LoanCalculator > "D:\Backups\LoanCalculator_service_%DATE%.txt"

# Backup virtual environment (optional)
xcopy "D:\2025\venv" "D:\Backups\LoanCalculator_venv_%DATE%" /E /I
```

### Development Environment
```cmd
# Clone application for development
xcopy "D:\2025\6_Personal\viiii_9_Bank_loan_Interest" "D:\Dev\LoanCalculator_Dev" /E /I

# Test development version on different port
python -m http.server 8081 --bind 127.0.0.1

# Access dev version: http://localhost:8081/main.html
```

## 📋 Example Calculations

### Scenario 1: Fixed Monthly Payments
- **Principal**: ₹100,000
- **Annual Rate**: 12%
- **Term**: 24 months
- **Monthly Payment**: ₹5,000

### Scenario 2: Variable Payments
- **Principal**: ₹50,000
- **Annual Rate**: 15%
- **Payments**: ₹3,000 (Month 1-6), ₹5,000 (Month 7-12)

### Scenario 3: Lump Sum Payment
- **Principal**: ₹75,000
- **Annual Rate**: 18%
- **Term**: 12 months
- **Payment**: One-time payment at end

## 📄 License & Usage

This application is designed for personal and educational use. Feel free to modify and adapt for your specific financial calculation needs.

---

**Created**: October 2025 | **Author**: Subin-PC | **Technology**: Python + HTML/JavaScript + Windows Service  
**Category**: Financial Tools | **Version**: 1.0

For questions or issues, check the troubleshooting section or review the Windows Event Log for detailed error information.