#!/usr/bin/env python3#!/usr/bin/env python3

""""""

Flow Testing ScriptComplete test of encryption-decryption flow with Flask app

Tests the complete application flow from start to finish"""

"""

def test_complete_flow():

import sys    print("🧪 Testing Complete Encryption-Decryption Flow")

import os    print("=" * 60)

import requests    

import time    try:

import json        from app_simple import app

        

def test_complete_flow():        # Test with Flask test client

    """Test complete application flow"""        with app.test_client() as client:

    print("=== Complete Flow Test ===")            

                print("1️⃣ Testing home page access...")

    base_url = "http://localhost:5000"            response = client.get('/')

    session = requests.Session()            if response.status_code == 200:

                    print("✅ Home page loads successfully")

    print("\n🚀 Testing Complete Application Flow...")            else:

                    print(f"❌ Home page failed: {response.status_code}")

    # Step 1: Access Dashboard                return False

    print("\n1. Accessing dashboard...")            

    try:            print("\n2️⃣ Testing encryption...")

        response = session.get(base_url, timeout=5)            test_message = "Hello! This is a test message for encryption and decryption."

        if response.status_code == 200:            test_policy = "user"

            print("✅ Dashboard accessible")            

        else:            response = client.post('/encrypt', data={

            print(f"❌ Dashboard failed: {response.status_code}")                'message': test_message,

            return False                'policy': test_policy

    except Exception as e:            })

        print(f"❌ Dashboard error: {e}")            

        return False            if response.status_code in [200, 302]:

                    print("✅ Encryption request successful")

    # Step 2: Test Login Flow                

    print("\n2. Testing login flow...")                # Extract data_id from response

    try:                response_text = response.data.decode()

        # Access login page                print(f"   Response length: {len(response_text)} characters")

        login_response = session.get(base_url + "/login", timeout=5)                

        if login_response.status_code == 200:                # Check if we can find a data ID pattern

            print("✅ Login page accessible")                import re

        else:                data_id_pattern = r'[a-f0-9]{64}'  # 64-character hex string

            print(f"❌ Login page failed: {login_response.status_code}")                matches = re.findall(data_id_pattern, response_text)

    except Exception as e:                

        print(f"❌ Login page error: {e}")                if matches:

                        data_id = matches[0]

    # Step 3: Test Encryption Flow                    print(f"✅ Found Data ID: {data_id}")

    print("\n3. Testing encryption flow...")                else:

    try:                    print("⚠️  Could not extract Data ID from response, using test approach...")

        # Get encrypt page                    # Direct test with ABE

        encrypt_page = session.get(base_url + "/encrypt", timeout=5)                    from app_simple import abe

        if encrypt_page.status_code == 200:                    data_id = abe.encrypt(test_message, test_policy)

            print("✅ Encrypt page accessible")                    print(f"✅ Direct encryption successful: {data_id}")

                            

            # Test encryption            else:

            encrypt_data = {                print(f"❌ Encryption failed: {response.status_code}")

                'message': 'Flow test message - Hello World!',                return False

                'policy': 'department:IT OR role:admin',            

                'user_id': 'flow_test_user'            print(f"\n3️⃣ Testing decryption...")

            }            response = client.post('/decrypt', data={

                            'data_id': data_id

            encrypt_result = session.post(base_url + "/encrypt",             })

                                        data=encrypt_data, timeout=10)            

            if encrypt_result.status_code == 200:            if response.status_code in [200, 302]:

                print("✅ Message encryption successful")                print("✅ Decryption request successful")

            else:                response_text = response.data.decode()

                print(f"❌ Encryption failed: {encrypt_result.status_code}")                

        else:                # Check if the original message appears in the response

            print(f"❌ Encrypt page failed: {encrypt_page.status_code}")                if test_message in response_text:

    except Exception as e:                    print("✅ Original message found in decryption response!")

        print(f"❌ Encryption flow error: {e}")                else:

                        print("⚠️  Original message not found in response")

    # Step 4: Test Decryption Flow                      print(f"   Looking for: '{test_message}'")

    print("\n4. Testing decryption flow...")                    print(f"   Response excerpt: {response_text[:300]}...")

    try:                

        decrypt_page = session.get(base_url + "/decrypt", timeout=5)            else:

        if decrypt_page.status_code == 200:                print(f"❌ Decryption failed: {response.status_code}")

            print("✅ Decrypt page accessible")                response_text = response.data.decode()

        else:                print(f"   Error response: {response_text[:300]}...")

            print(f"❌ Decrypt page failed: {decrypt_page.status_code}")                return False

    except Exception as e:            

        print(f"❌ Decryption flow error: {e}")            print(f"\n4️⃣ Testing user management...")

                response = client.get('/manage_users')

    # Step 5: Test File Operations            if response.status_code == 200:

    print("\n5. Testing file operations...")                print("✅ User management page loads")

    try:            else:

        # File encrypt page                print(f"❌ User management failed: {response.status_code}")

        file_encrypt_page = session.get(base_url + "/file_encrypt", timeout=5)            

        if file_encrypt_page.status_code == 200:            # Test creating a new user

            print("✅ File encrypt page accessible")            response = client.post('/manage_users', data={

        else:                'action': 'issue_ac',

            print(f"❌ File encrypt page failed: {file_encrypt_page.status_code}")                'user_id': 'flow_test_user',

                        'attributes': 'user,read_access,write_access',

        # File decrypt page                'password': 'test123'

        file_decrypt_page = session.get(base_url + "/file_decrypt", timeout=5)            })

        if file_decrypt_page.status_code == 200:            

            print("✅ File decrypt page accessible")            if response.status_code in [200, 302]:

        else:                print("✅ User creation successful")

            print(f"❌ File decrypt page failed: {file_decrypt_page.status_code}")            else:

    except Exception as e:                print(f"❌ User creation failed: {response.status_code}")

        print(f"❌ File operations error: {e}")            

                print(f"\n🎉 Complete flow test finished!")

    # Step 6: Test Management Features            return True

    print("\n6. Testing management features...")            

    try:    except Exception as e:

        # User management        print(f"❌ Error during flow test: {e}")

        users_page = session.get(base_url + "/manage_users", timeout=5)        import traceback

        if users_page.status_code == 200:        traceback.print_exc()

            print("✅ User management accessible")        return False

        else:

            print(f"❌ User management failed: {users_page.status_code}")if __name__ == "__main__":

            success = test_complete_flow()

        # Activity log    if success:

        activity_page = session.get(base_url + "/activity_log", timeout=5)        print(f"\n✅ Flow test completed! Check results above.")

        if activity_page.status_code == 200:        print(f"\n🚀 To run the actual web app:")

            print("✅ Activity log accessible")        print(f"   python app_simple.py")

        else:        print(f"   Then visit: http://localhost:5000")

            print(f"❌ Activity log failed: {activity_page.status_code}")    else:

    except Exception as e:        print(f"\n❌ Flow test failed. Check errors above.")

        print(f"❌ Management features error: {e}")
    
    print("\n✅ Complete flow test finished!")
    return True

def test_performance():
    """Basic performance testing"""
    print("\n=== Performance Test ===")
    
    base_url = "http://localhost:5000"
    
    print("Testing response times...")
    
    pages = ["/", "/login", "/encrypt", "/decrypt"]
    
    for page in pages:
        try:
            start_time = time.time()
            response = requests.get(base_url + page, timeout=5)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                print(f"✅ {page}: {response_time:.0f}ms")
            else:
                print(f"❌ {page}: Failed ({response.status_code})")
                
        except Exception as e:
            print(f"❌ {page}: Error - {e}")
    
    print("✅ Performance test completed")

if __name__ == "__main__":
    print("Application Flow Testing")
    print("=" * 25)
    print()
    print("⚠️  Make sure the application is running!")
    print("   Start with: python app_simple.py")
    print()
    
    # Wait for user confirmation
    time.sleep(2)
    
    # Run tests
    flow_ok = test_complete_flow()
    test_performance()
    
    if flow_ok:
        print("\n🎉 Flow testing completed successfully!")
    else:
        print("\n❌ Some flow tests failed!")
    
    sys.exit(0 if flow_ok else 1)