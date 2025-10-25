# abe_crypto.py
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from firebase_utils import FirebaseUtils
from config import FIREBASE_CRED_PATH
import hashlib
import base64
import os

class ABECrypto:
    def __init__(self):
        self.firebase = FirebaseUtils(FIREBASE_CRED_PATH)
        # Load or generate master RSA key pair
        key_file = "master_key.pem"
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                self.master_key = RSA.import_key(f.read())
        else:
            self.master_key = RSA.generate(2048)
            with open(key_file, 'wb') as f:
                f.write(self.master_key.export_key())
        self.master_public_key = self.master_key.publickey()

    def issue_ac(self, user_id, attributes):
        # Generate user-specific RSA key pair
        user_key = RSA.generate(2048)
        user_public_key = user_key.publickey()
        
        # Encrypt user's private key with AES
        aes_key = get_random_bytes(32)  # 256-bit AES key
        iv = get_random_bytes(16)       # 128-bit IV
        cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
        padded_key = pad(user_key.export_key(), AES.block_size)
        encrypted_sk = cipher_aes.encrypt(padded_key)
        
        # Encrypt AES key with master's public key
        cipher_rsa = PKCS1_OAEP.new(self.master_public_key)
        encrypted_aes_key = cipher_rsa.encrypt(aes_key)
        
        # Combine encrypted key and IV for storage
        sk_data = {
            'encrypted_sk': base64.b64encode(encrypted_sk).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'encrypted_aes_key': base64.b64encode(encrypted_aes_key).decode('utf-8'),
            'public_key': base64.b64encode(user_public_key.export_key()).decode('utf-8')
        }
        
        # Create Access Credential (AC)
        udk = hashlib.sha256(str(user_key.export_key()).encode()).hexdigest()[:16]
        ac = {
            'user_id': user_id,
            'attributes': attributes,
            'udk': udk,
            'validity': '2025-12-31',
            'signature': hashlib.sha256(udk.encode()).hexdigest()
        }
        
        # Store in Firebase
        self.firebase.store_user(user_id, attributes, ac, sk_data)
        return ac

    def encrypt(self, message, policy):
        # Generate AES key and IV for data encryption
        aes_key = get_random_bytes(32)  # 256-bit key
        iv = get_random_bytes(16)       # 128-bit IV
        
        # Encrypt message with AES
        cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
        padded_message = pad(message.encode(), AES.block_size)
        encrypted_data = cipher_aes.encrypt(padded_message)
        
        # Encrypt AES key with master's public key
        cipher_rsa = PKCS1_OAEP.new(self.master_public_key)
        encrypted_key = cipher_rsa.encrypt(aes_key)
        
        # Generate data ID
        data_id = hashlib.sha256(message.encode()).hexdigest()
        
        # Store in Firebase
        self.firebase.store_data(
            data_id,
            base64.b64encode(encrypted_data).decode('utf-8'),
            base64.b64encode(iv).decode('utf-8'),
            base64.b64encode(encrypted_key).decode('utf-8'),
            policy
        )
        return data_id

    def decrypt(self, user_id, data_id):
        # Retrieve user data
        user_data = self.firebase.get_user(user_id)
        ac = user_data.get('ac')
        sk_data = user_data.get('encrypted_sk')
        
        # Verify AC
        if not ac or hashlib.sha256(ac['udk'].encode()).hexdigest() != ac['signature']:
            raise Exception("Invalid AC.")
        
        # Decrypt AES key for user's private key with master's private key
        cipher_rsa = PKCS1_OAEP.new(self.master_key)
        encrypted_aes_key = base64.b64decode(sk_data['encrypted_aes_key'])
        aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        
        # Decrypt user's private key with AES
        iv = base64.b64decode(sk_data['iv'])
        encrypted_sk = base64.b64decode(sk_data['encrypted_sk'])
        cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
        padded_key = cipher_aes.decrypt(encrypted_sk)
        user_private_key = RSA.import_key(unpad(padded_key, AES.block_size))
        
        # Retrieve encrypted data
        data = self.firebase.get_data(data_id)
        encrypted_data = base64.b64decode(data['encrypted_data'])
        iv = base64.b64decode(data['iv'])
        encrypted_key = base64.b64decode(data['encrypted_key'])
        policy = data['policy']
        
        # Check attributes against policy
        user_attributes = set(user_data['attributes'])
        
        # Improved policy evaluation
        if self._evaluate_policy(policy, user_attributes):
            print(f"DEBUG: Policy satisfied - User: {user_attributes}, Policy: {policy}")
        else:
            print(f"DEBUG: Policy NOT satisfied - User: {user_attributes}, Policy: {policy}")
            raise Exception(f"You do not have the required attributes to decrypt this data. Policy: '{policy}', Your attributes: {list(user_attributes)}")
        
        # Decrypt AES key with master's private key
        cipher_rsa = PKCS1_OAEP.new(self.master_key)
        aes_key = cipher_rsa.decrypt(encrypted_key)
        
        # Decrypt data with AES
        cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
        padded_message = cipher_aes.decrypt(encrypted_data)
        message = unpad(padded_message, AES.block_size)
        
        return message.decode()

    def delegate_key_update(self, user_id, new_attributes):
        return self.issue_ac(user_id, new_attributes)

    def revoke_attribute(self, user_id, attribute_to_revoke):
        user_data = self.firebase.get_user(user_id)
        current_attributes = user_data['attributes']
        if attribute_to_revoke not in current_attributes:
            raise Exception("Attribute not assigned.")
        
        updated_attributes = [attr for attr in current_attributes if attr != attribute_to_revoke]
        return self.delegate_key_update(user_id, updated_attributes)
    
    def _evaluate_policy(self, policy, user_attributes):
        """
        Enhanced policy evaluation that handles AND, OR, and parentheses
        Examples:
        - "admin" -> user must have 'admin'
        - "user AND read_access" -> user must have both 'user' and 'read_access'
        - "admin OR manager" -> user must have either 'admin' or 'manager'
        - "(admin OR manager) AND active" -> user must have ('admin' or 'manager') and 'active'
        """
        import re
        
        # Clean up the policy string
        policy = policy.strip()
        
        # Handle simple single attribute case
        if not any(op in policy.upper() for op in [' AND ', ' OR ', '(', ')']):
            return policy.strip() in user_attributes
        
        # Replace attribute names with True/False based on user attributes
        def replace_attributes(match):
            attr = match.group(0).strip()
            return 'True' if attr in user_attributes else 'False'
        
        # Find all attribute names (sequences of word characters, digits, and underscores)
        # that are not Python keywords (AND, OR, True, False)
        attribute_pattern = r'\b(?!(?:AND|OR|True|False|and|or)\b)[a-zA-Z_][a-zA-Z0-9_]*\b'
        
        # Convert policy to uppercase for consistency
        policy_upper = policy.upper()
        
        # Replace AND/OR with Python operators
        policy_upper = policy_upper.replace(' AND ', ' and ')
        policy_upper = policy_upper.replace(' OR ', ' or ')
        
        # Find and replace attribute names with boolean values
        attributes_found = re.findall(attribute_pattern, policy_upper)
        
        # Create a copy for evaluation
        eval_policy = policy_upper
        
        # Replace each attribute with its boolean value
        for attr in set(attributes_found):  # Use set to avoid duplicate replacements
            if attr.upper() not in ['AND', 'OR', 'TRUE', 'FALSE']:
                # Use word boundaries to ensure exact matches
                attr_pattern = r'\b' + re.escape(attr) + r'\b'
                replacement = 'True' if attr in user_attributes else 'False'
                eval_policy = re.sub(attr_pattern, replacement, eval_policy, flags=re.IGNORECASE)
        
        print(f"DEBUG: Original policy: {policy}")
        print(f"DEBUG: Evaluation policy: {eval_policy}")
        print(f"DEBUG: User attributes: {user_attributes}")
        
        try:
            # Safely evaluate the boolean expression
            result = eval(eval_policy)
            print(f"DEBUG: Policy evaluation result: {result}")
            return result
        except Exception as e:
            print(f"DEBUG: Error evaluating policy '{policy}': {e}")
            # Fallback to simple attribute check
            return policy.strip() in user_attributes