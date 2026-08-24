#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONZ XTER OTP SPAMMER PRO v3.0
PREMIUM UNRESTRICTED EDITION
© 2090 MONZ XTER LABS
"""

import sys
import os
import time
import json
from datetime import datetime
from colorama import Fore, init, Style
from login import LoginSystem
from main_engine import MainEngine
from targets import TargetManager

init(autoreset=True)

class MonzXterPro:
    def __init__(self):
        self.version = "3.0.0"
        self.login = LoginSystem()
        self.engine = MainEngine()
        self.target_manager = TargetManager()
        self.config = self.load_config()
        
    def load_config(self):
        """Load config from file"""
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                return json.load(f)
        return {}
        
    def banner(self):
        os.system("clear" if os.name == "posix" else "cls")
        print(Fore.CYAN + """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ███╗   ███╗ ██████╗ ███╗   ██╗███████╗                  ║
║   ████╗ ████║██╔═══██╗████╗  ██║╚══███╔╝                  ║
║   ██╔████╔██║██║   ██║██╔██╗ ██║  ███╔╝                   ║
║   ██║╚██╔╝██║██║   ██║██║╚██╗██║ ███╔╝                    ║
║   ██║ ╚═╝ ██║╚██████╔╝██║ ╚████║███████╗                  ║
║   ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝                  ║
║                                                              ║
║   ╔═══════════════════════════════════════════════════════╗ ║
║   ║  OTP SPAMMER PRO - UNRESTRICTED EDITION             ║ ║
║   ║  VERSION: 3.0.0                                    ║ ║
║   ║  LICENSE: PREMIUM                                 ║ ║
║   ║  STATUS: ACTIVE                                  ║ ║
║   ║  OWNER: MONZ XTER                               ║ ║
║   ║  YEAR: 2090 - ∞                               ║ ║
║   ╚═══════════════════════════════════════════════════╝ ║
║                                                              ║
║   "NO FILTER - NO SENSOR - NO LIMITS"                       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        if self.login.is_logged_in():
            user = self.login.get_current_user()
            role = self.login.get_user_role()
            
            # Get expiry info
            expiry = self.login.get_user_expiry()
            if expiry:
                days_left = (expiry - datetime.now()).days
                if days_left < 0:
                    expiry_display = Fore.RED + "EXPIRED!"
                elif days_left < 3:
                    expiry_display = Fore.YELLOW + f"{days_left} days left"
                else:
                    expiry_display = Fore.GREEN + f"{days_left} days left"
            else:
                expiry_display = Fore.MAGENTA + "FOREVER (Admin)"
            
            print(Fore.GREEN + f"\n✅ Logged in as: {user} ({role})")
            print(Fore.YELLOW + f"📅 {expiry_display}")
        else:
            print(Fore.RED + "\n❌ Not logged in!")
        
        print(Fore.CYAN + "="*60 + "\n")
    
    def menu(self):
        print(Fore.WHITE + """
╔══════════════════════════════════════════════════════════════╗
║  📋 PREMIUM MENU                                           ║
╠══════════════════════════════════════════════════════════════╣
║  1. 🚀 START SPAM (Manual Input)                          ║
║  2. 📂 START SPAM (Batch from File)                      ║
║  3. ⚙️  CONFIGURATION                                    ║
║  4. 📊 TARGET MANAGER                                   ║
║  5. 🔄 PROXY MANAGER                                   ║
║  6. 📝 VIEW LOGS                                      ║
║  7. 👥 USER MANAGEMENT (Admin Only)                  ║
║  8. 🔐 LOGOUT                                        ║
║  9. ❌ EXIT                                         ║
╚══════════════════════════════════════════════════════════════╝
        """)
        return input(Fore.CYAN + "┌─[MONZ@XTER]─[~]\n└──╼ $ ").strip()
    
    def start_spam_manual(self):
        if not self.login.check_permission("user"):
            print(Fore.RED + "❌ Akses ditolak! Login terlebih dahulu!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return
        
        print(Fore.YELLOW + "\n[⚡] MANUAL TARGET INPUT")
        print(Fore.WHITE + "="*60)
        
        targets = self.target_manager.get_targets()
        if targets:
            print(Fore.GREEN + f"[✓] Loaded {len(targets)} targets from file")
        
        print(Fore.CYAN + "\nFormat: 628xxxxxxxxxx (Indonesia)")
        print(Fore.CYAN + "Type 'done' to finish, 'file' to load from file\n")
        
        new_targets = []
        while True:
            phone = input(Fore.CYAN + "[+] Target: ").strip()
            if phone.lower() == "done":
                break
            if phone.lower() == "file":
                targets = self.target_manager.load_from_file()
                if targets:
                    new_targets.extend(targets)
                    print(Fore.GREEN + f"[✓] Added {len(targets)} from file!")
                continue
            phone = self.target_manager.validate_phone(phone)
            if phone:
                new_targets.append(phone)
                print(Fore.GREEN + f"[✓] Added: {phone}")
            else:
                print(Fore.RED + "[✗] Invalid number!")
        
        if new_targets:
            print(Fore.WHITE + "\n" + "="*60)
            print(Fore.GREEN + f"[✓] Total targets: {len(new_targets)}")
            confirm = input(Fore.YELLOW + "\n[!] Start spam? (y/n): ").strip().lower()
            if confirm == "y":
                self.engine.run(new_targets)
        else:
            print(Fore.RED + "[✗] No targets added!")
        
        input(Fore.CYAN + "\n[+] Press Enter to continue...")
    
    def start_spam_batch(self):
        if not self.login.check_permission("user"):
            print(Fore.RED + "❌ Akses ditolak! Login terlebih dahulu!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return
        
        print(Fore.YELLOW + "\n[📂] BATCH MODE")
        print(Fore.WHITE + "="*60)
        
        targets = self.target_manager.load_from_file()
        if targets:
            print(Fore.GREEN + f"[✓] Loaded {len(targets)} targets")
            self.engine.run(targets)
        else:
            print(Fore.RED + "[✗] No targets found!")
        
        input(Fore.CYAN + "\n[+] Press Enter to continue...")
    
    def show_config(self):
        if not self.login.check_permission("user"):
            print(Fore.RED + "❌ Akses ditolak! Login terlebih dahulu!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return
        
        print(Fore.YELLOW + "\n[⚙️] CURRENT CONFIGURATION")
        print(Fore.WHITE + "="*60)
        self.engine.show_config()
        input(Fore.CYAN + "\n[+] Press Enter to continue...")
    
    def target_manager(self):
        if not self.login.check_permission("user"):
            print(Fore.RED + "❌ Akses ditolak! Login terlebih dahulu!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return
        
        self.target_manager.manage()
    
    def proxy_manager(self):
        if not self.login.check_permission("user"):
            print(Fore.RED + "❌ Akses ditolak! Login terlebih dahulu!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return
        
        print(Fore.YELLOW + "\n[🔄] PROXY MANAGER")
        print(Fore.WHITE + "="*60)
        self.engine.show_proxies()
        input(Fore.CYAN + "\n[+] Press Enter to continue...")
    
    def view_logs(self):
        if not self.login.check_permission("user"):
            print(Fore.RED + "❌ Akses ditolak! Login terlebih dahulu!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return
        
        print(Fore.YELLOW + "\n[📝] VIEW LOGS")
        print(Fore.WHITE + "="*60)
        self.engine.show_logs()
        input(Fore.CYAN + "\n[+] Press Enter to continue...")
    
    def user_management(self):
        if not self.login.is_admin():
            print(Fore.RED + "❌ Akses ditolak! Hanya admin!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return
        
        self.login.user_menu()
    
    def logout(self):
        if self.login.is_logged_in():
            self.login.logout()
            print(Fore.GREEN + "✅ Logout berhasil!")
        else:
            print(Fore.YELLOW + "⚠️ Tidak ada user yang login!")
        input(Fore.CYAN + "\n[+] Press Enter to continue...")
    
    def run(self):
        # Login first
        if not self.login.login_prompt():
            sys.exit(1)
        
        while True:
            self.banner()
            choice = self.menu()
            
            if choice == "1":
                self.start_spam_manual()
            elif choice == "2":
                self.start_spam_batch()
            elif choice == "3":
                self.show_config()
            elif choice == "4":
                self.target_manager()
            elif choice == "5":
                self.proxy_manager()
            elif choice == "6":
                self.view_logs()
            elif choice == "7":
                self.user_management()
            elif choice == "8":
                self.logout()
                if not self.login.login_prompt():
                    sys.exit(1)
            elif choice == "9":
                print(Fore.RED + "\n❌ Exiting...")
                print(Fore.CYAN + "© 2090 MONZ XTER LABS")
                sys.exit(0)
            else:
                print(Fore.RED + "❌ Invalid choice!")

if __name__ == "__main__":
    app = MonzXterPro()
    app.run()
