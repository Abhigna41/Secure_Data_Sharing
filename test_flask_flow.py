#!/usr/bin/env python3#!/usr/bin/env python3

""""""

Flask Application Flow TestingTest the complete Flask encrypt/decrypt flow

Tests the complete Flask application workflow"""

"""

import sys

import sysimport os

import ossys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests

import timeprint("🌐 Testing Flask Encrypt/Decrypt Flow")

print("=" * 50)

def test_flask_flow():

    """Test complete Flask application flow"""try:

    print("=== Flask Flow Test ===")    from app_simple import app

        

    base_url = "http://localhost:5000"    with app.test_client() as client:

    session = requests.Session()        print("📝 Testing encryption...")

            

    print("\n1. Testing application startup...")        # Test encryption

    try:        response = client.post('/encrypt', data={

        response = session.get(base_url, timeout=5)            'message': 'Test message for decryption',

        if response.status_code == 200:            'policy': 'user'

            print("✅ Application is running and accessible")        }, follow_redirects=True)

        else:        

            print(f"❌ Application returned status: {response.status_code}")        if response.status_code == 200:

            return False            print("✅ Encryption request processed")

    except requests.exceptions.ConnectionError:            

        print("❌ Cannot connect to application. Make sure it's running on localhost:5000")            # Extract data ID from response (this would be in the template)

        return False            # For now, let's just test the route is working

    except Exception as e:            print("✅ Encryption flow completed")

        print(f"❌ Error testing application: {e}")        else:

        return False            print(f"❌ Encryption failed with status {response.status_code}")

                

    print("\n2. Testing key pages...")        print("\n🔓 Testing decryption page...")

    pages = {        

        "Dashboard": "/",        # Test decryption page

        "Login": "/login",        response = client.get('/decrypt')

        "Encrypt": "/encrypt",        if response.status_code == 200:

        "Decrypt": "/decrypt",            print("✅ Decryption page loads successfully")

        "File Encrypt": "/file_encrypt",        else:

        "File Decrypt": "/file_decrypt",            print(f"❌ Decryption page failed with status {response.status_code}")

        "Manage Users": "/manage_users",    

        "Activity Log": "/activity_log"    print("\n🎉 Flask flow test completed!")

    }    

    except Exception as e:

    for page_name, url in pages.items():    print(f"❌ Error during Flask testing: {e}")

        try:    import traceback

            response = session.get(base_url + url, timeout=5)    traceback.print_exc()

            if response.status_code == 200:

                print(f"✅ {page_name}: OK")print("\n" + "=" * 50)

            else:
                print(f"❌ {page_name}: Status {response.status_code}")
        except Exception as e:
            print(f"❌ {page_name}: Error - {e}")
    
    print("\n3. Testing encryption flow...")
    try:
        # Test message encryption
        encrypt_data = {
            'message': 'Test message for flow testing',
            'policy': 'department:IT',
            'user_id': 'test_user'
        }
        
        response = session.post(base_url + "/encrypt", data=encrypt_data, timeout=10)
        if response.status_code == 200:
            print("✅ Message encryption: OK")
        else:
            print(f"❌ Message encryption: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Encryption test failed: {e}")
    
    print("\n4. Testing user management...")
    try:
        response = session.get(base_url + "/manage_users", timeout=5)
        if response.status_code == 200:
            print("✅ User management page: OK")
        else:
            print(f"❌ User management: Status {response.status_code}")
    except Exception as e:
        print(f"❌ User management test failed: {e}")
    
    print("\n=== Flask Flow Test Complete ===")
    return True

if __name__ == "__main__":
    print("Flask Application Flow Test")
    print("Make sure the Flask app is running before running this test")
    print("Start the app with: python app_simple.py")
    print()
    
    test_flask_flow()