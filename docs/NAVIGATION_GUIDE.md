# 🗺️ Secure Data Sharing System - Navigation Guide

## Where to Find Activity Logs and Other Options

### 🏠 **Main Navigation (Sidebar)**
When you log into the system, you'll see a sidebar on the left with all available options:

#### 📊 **Always Available (All Users):**
- **Dashboard** - `/` - Main overview page with statistics and quick actions
- **Encrypt Message** - `/encrypt` - Encrypt text messages with access policies  
- **Decrypt Message** - `/decrypt` - Decrypt messages using your attributes
- **Encrypt File** - `/file_encrypt` - Upload and encrypt files
- **Decrypt File** - `/file_decrypt` - Decrypt and download files

#### 🔧 **Admin Only Options:**
*These appear only if you're logged in as admin or have admin attributes*

- **Manage Users** - `/manage_users` - Issue access controls, manage user attributes
- **📋 Activity Log** - `/activity_log` - **THIS IS WHERE YOU'LL FIND THE ACTIVITY LOGS!**

### 🚀 **How to Access the Activity Log:**

1. **Start the Application:**
   ```bash
   python app_simple.py
   ```

2. **Open in Browser:**
   ```
   http://localhost:5000
   ```

3. **Login Options:**
   - **Admin Tab:** Enter "admin" as username (gets admin privileges)
   - **Guest Tab:** Click "Continue as Guest" (limited access)

4. **Navigate to Activity Log:**
   - Look at the sidebar on the left
   - Click on **"Activity Log"** (📋 icon)
   - This will take you to `/activity_log`

### 📊 **What You'll See in Activity Log:**

#### **Main Table:**
- **Timestamp** - When the action occurred
- **User** - Who performed the action  
- **Action** - What they did (Login, Encrypt, Decrypt, etc.)
- **Details** - Additional information about the action

#### **Activity Statistics Cards:**
- **Total Logins** - Count of login activities
- **Encryptions** - Count of encrypt operations (messages + files)
- **Decryptions** - Count of decrypt operations (messages + files)  
- **Total Users** - Number of registered users

### 🎯 **Activity Types Tracked:**

| Action | Badge Color | Description |
|--------|-------------|-------------|
| **Login** | 🟢 Green | User login events |
| **Encrypt** | 🔵 Blue | Message encryption |
| **Decrypt** | 🟡 Yellow | Message decryption |
| **File Encrypt** | 🔵 Cyan | File encryption |
| **File Decrypt** | 🔵 Cyan | File decryption |
| **Other** | ⚫ Gray | System operations |

### 🔐 **Access Requirements:**

- **Activity Log is ADMIN ONLY** - You need admin privileges to view it
- If you don't see it in the sidebar, you're not logged in as admin
- Use the "Admin" login tab and enter "admin" as the username

### 🎨 **Clean Theme Features:**

The Activity Log now features:
- ✅ Clean white cards with professional styling
- ✅ Color-coded action badges for easy identification
- ✅ Responsive table design with hover effects
- ✅ Statistical overview cards
- ✅ Professional admin dashboard appearance
- ✅ No gradients or vibrant colors (corporate-friendly)

### 🛠️ **Quick Start Guide:**

1. **Run:** `python app_simple.py`
2. **Visit:** `http://localhost:5000`
3. **Login as Admin:** Use "admin" in the Admin tab
4. **Click:** "Activity Log" in the sidebar
5. **View:** All system activities and statistics

The activity log automatically tracks all user actions and displays them in a clean, professional interface perfect for monitoring system usage and security auditing.
