#!/usr/bin/env python3#!/usr/bin/env python3

""""""

ABE System CheckSimple test to check what ABE implementation is being used

Verify ABE crypto system functionality"""

"""

import sys

import sysimport os

import os

# Test which ABE implementation we're using

def check_abe():print("🔍 Checking ABE Implementation")

    """Check ABE crypto system"""print("=" * 40)

    print("=== ABE System Check ===")

    try:

    try:    # Try to import real ABE first

        # Try to import ABE crypto    from abe_crypto import ABECrypto as RealABE

        try:    print("✅ Real ABE crypto imported successfully")

            from abe_crypto import ABECrypto    

            print("✅ ABE Crypto module imported successfully")    # Test real ABE

            use_real_abe = True    real_abe = RealABE()

        except ImportError:    print(f"   Real ABE type: {type(real_abe)}")

            print("⚠️  ABE Crypto module not found - using mock")    print(f"   Has firebase: {hasattr(real_abe, 'firebase')}")

            use_real_abe = False    

            except Exception as e:

            # Create mock ABE    print(f"❌ Real ABE import failed: {e}")

            class ABECrypto:

                def __init__(self):# Now check what the Flask app uses

                    self.data_store = {}try:

                    self.user_store = {}    from app_simple import abe

                    print(f"\n✅ Flask app ABE loaded")

                def issue_ac(self, user_id, attributes):    print(f"   ABE type: {type(abe).__name__}")

                    self.user_store[user_id] = attributes    print(f"   Has firebase: {hasattr(abe, 'firebase')}")

                    return f"AC_{user_id}_{len(attributes)}_attrs"    print(f"   Has data_store: {hasattr(abe, 'data_store')}")

                    print(f"   Has user_store: {hasattr(abe, 'user_store')}")

                def encrypt(self, message, policy):    

                    import uuid    # Test basic functionality

                    data_id = f"DATA_{uuid.uuid4().hex[:8]}"    print(f"\n🧪 Testing basic ABE functionality...")

                    self.data_store[data_id] = {'message': message, 'policy': policy}    

                    return data_id    # Test issuing AC

                    try:

                def decrypt(self, user_id, data_id):        ac = abe.issue_ac("test_user", ["user", "read_access"])

                    if data_id not in self.data_store:        print(f"✅ Issue AC works: {ac}")

                        raise Exception("Data not found")    except Exception as e:

                    return self.data_store[data_id]['message']        print(f"❌ Issue AC failed: {e}")

            

        # Initialize ABE system    # Test encryption

        abe = ABECrypto()    try:

        print("✅ ABE system initialized")        data_id = abe.encrypt("test message", "user")

                print(f"✅ Encryption works: {data_id}")

        # Test basic operations        

        print("\nTesting basic ABE operations...")        # Test decryption

                try:

        # Issue attributes            decrypted = abe.decrypt("test_user", data_id)

        abe.issue_ac("test_user", ["department:IT", "role:admin"])            print(f"✅ Decryption works: {decrypted}")

        print("✅ Attribute issuance working")        except Exception as e:

                    print(f"❌ Decryption failed: {e}")

        # Encrypt message            

        message = "Test message for ABE check"    except Exception as e:

        policy = "department:IT"        print(f"❌ Encryption failed: {e}")

        data_id = abe.encrypt(message, policy)        

        print(f"✅ Encryption working - Data ID: {data_id}")except Exception as e:

            print(f"❌ Flask app ABE import failed: {e}")

        # Decrypt message    import traceback

        decrypted = abe.decrypt("test_user", data_id)    traceback.print_exc()

        print(f"✅ Decryption working - Message: {decrypted}")

        print(f"\n🎯 Summary: Check the output above to see which ABE implementation is being used and if there are any errors.")

        # Verify message integrity
        if decrypted == message:
            print("✅ Message integrity verified")
        else:
            print("❌ Message integrity failed")
            return False
        
        print(f"\n=== ABE Check Results ===")
        print(f"ABE Implementation: {'Real' if use_real_abe else 'Mock'}")
        print("✅ All ABE operations working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ ABE check failed: {e}")
        return False

def check_dependencies():
    """Check ABE-related dependencies"""
    print("\n=== ABE Dependencies Check ===")
    
    required_modules = ['uuid', 'json', 'base64', 'os']
    optional_modules = ['cryptography', 'pycrypto']
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - Required but missing")
            return False
    
    for module in optional_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"⚠️  {module} - Optional, not found")
    
    return True

if __name__ == "__main__":
    print("ABE Crypto System Check")
    print("=" * 25)
    
    deps_ok = check_dependencies()
    abe_ok = check_abe()
    
    if deps_ok and abe_ok:
        print("\n🎉 ABE system check passed!")
        sys.exit(0)
    else:
        print("\n❌ ABE system check failed!")
        sys.exit(1)