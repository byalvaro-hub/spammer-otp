#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONZ XTER PROTECTED SCRIPT - OBFUSCATED VERSION
"""

import base64
import hashlib
import os
from cryptography.fernet import Fernet

class ProtectedScript:
    def __init__(self):
        self.key = self.get_key()
        self.cipher = Fernet(self.key)
    
    def get_key(self):
        # Generate key from environment
        env_key = os.environ.get("MONZ_KEY", "default_key_12345")
        return hashlib.sha256(env_key.encode()).digest()
    
    def decrypt_code(self, encrypted_code):
        try:
            return self.cipher.decrypt(encrypted_code.encode()).decode()
        except:
            return None
    
    def verify_hash(self, code):
        expected_hash = "a1b2c3d4e5f6g7h8i9j0"
        actual_hash = hashlib.md5(code.encode()).hexdigest()[:20]
        return actual_hash == expected_hash
    
    def run_protected(self):
        """Main protected function"""
        print("[🔒] Running protected script...")
        # Protected code here
        
if __name__ == "__main__":
    script = ProtectedScript()
    script.run_protected()