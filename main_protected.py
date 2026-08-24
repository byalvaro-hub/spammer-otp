#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONZ XTER PROTECTED ENGINE - WITH LICENSE CHECK
"""

import sys
import os
import hashlib
import base64
from cryptography.fernet import Fernet
from colorama import Fore, init
from license import LicenseChecker

init(autoreset=True)

class ProtectedEngine:
    def __init__(self):
        self.license = LicenseChecker()
        self.key = self.generate_key()
    
    def generate_key(self):
        """Generate encryption key from license"""
        license_key = self.license.get_key()
        return hashlib.sha256(license_key.encode()).digest()
    
    def verify_integrity(self):
        """Verify script integrity"""
        script_hash = hashlib.md5(open(__file__, 'rb').read()).hexdigest()
        stored_hash = self.load_stored_hash()
        return script_hash == stored_hash
    
    def load_stored_hash(self):
        try:
            with open(".hash", "r") as f:
                return f.read().strip()
        except:
            return ""
    
    def run(self):
        print(Fore.YELLOW + "\n[🛡️] PROTECTED MODE ACTIVATED")
        print(Fore.WHITE + "="*60)
        
        if not self.license.check():
            print(Fore.RED + "[✗] Invalid license!")
            return
        
        if not self.verify_integrity():
            print(Fore.RED + "[✗] Script integrity check failed!")
            return
        
        print(Fore.GREEN + "[✓] All checks passed!")
        print(Fore.CYAN + "[✓] Running protected spam engine...")
        
        # Protected spam logic here
        self.protected_spam()
    
    def protected_spam(self):
        print(Fore.GREEN + "\n[✓] Protected spam engine running...")
        # Your protected spam code here