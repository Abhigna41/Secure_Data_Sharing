# Secure Data Sharing System - Web Application

A Flask-based web application for secure data sharing using Attribute-Based Encryption (ABE).

## 🚀 Quick Start

### Option 1: Complete Setup & Run
```bat
run_complete_fixed.bat
```

### Option 2: Direct Run
```bat
run_fixed.bat
```

### Option 3: Manual Run
```bash
python app_simple.py
```

Then visit: **http://localhost:5000**

## 📁 Essential Files

### Core Application
- `app_simple.py` - Main Flask web application
- `abe_crypto.py` - Attribute-Based Encryption implementation
- `firebase_utils.py` - Firebase integration utilities
- `config.py` - Configuration settings

### Configuration
- `firebase_service_account.json` - Firebase credentials
- `master_key.pem` - Master encryption key
- `requirements.txt` - Python dependencies

### Templates
- `templates/` - HTML templates for web interface
  - `base.html` - Base template
  - `dashboard.html` - Main dashboard
  - `login_simple.html` - Simple login page
  - `encrypt.html` - Message encryption
  - `decrypt.html` - Message decryption
  - `file_encrypt.html` - File encryption
  - `file_decrypt.html` - File decryption
  - `manage_users.html` - User management
  - `activity_log.html` - Activity logging
  - `encrypt_result.html` - Encryption results
  - `decrypt_result.html` - Decryption results

### Runtime Directories
- `uploads/` - Temporary file uploads
- `downloads/` - Decrypted file downloads
- `venv/` - Python virtual environment

### Batch Files
- `run_complete_fixed.bat` - Complete setup and run
- `run_fixed.bat` - Simple run

## 🔧 Features

### ✅ Web Interface
- **Simple Login**: No password required, just enter any username
- **Message Encryption/Decryption**: Secure text message handling
- **File Encryption/Decryption**: Upload and encrypt files
- **User Management**: Create users with specific attributes
- **Activity Logging**: Track all system operations
- **Auto-Registration**: Users automatically registered with proper credentials

### ✅ Security Features
- **Attribute-Based Encryption**: Policy-based access control
- **Firebase Integration**: Secure cloud storage
- **Master Key Management**: RSA key-based security
- **Access Control**: User attribute verification

### ✅ User Experience
- **Modern Web UI**: Bootstrap-based responsive design
- **No Complex Setup**: Auto-login and user registration
- **Clear Error Handling**: Informative error messages
- **Quick Actions**: Preset user creation buttons

## 🎯 How to Use

1. **Start the Application**: Run `run_complete_fixed.bat`
2. **Access Web Interface**: Open http://localhost:5000
3. **Simple Login**: Enter any username (e.g., "alice", "testuser")
4. **Encrypt Data**: Go to "Encrypt Data" → Enter message → Get Data ID
5. **Decrypt Data**: Go to "Decrypt Data" → Enter Data ID → View decrypted message
6. **Manage Users**: Go to "User Management" → Create users with attributes
7. **File Operations**: Upload and encrypt files, then decrypt and download

## 🛠️ Technical Details

- **Framework**: Flask (Python web framework)
- **Encryption**: Attribute-Based Encryption with RSA/AES
- **Database**: Firebase Firestore
- **Frontend**: Bootstrap 5 + Custom CSS
- **Authentication**: Simplified (no passwords required)

## 📝 Notes

- **Development Mode**: Debug mode enabled for development
- **Auto-Registration**: Users automatically get proper encryption credentials
- **File Size Limit**: 16MB maximum file size
- **Session Management**: Web sessions maintain user state
- **Error Logging**: All operations logged for debugging

## 🔄 Recent Fixes

- ✅ Fixed decryption "User not found" errors
- ✅ Improved user management interface
- ✅ Enhanced auto-registration system
- ✅ Better error handling and debugging
- ✅ Simplified login process
- ✅ **Cleaned up codebase and removed ALL unused files**

---

**Ready to use! Clean, minimal, and fully functional.**
