#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONZ XTER HANDLERS - REQUEST HANDLING
"""

import requests
import time
import random
from colorama import Fore, init
from handlers_plain import send_otp_plain
from useragents import UAManager
from utilitas import ProxyManager

init(autoreset=True)

class SpamHandler:
    def __init__(self, config):
        self.config = config
        self.ua_manager = UAManager()
        self.proxy_manager = ProxyManager()
    
    def send_otp(self, target, endpoint, retry=3, timeout=5):
        """Send OTP with retry logic"""
        for attempt in range(retry):
            ua = self.ua_manager.get_random() if self.config.get('ua_enabled', True) else None
            proxy = self.proxy_manager.get_random() if self.config.get('proxy_enabled', True) else None
            
            result = send_otp_plain(target, endpoint, ua, proxy, timeout)
            
            if result:
                print(Fore.GREEN + f"[✓] {target} - OTP sent!")
                return True
            else:
                print(Fore.YELLOW + f"[⚠] {target} - Retry {attempt+1}/{retry}")
                time.sleep(1)
        
        print(Fore.RED + f"[✗] {target} - Failed after {retry} attempts")
        return False