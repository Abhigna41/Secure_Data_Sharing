#!/usr/bin/env python3
"""
Secure Data Sharing System - Web Application
============================================

Flask web application for the Secure Data Sharing System.
Provides web-based interface for attribute-based encryption operations.

Author: Your Name
Date: 2025
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import os
import uuid
import json
from datetime import datetime
import base64
from io import BytesIO
import tempfile

# Import your existing modules
try:
    from abe_crypto import ABECrypto
except ImportError:
    print("Warning: ABE Crypto module not found. Creating mock implementation.")
    class ABECrypto:
        def __init__(self):
            self.data_store = {}
            self.user_store = {}
        
        def issue_ac(self, user_id, attributes):
            self.user_store[user_id] = attributes
            return f"AC_{user_id}_{len(attributes)}_attrs"
        
        def encrypt(self, message, policy):
            data_id = f"DATA_{uuid.uuid4().hex[:8]}"
            self.data_store[data_id] = {'message': message, 'policy': policy}
            return data_id
        
        def decrypt(self, user_id, data_id):
            if data_id not in self.data_store:
                raise Exception("Data not found")
            return self.data_store[data_id]['message']
        
        def revoke_attribute(self, user_id, attribute):
            if user_id in self.user_store:
                attrs = self.user_store[user_id]
                if attribute in attrs:
                    attrs.remove(attribute)
                return f"AC_{user_id}_{len(attrs)}_attrs"
            raise Exception("User not found")

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this!

# Configuration
UPLOAD_FOLDER = 'uploads'
DOWNLOAD_FOLDER = 'downloads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Initialize ABE system
abe = ABECrypto()

# Simple in-memory user store (replace with database in production)
users = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'attributes': ['admin', 'manager', 'read_access', 'write_access'],
        'role': 'admin'
    },
    'user1': {
        'password': generate_password_hash('user123'),
        'attributes': ['user', 'read_access'],
        'role': 'user'
    }
}

# Activity log
activity_log = []

@app.context_processor
def inject_common_vars():
    """Inject common variables into all templates"""
    return {
        'users': users,
        'current_user_id': session.get('user_id', 'guest'),
        'current_user_attributes': session.get('user_attributes', [])
    }

def log_activity(user_id, action, details=""):
    """Log user activity"""
    activity_log.append({
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': user_id,
        'action': action,
        'details': details
    })
    # Keep only last 100 entries
    if len(activity_log) > 100:
        activity_log.pop(0)

@app.route('/')
def index():
    """Home page - redirect to login if not authenticated, otherwise show dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return redirect(url_for('dashboard'))

def ensure_user_registered(user_id, attributes=None):
    """Ensure user has proper Access Credentials in the system"""
    if attributes is None:
        attributes = ['user', 'read_access', 'write_access']
    
    print(f"DEBUG: Checking registration for user '{user_id}' with attributes {attributes}")
    
    try:
        # Try to get user from Firebase - if it fails, they need to be registered
        if hasattr(abe, 'firebase'):
            print(f"DEBUG: Using real ABE with Firebase")
            user_data = abe.firebase.get_user(user_id)
            print(f"DEBUG: User '{user_id}' found in Firebase")
            return True
        else:
            print(f"DEBUG: Using mock ABE implementation")
            # Using mock implementation, check if user exists in mock store
            if hasattr(abe, 'user_store') and user_id in abe.user_store:
                print(f"DEBUG: User '{user_id}' found in mock store")
                return True
            else:
                print(f"DEBUG: User '{user_id}' not found in mock store, will register")
                raise Exception("User not found in mock store")
    except Exception as e:
        print(f"DEBUG: User '{user_id}' not found ({e}), attempting to register...")
        # User not found, issue new Access Credentials
        try:
            ac = abe.issue_ac(user_id, attributes)
            print(f"DEBUG: Successfully issued AC for '{user_id}': {ac}")
            log_activity(user_id, 'auto_register', f'User auto-registered with attributes: {attributes}')
            return True
        except Exception as reg_error:
            print(f"DEBUG: Failed to register user '{user_id}': {reg_error}")
            log_activity(user_id, 'auto_register_failed', str(reg_error))
            return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login with admin credentials"""
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        password = request.form.get('password', '').strip()
        
        # Check if user exists and password is correct
        if user_id in users and check_password_hash(users[user_id]['password'], password):
            session['user_id'] = user_id
            session['user_attributes'] = users[user_id]['attributes']
            session['user_role'] = users[user_id]['role']
            
            # Ensure user is registered in the ABE system
            if ensure_user_registered(user_id, users[user_id]['attributes']):
                log_activity(user_id, 'login', 'User logged in successfully')
                flash(f'Welcome back, {user_id}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Failed to register user in the system. Please try again.', 'error')
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/guest_login', methods=['POST'])
def guest_login():
    """Simple guest login - no credentials required"""
    user_id = 'guest'
    attributes = ['user', 'read_access', 'write_access']
    
    # Ensure user is registered in the ABE system
    if ensure_user_registered(user_id, attributes):
        session['user_id'] = user_id
        session['user_attributes'] = attributes
        session['user_role'] = 'user'
        log_activity(user_id, 'guest_login', 'Guest user logged in')
        flash(f'Welcome, Guest User!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Failed to register guest user in the system. Please try again.', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """User logout"""
    if 'user_id' in session:
        log_activity(session['user_id'], 'logout', 'User logged out')
        session.pop('user_id', None)
        session.pop('user_attributes', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    """Main dashboard"""
    # Auto-login if not logged in
    if 'user_id' not in session:
        user_id = 'user'
        attributes = ['user', 'read_access', 'write_access', 'admin']
        
        # Ensure user is registered before proceeding
        if ensure_user_registered(user_id, attributes):
            session['user_id'] = user_id
            session['user_attributes'] = attributes
        else:
            flash('Unable to register user. Please try logging in.', 'error')
            return redirect(url_for('login'))
    
    return render_template('dashboard.html',
                         user_id=session['user_id'],
                         user_attributes=session.get('user_attributes', []),
                         user_role='user',
                         users=users)

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt_data():
    """Encrypt data/message"""
    # Auto-login if not logged in
    if 'user_id' not in session:
        user_id = 'user'
        attributes = ['user', 'read_access', 'write_access', 'admin']
        
        # Ensure user is registered before proceeding
        if ensure_user_registered(user_id, attributes):
            session['user_id'] = user_id
            session['user_attributes'] = attributes
        else:
            flash('Unable to register user. Please try logging in.', 'error')
            return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            message = request.form.get('message', '').strip()
            policy = request.form.get('policy', 'user').strip()  # Default policy
            
            if not message:
                flash('Message is required!', 'error')
                return redirect(url_for('encrypt_data'))
            
            if not policy:
                policy = 'user'  # Fallback to default
            
            print(f"DEBUG: Encrypting with policy: '{policy}'")
            
            # Encrypt the message
            data_id = abe.encrypt(message, policy)
            
            log_activity(session['user_id'], 'encrypt', f'Data encrypted with policy: {policy}')
            flash(f'Data encrypted successfully! Data ID: {data_id}', 'success')
            
            return render_template('encrypt_result.html', data_id=data_id, policy=policy, users=users)
            
        except Exception as e:
            flash(f'Encryption failed: {str(e)}', 'error')
            log_activity(session.get('user_id', 'anonymous'), 'encrypt_failed', str(e))
    
    return render_template('encrypt.html', users=users)

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt_data():
    """Decrypt data/message"""
    # Auto-login if not logged in
    if 'user_id' not in session:
        user_id = 'user'
        attributes = ['user', 'read_access', 'write_access', 'admin']
        
        # Ensure user is registered before proceeding
        if ensure_user_registered(user_id, attributes):
            session['user_id'] = user_id
            session['user_attributes'] = attributes
        else:
            flash('Unable to register user. Please try logging in.', 'error')
            return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            data_id = request.form.get('data_id', '').strip()
            
            print(f"DEBUG: Decrypt attempt by user '{session['user_id']}' for data '{data_id}'")
            
            if not data_id:
                flash('Data ID is required!', 'error')
                return redirect(url_for('decrypt_data'))
            
            # Ensure user is properly registered before decryption
            user_id = session['user_id']
            user_attributes = session.get('user_attributes', [])
            
            print(f"DEBUG: User {user_id} has attributes: {user_attributes}")
            
            if not ensure_user_registered(user_id, user_attributes):
                flash('Failed to verify user registration. Please try logging in again.', 'error')
                return redirect(url_for('login'))
            
            # Decrypt the message
            print(f"DEBUG: Attempting decryption...")
            message = abe.decrypt(user_id, data_id)
            print(f"DEBUG: Decryption successful, message length: {len(message)}")
            
            # Create a downloadable file for the decrypted message
            download_filename = f"decrypted_message_{data_id[:8]}.txt"
            download_path = os.path.join(DOWNLOAD_FOLDER, download_filename)
            
            # Ensure download folder exists
            if not os.path.exists(DOWNLOAD_FOLDER):
                os.makedirs(DOWNLOAD_FOLDER)
            
            # Save decrypted message to file
            with open(download_path, 'w', encoding='utf-8') as f:
                f.write(message)
            
            log_activity(session['user_id'], 'decrypt', f'Data decrypted: {data_id}')
            flash('Data decrypted successfully!', 'success')
            
            return render_template('decrypt_result.html', 
                                 message=message, 
                                 data_id=data_id, 
                                 download_link=download_filename,
                                 users=users)
            
        except Exception as e:
            error_msg = str(e)
            print(f"DEBUG: Decryption failed with error: {error_msg}")
            flash(f'Decryption failed: {error_msg}', 'error')
            log_activity(session.get('user_id', 'anonymous'), 'decrypt_failed', str(e))
    
    return render_template('decrypt.html', users=users)

@app.route('/file_encrypt', methods=['GET', 'POST'])
def file_encrypt():
    """Encrypt file"""
    # Auto-login if not logged in
    if 'user_id' not in session:
        user_id = 'user'
        attributes = ['user', 'read_access', 'write_access', 'admin']
        
        # Ensure user is registered before proceeding
        if ensure_user_registered(user_id, attributes):
            session['user_id'] = user_id
            session['user_attributes'] = attributes
        else:
            flash('Unable to register user. Please try logging in.', 'error')
            return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                flash('No file selected!', 'error')
                return redirect(url_for('file_encrypt'))
            
            file = request.files['file']
            policy = request.form.get('policy', 'user').strip()  # Default policy
            
            if file.filename == '':
                flash('No file selected!', 'error')
                return redirect(url_for('file_encrypt'))
            
            # Read file content
            file_content = file.read()
            if len(file_content) > MAX_FILE_SIZE:
                flash(f'File too large! Max size: {MAX_FILE_SIZE // (1024*1024)}MB', 'error')
                return redirect(url_for('file_encrypt'))
            
            # Create file info with proper error handling
            filename = secure_filename(file.filename) or 'unnamed_file'
            file_info = {
                'filename': filename,
                'size': len(file_content),
                'content': base64.b64encode(file_content).decode('utf-8'),
                'type': 'file'
            }
            
            # Encrypt the file data
            data_id = abe.encrypt(json.dumps(file_info), policy)
            
            log_activity(session['user_id'], 'file_encrypt', f'File encrypted: {filename}')
            flash(f'File encrypted successfully! Data ID: {data_id}', 'success')
            
            return render_template('encrypt_result.html', 
                                 data_id=data_id, 
                                 policy=policy, 
                                 filename=filename,
                                 users=users)
            
        except Exception as e:
            flash(f'File encryption failed: {str(e)}', 'error')
            log_activity(session.get('user_id', 'anonymous'), 'file_encrypt_failed', str(e))
            return redirect(url_for('file_encrypt'))
    
    return render_template('file_encrypt.html', users=users)

@app.route('/file_decrypt', methods=['GET', 'POST'])
def file_decrypt():
    """Decrypt file"""
    # Auto-login if not logged in
    if 'user_id' not in session:
        user_id = 'user'
        attributes = ['user', 'read_access', 'write_access', 'admin']
        
        # Ensure user is registered before proceeding
        if ensure_user_registered(user_id, attributes):
            session['user_id'] = user_id
            session['user_attributes'] = attributes
        else:
            flash('Unable to register user. Please try logging in.', 'error')
            return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            data_id = request.form.get('data_id', '').strip()
            
            if not data_id:
                flash('Data ID is required!', 'error')
                return redirect(url_for('file_decrypt'))
            
            # Decrypt the file data
            print(f"DEBUG: Attempting to decrypt file with data ID: {data_id}")
            decrypted_data = abe.decrypt(session['user_id'], data_id)
            print(f"DEBUG: Decryption successful, data length: {len(decrypted_data)}")
            
            try:
                # Try to parse as file data
                file_info = json.loads(decrypted_data)
                print(f"DEBUG: Successfully parsed as JSON file info")
                
                if 'content' in file_info and 'filename' in file_info:
                    # It's a file - decode and save
                    file_content = base64.b64decode(file_info['content'])
                    filename = file_info.get('filename', 'decrypted_file')
                    
                    print(f"DEBUG: File detected - filename: {filename}, size: {len(file_content)} bytes")
                    
                    # Preserve original file extension
                    original_ext = os.path.splitext(filename)[1]
                    if not original_ext:
                        # If no extension, try to determine from content
                        if filename.lower().endswith('.csv') or 'csv' in filename.lower():
                            original_ext = '.csv'
                        else:
                            original_ext = '.txt'
                    
                    # Save to downloads folder with preserved extension
                    base_name = os.path.splitext(filename)[0]
                    download_filename = f"{uuid.uuid4().hex[:8]}_{base_name}{original_ext}"
                    download_path = os.path.join(DOWNLOAD_FOLDER, download_filename)
                    
                    # Ensure downloads folder exists
                    if not os.path.exists(DOWNLOAD_FOLDER):
                        os.makedirs(DOWNLOAD_FOLDER)
                    
                    with open(download_path, 'wb') as f:
                        f.write(file_content)
                    
                    print(f"DEBUG: File saved to: {download_path}")
                    
                    log_activity(session['user_id'], 'file_decrypt', f'File decrypted: {filename}')
                    flash(f'File "{filename}" decrypted successfully!', 'success')
                    
                    # Ensure file_size is an integer
                    file_size = file_info.get('size', len(file_content))
                    if isinstance(file_size, str):
                        try:
                            file_size = int(file_size)
                        except ValueError:
                            file_size = len(file_content)
                    
                    return render_template('decrypt_result.html',
                                         message="file_decrypted",  # Trigger to show result section
                                         filename=filename,
                                         file_size=file_size,
                                         download_link=download_filename,
                                         users=users)
                else:
                    # It's structured data but not a file
                    raise json.JSONDecodeError("Not a file", "", 0)
                    
            except (json.JSONDecodeError, KeyError, ValueError):
                # It's a regular message, not a file
                log_activity(session['user_id'], 'decrypt', f'Message decrypted: {data_id}')
                flash('Data decrypted successfully! (Plain text message)', 'success')
                return render_template('decrypt_result.html', message=decrypted_data, data_id=data_id, users=users)
            
        except Exception as e:
            flash(f'Decryption failed: {str(e)}', 'error')
            log_activity(session.get('user_id', 'anonymous'), 'decrypt_failed', str(e))
            return redirect(url_for('file_decrypt'))
    
    return render_template('file_decrypt.html', users=users)

@app.route('/download/<filename>')
def download_file(filename):
    """Download decrypted file"""
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(file_path):
        try:
            return send_file(file_path, as_attachment=True)
        except Exception as e:
            flash(f'Download failed: {str(e)}', 'error')
            return redirect(url_for('dashboard'))
    else:
        flash('File not found!', 'error')
        return redirect(url_for('dashboard'))

@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    """User management"""
    # Auto-login if not logged in
    if 'user_id' not in session:
        user_id = 'admin'
        attributes = ['user', 'read_access', 'write_access', 'admin']
        
        # Ensure user is registered before proceeding
        if ensure_user_registered(user_id, attributes):
            session['user_id'] = user_id
            session['user_attributes'] = attributes
        else:
            flash('Unable to register admin user. Please try logging in.', 'error')
            return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            action = request.form.get('action')
            target_user = request.form.get('user_id', '').strip()
            
            print(f"DEBUG: Received action: {action}, target_user: {target_user}")  # Debug print
            
            if action == 'issue_ac':
                attributes_str = request.form.get('attributes', '').strip()
                password = request.form.get('password', 'default123')
                
                print(f"DEBUG: Attributes string: {attributes_str}")  # Debug print
                
                if not target_user:
                    flash('User ID is required!', 'error')
                    return redirect(url_for('manage_users'))
                
                if not attributes_str:
                    flash('Attributes are required!', 'error')
                    return redirect(url_for('manage_users'))
                
                # Parse attributes
                attributes = [attr.strip() for attr in attributes_str.split(',') if attr.strip()]
                
                if not attributes:
                    flash('At least one valid attribute is required!', 'error')
                    return redirect(url_for('manage_users'))
                
                print(f"DEBUG: Parsed attributes: {attributes}")  # Debug print
                
                try:
                    # Issue AC using ABE system
                    ac = abe.issue_ac(target_user, attributes)
                    
                    # Update local user store
                    users[target_user] = {
                        'password': generate_password_hash(password),
                        'attributes': attributes,
                        'role': 'admin' if 'admin' in attributes else 'user'
                    }
                    
                    log_activity(session['user_id'], 'issue_ac', f'AC issued for {target_user} with attributes: {attributes}')
                    flash(f'[SUCCESS] Access Control successfully issued for "{target_user}" with attributes: {", ".join(attributes)}', 'success')
                    
                    print(f"DEBUG: Successfully issued AC for {target_user}")  # Debug print
                    
                except Exception as ac_error:
                    print(f"DEBUG: AC issue failed: {ac_error}")  # Debug print
                    flash(f'Failed to issue AC: {str(ac_error)}', 'error')
            
            elif action == 'revoke_attribute':
                attribute = request.form.get('attribute', '').strip()
                
                if not target_user or not attribute:
                    flash('User ID and attribute are required for revocation!', 'error')
                    return redirect(url_for('manage_users'))
                
                try:
                    new_ac = abe.revoke_attribute(target_user, attribute)
                    
                    # Update local user store
                    if target_user in users:
                        user_attrs = users[target_user]['attributes']
                        if attribute in user_attrs:
                            user_attrs.remove(attribute)
                    
                    log_activity(session['user_id'], 'revoke_attribute', f'Revoked {attribute} from {target_user}')
                    flash(f'[SUCCESS] Attribute "{attribute}" revoked from "{target_user}"!', 'success')
                    
                except Exception as revoke_error:
                    flash(f'Failed to revoke attribute: {str(revoke_error)}', 'error')
            
            else:
                flash('Invalid action specified!', 'error')
                    
        except Exception as e:
            print(f"DEBUG: General error in manage_users: {e}")  # Debug print
            flash(f'Operation failed: {str(e)}', 'error')
            log_activity(session['user_id'], 'manage_users_failed', str(e))
    
    return render_template('manage_users.html', users=users)

@app.route('/activity_log')
def view_activity_log():
    """View activity log"""
    # Auto-login if not logged in
    if 'user_id' not in session:
        session['user_id'] = 'admin'
        session['user_attributes'] = ['user', 'read_access', 'write_access', 'admin']
    
    # Show only last 20 entries for compact view
    recent_logs = list(reversed(activity_log))[:20]
    return render_template('activity_log.html', activity_log=recent_logs, users=users)

@app.route('/user_attributes', methods=['GET', 'POST'])
def user_attributes():
    """User attribute management"""
    # Auto-login if not logged in
    if 'user_id' not in session:
        session['user_id'] = 'user'
        session['user_attributes'] = ['user', 'read_access']
    
    if request.method == 'POST':
        try:
            action = request.form.get('action')
            user_id = session['user_id']
            
            if action == 'add_custom':
                # Add a single custom attribute
                custom_attr = request.form.get('custom_attribute', '').strip()
                if custom_attr:
                    # Validate attribute name (alphanumeric and underscore only)
                    if custom_attr.replace('_', '').replace('-', '').isalnum():
                        current_attrs = session.get('user_attributes', [])
                        if custom_attr not in current_attrs:
                            current_attrs.append(custom_attr)
                            session['user_attributes'] = current_attrs
                            
                            # Update in users dictionary if exists
                            if user_id in users:
                                users[user_id]['attributes'] = current_attrs
                            
                            flash(f'Attribute "{custom_attr}" added successfully!', 'success')
                            log_activity(user_id, 'attribute_added', f'Added attribute: {custom_attr}')
                        else:
                            flash(f'Attribute "{custom_attr}" already exists!', 'warning')
                    else:
                        flash('Invalid attribute name. Use only letters, numbers, and underscores.', 'error')
                else:
                    flash('Please enter an attribute name.', 'error')
                    
            elif action == 'save_attributes':
                # Save all attributes from the form
                attributes_str = request.form.get('attributes', '').strip()
                if attributes_str:
                    new_attributes = [attr.strip() for attr in attributes_str.split(',') if attr.strip()]
                    session['user_attributes'] = new_attributes
                    
                    # Update in users dictionary if exists
                    if user_id in users:
                        users[user_id]['attributes'] = new_attributes
                    
                    flash(f'Attributes updated successfully! You now have {len(new_attributes)} attributes.', 'success')
                    log_activity(user_id, 'attributes_updated', f'Updated to: {", ".join(new_attributes)}')
                else:
                    # Clear all attributes
                    session['user_attributes'] = []
                    if user_id in users:
                        users[user_id]['attributes'] = []
                    flash('All attributes cleared.', 'info')
                    log_activity(user_id, 'attributes_cleared', 'All attributes removed')
                    
        except Exception as e:
            flash(f'Error updating attributes: {str(e)}', 'error')
            log_activity(session.get('user_id', 'anonymous'), 'attribute_update_failed', str(e))
    
    return render_template('user_attributes.html', 
                         user_attributes=session.get('user_attributes', []),
                         user_id=session.get('user_id', 'user'),
                         users=users)

@app.route('/policy_checker')
def policy_checker():
    """Policy checker tool"""
    # Auto-login if not logged in
    if 'user_id' not in session:
        session['user_id'] = 'user'
        session['user_attributes'] = ['user', 'read_access']
    
    return render_template('policy_checker.html', 
                         user_attributes=session.get('user_attributes', []),
                         user_id=session.get('user_id', 'user'),
                         users=users)

@app.route('/update_user_attributes', methods=['POST'])
def update_user_attributes():
    """Update user attributes via AJAX"""
    try:
        # Auto-login if not logged in
        if 'user_id' not in session:
            session['user_id'] = 'user'
            session['user_attributes'] = ['user', 'read_access']
        
        action = request.form.get('action')
        user_id = session['user_id']
        
        if action == 'update_attributes':
            attributes_str = request.form.get('attributes', '').strip()
            if attributes_str:
                new_attributes = [attr.strip() for attr in attributes_str.split(',') if attr.strip()]
                # Validate each attribute
                for attr in new_attributes:
                    if not attr.replace('_', '').replace('-', '').isalnum():
                        return jsonify({'success': False, 'error': f'Invalid attribute: {attr}'})
                
                session['user_attributes'] = new_attributes
                
                # Update in users dictionary if exists
                if user_id in users:
                    users[user_id]['attributes'] = new_attributes
                
                log_activity(user_id, 'attributes_updated_inline', f'Updated to: {", ".join(new_attributes)}')
                return jsonify({'success': True, 'attributes': new_attributes})
            else:
                # Clear all attributes
                session['user_attributes'] = []
                if user_id in users:
                    users[user_id]['attributes'] = []
                log_activity(user_id, 'attributes_cleared_inline', 'All attributes removed')
                return jsonify({'success': True, 'attributes': []})
        
        return jsonify({'success': False, 'error': 'Invalid action'})
        
    except Exception as e:
        log_activity(session.get('user_id', 'anonymous'), 'attribute_update_failed_inline', str(e))
        return jsonify({'success': False, 'error': str(e)})

# API Endpoints
@app.route('/api/encrypt', methods=['POST'])
def api_encrypt():
    """API endpoint for encryption"""
    try:
        data = request.get_json()
        message = data.get('message')
        policy = data.get('policy')
        
        if not message or not policy:
            return jsonify({'error': 'Message and policy are required'}), 400
        
        data_id = abe.encrypt(message, policy)
        return jsonify({'success': True, 'data_id': data_id})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/decrypt', methods=['POST'])
def api_decrypt():
    """API endpoint for decryption"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        data_id = data.get('data_id')
        
        if not user_id or not data_id:
            return jsonify({'error': 'User ID and data ID are required'}), 400
        
        message = abe.decrypt(user_id, data_id)
        return jsonify({'success': True, 'message': message})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'users_online': len([k for k in session.keys() if k == 'user_id']),
        'total_users': len(users)
    })

if __name__ == '__main__':
    print("Starting Secure Data Sharing Web Application...")
    print("Access the application at: http://localhost:5000")
    print("No login required - Direct access available!")
    print("Or visit /login to set a custom username")
    print("Application ready!")
    
    # Run the application
    app.run(
        debug=True,  # Set to False in production
        host='0.0.0.0',  # Makes it accessible from other devices on network
        port=5000
    )
