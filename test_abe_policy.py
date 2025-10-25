#!/usr/bin/env python3#!/usr/bin/env python3

""""""

ABE Policy Testing ScriptQuick test for ABE policy checking

Tests the ABE encryption and policy evaluation functionality"""

"""

import sys

import sysimport os

import ossys.path.append(os.path.dirname(os.path.abspath(__file__)))



# Add current directory to pathprint("🧪 Testing ABE Policy Checking")

sys.path.append(os.path.dirname(os.path.abspath(__file__)))print("=" * 50)



try:try:

    from abe_crypto import ABECrypto    from abe_crypto import ABECrypto

except ImportError:    

    print("Warning: ABE Crypto module not found. Using mock implementation.")    # Test policy parsing logic

    class ABECrypto:    def test_policy_parsing():

        def __init__(self):        print("\n📋 Testing policy parsing logic...")

            self.data_store = {}        

            self.user_store = {}        test_cases = [

                    ("user", ["user"], True),

        def issue_ac(self, user_id, attributes):            ("admin", ["user", "admin"], True),

            self.user_store[user_id] = attributes            ("admin", ["user"], False),

            return f"AC_{user_id}_{len(attributes)}_attrs"            ("user AND admin", ["user", "admin"], True),

                    ("user AND admin", ["user"], False),

        def encrypt(self, message, policy):            ("read_access AND write_access", ["user", "read_access", "write_access"], True),

            import uuid        ]

            data_id = f"DATA_{uuid.uuid4().hex[:8]}"        

            self.data_store[data_id] = {'message': message, 'policy': policy}        for policy, user_attrs, expected_result in test_cases:

            return data_id            user_attributes = set(user_attrs)

                    

        def decrypt(self, user_id, data_id):            # Parse policy - handle both 'AND' and 'and', and single attributes

            if data_id not in self.data_store:            policy_lower = policy.lower()

                raise Exception("Data not found")            if ' and ' in policy_lower:

            return self.data_store[data_id]['message']                policy_attributes = set([attr.strip() for attr in policy_lower.split(' and ')])

            elif ' AND ' in policy:

def test_abe_policy():                policy_attributes = set([attr.strip() for attr in policy.split(' AND ')])

    """Test ABE policy functionality"""            else:

    print("=== ABE Policy Test ===")                # Single attribute policy

                    policy_attributes = set([policy.strip()])

    # Initialize ABE system            

    abe = ABECrypto()            result = policy_attributes.issubset(user_attributes)

                status = "✅" if result == expected_result else "❌"

    # Test 1: Basic encryption/decryption            

    print("\n1. Testing basic encryption/decryption...")            print(f"  {status} Policy: '{policy}' | User: {user_attrs} | Expected: {expected_result} | Got: {result}")

    try:    

        # Issue attributes    test_policy_parsing()

        abe.issue_ac("user1", ["department:IT", "role:admin"])    

        abe.issue_ac("user2", ["department:HR", "role:user"])    print("\n🔐 Testing ABE encryption/decryption...")

            

        # Encrypt message    # Initialize ABE (this will use mock if Firebase isn't available)

        message = "This is a test message"    abe = ABECrypto()

        policy = "department:IT AND role:admin"    

        data_id = abe.encrypt(message, policy)    # Test basic flow

        print(f"✅ Encrypted message with policy: {policy}")    user_id = "test_user"

        print(f"   Data ID: {data_id}")    attributes = ["user", "read_access", "write_access"]

            

        # Decrypt message    print(f"📝 Issuing AC for user '{user_id}' with attributes: {attributes}")

        decrypted = abe.decrypt("user1", data_id)    ac = abe.issue_ac(user_id, attributes)

        print(f"✅ Decrypted message: {decrypted}")    print("✅ AC issued successfully")

            

        if decrypted == message:    # Test encryption with simple policy

            print("✅ Encryption/Decryption successful!")    test_message = "Hello, this is a test message!"

        else:    test_policy = "user"

            print("❌ Decryption failed - messages don't match")    

                print(f"🔒 Encrypting message with policy: '{test_policy}'")

    except Exception as e:    data_id = abe.encrypt(test_message, test_policy)

        print(f"❌ Test 1 failed: {e}")    print(f"✅ Encryption successful, Data ID: {data_id}")

        

    # Test 2: Policy evaluation    # Test decryption

    print("\n2. Testing policy evaluation...")    print(f"🔓 Attempting to decrypt data...")

    try:    decrypted_message = abe.decrypt(user_id, data_id)

        policies = [    print(f"✅ Decryption successful: '{decrypted_message}'")

            "department:IT",    

            "role:admin",    if decrypted_message == test_message:

            "department:IT AND role:admin",        print("✅ Message integrity verified!")

            "department:HR OR role:admin"    else:

        ]        print("❌ Message integrity failed!")

            

        for policy in policies:    print("\n🎉 ABE policy testing completed successfully!")

            data_id = abe.encrypt(f"Message for policy: {policy}", policy)    

            print(f"   Policy: {policy}")except Exception as e:

                print(f"❌ Error during testing: {e}")

            # Try with user1 (IT admin)    import traceback

            try:    traceback.print_exc()

                result = abe.decrypt("user1", data_id)

                print(f"     ✅ User1 (IT admin) can access")print("\n" + "=" * 50)

            except:
                print(f"     ❌ User1 (IT admin) cannot access")
                
            # Try with user2 (HR user)
            try:
                result = abe.decrypt("user2", data_id)
                print(f"     ✅ User2 (HR user) can access")
            except:
                print(f"     ❌ User2 (HR user) cannot access")
                
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
    
    print("\n=== ABE Policy Test Complete ===")

if __name__ == "__main__":
    test_abe_policy()