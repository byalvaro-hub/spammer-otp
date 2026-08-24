#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONZ XTER UTILITIES - PROXY & LOGGER
"""

import random
import os
import json
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

class ProxyManager:
    def __init__(self, file_path="data/proxies.txt"):
        self.file_path = file_path
        self.proxies = self.load()
    
    def load(self):
        """Load proxies from file"""
        proxies = []
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                proxies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        # Convert to dict format
        self.proxy_dicts = []
        for p in proxies:
            if p.startswith("http://") or p.startswith("https://"):
                self.proxy_dicts.append({"http": p, "https": p})
            elif p.startswith("socks5://"):
                self.proxy_dicts.append({"http": p, "https": p})
            else:
                self.proxy_dicts.append({"http": f"http://{p}", "https": f"http://{p}"})
        
        return self.proxy_dicts
    
    def get_random(self):
        """Get random proxy"""
        if not self.proxy_dicts:
            return None
        return random.choice(self.proxy_dicts)
    
    def get_all(self):
        """Get all proxies"""
        return self.proxy_dicts

class Logger:
    def __init__(self, log_file="logs/activity.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    def log(self, level, message):
        """Log message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] [{level}] {message}"
        
        with open(self.log_file, "a") as f:
            f.write(entry + "\n")
    
    def info(self, message):
        self.log("INFO", message)
    
    def error(self, message):
        self.log("ERROR", message)
    
    def warning(self, message):
        self.log("WARNING", message)
    
    def debug(self, message):
        self.log("DEBUG", message)
    
    def show_last(self, lines=20):
        """Show last n log lines"""
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                all_lines = f.readlines()
                for line in all_lines[-lines:]:
                    print(Fore.WHITE + line.strip())
        else:
            print(Fore.RED + "[✗] No log file found")
    
    def clear(self):
        """Clear log file"""
        if os.path.exists(self.log_file):
            os.remove(self.log_file)