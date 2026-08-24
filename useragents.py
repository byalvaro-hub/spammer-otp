#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONZ XTER USER-AGENT MANAGER
"""

import random
import os

class UAManager:
    def __init__(self, file_path="data/useragents.txt"):
        self.file_path = file_path
        self.agents = self.load()
    
    def load(self):
        """Load user-agents from file"""
        agents = []
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                agents = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        
        # Fallback defaults
        if not agents:
            agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Android 12; Mobile; rv:68.0) Gecko/68.0 Firefox/115.0",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
                "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 Chrome/118.0.0.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0"
            ]
        
        return agents
    
    def get_random(self):
        """Get random user-agent"""
        return random.choice(self.agents)
    
    def get_all(self):
        """Get all user-agents"""
        return self.agents