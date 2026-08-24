#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONZ XTER LOGIN SYSTEM - PREMIUM EDITION v2.0
Multi-level authentication with EXPIRY DATE
User: 14 days | Premium: 30 days | Admin: Forever
"""

import os
import json
import hashlib
import getpass
import secrets
import string
from datetime import datetime, timedelta
from colorama import Fore, init

init(autoreset=True)

class LoginSystem:
    def __init__(self, user_file="data/users.json"):
        self.user_file = user_file
        self.current_user = None
        self.session = {}
        self.users = self.load_users()
    
    def load_users(self):
        """Load users from file"""
        if os.path.exists(self.user_file):
            try:
                with open(self.user_file, "r") as f:
                    return json.load(f)
            except:
                return self.create_default_users()
        else:
            return self.create_default_users()
    
    def create_default_users(self):
        """Create default users with COMPLEX passwords & EXPIRY"""
        os.makedirs(os.path.dirname(self.user_file), exist_ok=True)
        
        default_users = {
            "MonzXter_Admin": {
                "password": self.hash_password("Monz@2090#Secure!Xyz"),
                "role": "admin",
                "created": datetime.now().isoformat(),
                "last_login": None,
                "status": "active",
                "expiry": None  # Admin forever
            },
            "Xter_User_Pro": {
                "password": self.hash_password("Us3r#Monz@2026!Xyz#Secure"),
                "role": "user",
                "created": datetime.now().isoformat(),
                "last_login": None,
                "status": "active",
                "expiry": (datetime.now() + timedelta(days=14)).isoformat()  # 14 days
            },
            "Premium_Xter_Elite": {
                "password": self.hash_password("Pr3m!um@Monz@#2090$Xter$Elite"),
                "role": "premium",
                "created": datetime.now().isoformat(),
                "last_login": None,
                "status": "active",
                "expiry": (datetime.now() + timedelta(days=30)).isoformat()  # 30 days
            }
        }
        
        with open(self.user_file, "w") as f:
            json.dump(default_users, f, indent=2)
        return default_users
    
    def save_users(self):
        """Save users to file"""
        with open(self.user_file, "w") as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password):
        """Hash password using SHA256 with salt"""
        salt = "MonzXter_Salt_2090#Secure"
        return hashlib.sha256((salt + password + salt[::-1]).encode()).hexdigest()
    
    def generate_secure_password(self, length=16):
        """Generate secure random password"""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def generate_username(self, role="user"):
        """Generate username based on role"""
        prefix = {
            "admin": "Admin",
            "premium": "Premium",
            "user": "User"
        }
        random_suffix = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        return f"{prefix.get(role, 'User')}_{random_suffix}"
    
    def check_expiry(self, username):
        """Check if user account has expired"""
        if username not in self.users:
            return False, "User tidak ditemukan!"
        
        user = self.users[username]
        
        # Admin never expires
        if user["role"] == "admin":
            return True, "Akun aktif (admin forever)"
        
        expiry = user.get("expiry")
        if not expiry:
            return True, "Akun aktif (no expiry)"
        
        try:
            expiry_date = datetime.fromisoformat(expiry)
            if datetime.now() > expiry_date:
                return False, f"Akun telah kadaluarsa! Expiry: {expiry_date.strftime('%Y-%m-%d %H:%M')}"
            else:
                days_left = (expiry_date - datetime.now()).days
                hours_left = (expiry_date - datetime.now()).seconds // 3600
                return True, f"Akun aktif. Sisa {days_left} hari {hours_left} jam"
        except:
            return True, "Akun aktif"
    
    def login(self, username, password):
        """Login user with expiry check"""
        if username not in self.users:
            return False, "❌ User tidak ditemukan!", None
        
        user = self.users[username]
        
        # Check if user is active
        if user.get("status") != "active":
            return False, "❌ Akun telah dinonaktifkan!", None
        
        # Check expiry
        is_valid, expiry_msg = self.check_expiry(username)
        if not is_valid:
            return False, f"❌ {expiry_msg}", None
        
        # Check password
        if user["password"] != self.hash_password(password):
            return False, "❌ Password salah!", None
        
        # Update last login
        user["last_login"] = datetime.now().isoformat()
        self.save_users()
        
        # Set session
        self.current_user = username
        self.session = {
            "username": username,
            "role": user["role"],
            "login_time": datetime.now().isoformat(),
            "expiry": (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        return True, f"✅ Login berhasil!\n📊 User: {username}\n👑 Role: {user['role']}\n📅 {expiry_msg}", user
    
    def logout(self):
        """Logout user"""
        self.current_user = None
        self.session = {}
        return True, "✅ Logout berhasil!"
    
    def is_logged_in(self):
        """Check if user is logged in"""
        if not self.session:
            return False
        
        # Check session expiry
        expiry = datetime.fromisoformat(self.session.get("expiry", datetime.now().isoformat()))
        if datetime.now() > expiry:
            self.logout()
            return False
        
        return True
    
    def get_current_user(self):
        """Get current logged in user"""
        return self.current_user
    
    def get_user_role(self):
        """Get user role"""
        if self.current_user and self.current_user in self.users:
            return self.users[self.current_user].get("role", "user")
        return None
    
    def get_user_expiry(self):
        """Get user expiry date"""
        if self.current_user and self.current_user in self.users:
            expiry = self.users[self.current_user].get("expiry")
            if expiry:
                try:
                    return datetime.fromisoformat(expiry)
                except:
                    return None
        return None
    
    def is_admin(self):
        """Check if current user is admin"""
        return self.get_user_role() == "admin"
    
    def is_premium(self):
        """Check if current user is premium"""
        return self.get_user_role() in ["admin", "premium"]
    
    def check_permission(self, required_role="user"):
        """Check if user has required permission"""
        role_order = ["user", "premium", "admin"]
        current_role = self.get_user_role()
        
        if not current_role:
            return False
        
        if current_role not in role_order:
            return False
        
        if required_role not in role_order:
            return False
        
        return role_order.index(current_role) >= role_order.index(required_role)
    
    def add_user(self, username, password, role="user", days=14):
        """Add new user with expiry"""
        if username in self.users:
            return False, "❌ Username sudah ada!"
        
        if role not in ["user", "premium", "admin"]:
            role = "user"
        
        expiry_days = None
        if role == "user":
            expiry_days = 14
        elif role == "premium":
            expiry_days = 30
        else:
            expiry_days = None  # Admin forever
        
        self.users[username] = {
            "password": self.hash_password(password),
            "role": role,
            "created": datetime.now().isoformat(),
            "last_login": None,
            "status": "active",
            "expiry": (datetime.now() + timedelta(days=expiry_days)).isoformat() if expiry_days else None
        }
        self.save_users()
        return True, f"✅ User {username} berhasil ditambahkan! (Expiry: {expiry_days} hari)" if expiry_days else f"✅ User {username} berhasil ditambahkan! (Admin Forever)"
    
    def delete_user(self, username):
        """Delete user"""
        if username not in self.users:
            return False, "❌ User tidak ditemukan!"
        
        if username == "MonzXter_Admin":
            return False, "❌ Tidak bisa menghapus admin utama!"
        
        if username == self.current_user:
            return False, "❌ Tidak bisa menghapus diri sendiri!"
        
        del self.users[username]
        self.save_users()
        return True, f"✅ User {username} berhasil dihapus!"
    
    def list_users(self):
        """List all users with expiry info"""
        print(Fore.CYAN + "\n" + "="*75)
        print(Fore.CYAN + "📊 DAFTAR USER")
        print(Fore.CYAN + "="*75)
        print(Fore.WHITE + f"{'Username':<20} {'Role':<10} {'Status':<10} {'Expiry':<20} {'Last Login':<20}")
        print(Fore.CYAN + "-"*75)
        
        for username, data in self.users.items():
            status = data.get("status", "active")
            status_color = Fore.GREEN if status == "active" else Fore.RED
            role_color = Fore.MAGENTA if data["role"] == "admin" else (Fore.YELLOW if data["role"] == "premium" else Fore.CYAN)
            
            # Expiry
            expiry = data.get("expiry")
            if expiry:
                try:
                    expiry_date = datetime.fromisoformat(expiry)
                    days_left = (expiry_date - datetime.now()).days
                    if days_left < 0:
                        expiry_display = Fore.RED + "EXPIRED"
                    elif days_left < 3:
                        expiry_display = Fore.YELLOW + f"{days_left}d left"
                    else:
                        expiry_display = Fore.GREEN + f"{days_left}d left"
                except:
                    expiry_display = Fore.WHITE + "N/A"
            else:
                expiry_display = Fore.MAGENTA + "FOREVER"
            
            # Last login
            last_login = data.get("last_login", "Never")
            if last_login and last_login != "Never":
                last_login = last_login[:19]
            else:
                last_login = "Never"
            
            print(f"{Fore.WHITE}{username:<20} {role_color}{data['role']:<10} {status_color}{status:<10} {expiry_display:<20} {Fore.YELLOW}{last_login:<20}")
        
        print(Fore.CYAN + "="*75)
    
    def change_password(self, username, old_password, new_password):
        """Change user password"""
        if username not in self.users:
            return False, "❌ User tidak ditemukan!"
        
        if self.users[username]["password"] != self.hash_password(old_password):
            return False, "❌ Password lama salah!"
        
        if len(new_password) < 8:
            return False, "❌ Password minimal 8 karakter!"
        
        self.users[username]["password"] = self.hash_password(new_password)
        self.save_users()
        return True, "✅ Password berhasil diubah!"
    
    def toggle_user_status(self, username):
        """Activate/deactivate user"""
        if username not in self.users:
            return False, "❌ User tidak ditemukan!"
        
        if username == "MonzXter_Admin":
            return False, "❌ Tidak bisa menonaktifkan admin utama!"
        
        current_status = self.users[username].get("status", "active")
        new_status = "inactive" if current_status == "active" else "active"
        self.users[username]["status"] = new_status
        self.save_users()
        return True, f"✅ User {username} status: {new_status}!"
    
    def extend_expiry(self, username, extra_days):
        """Extend user expiry"""
        if username not in self.users:
            return False, "❌ User tidak ditemukan!"
        
        user = self.users[username]
        
        if user["role"] == "admin":
            return False, "❌ Admin tidak punya expiry!"
        
        current_expiry = user.get("expiry")
        if current_expiry:
            try:
                expiry_date = datetime.fromisoformat(current_expiry)
                new_expiry = expiry_date + timedelta(days=extra_days)
            except:
                new_expiry = datetime.now() + timedelta(days=extra_days)
        else:
            new_expiry = datetime.now() + timedelta(days=extra_days)
        
        user["expiry"] = new_expiry.isoformat()
        self.save_users()
        return True, f"✅ Expiry diperpanjang {extra_days} hari! (Baru: {new_expiry.strftime('%Y-%m-%d %H:%M')})"
    
    def login_prompt(self):
        """Display login prompt with enhanced security"""
        print(Fore.CYAN + """
╔══════════════════════════════════════════════════════════════╗
║  🔐 MONZ XTER LOGIN SYSTEM v2.0                            ║
║  PREMIUM AUTHENTICATION WITH EXPIRY                       ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        print(Fore.YELLOW + "\n[!] Login Required!")
        print(Fore.WHITE + "-"*60)
        print(Fore.CYAN + "📌 User: 14 days expiry")
        print(Fore.CYAN + "📌 Premium: 30 days expiry")
        print(Fore.CYAN + "📌 Admin: Forever")
        print(Fore.WHITE + "-"*60)
        
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            username = input(Fore.CYAN + "\n[+] Username: ").strip()
            password = getpass.getpass(Fore.CYAN + "[+] Password: ").strip()
            
            success, message, user_data = self.login(username, password)
            
            if success:
                print(Fore.GREEN + f"\n{message}")
                return True
            else:
                attempts += 1
                print(Fore.RED + f"\n{message} (Attempt {attempts}/{max_attempts})")
        
        print(Fore.RED + "\n❌ Terlalu banyak percobaan! Program berhenti.")
        return False
    
    def user_menu(self):
        """User management menu (for admin)"""
        if not self.is_admin():
            print(Fore.RED + "❌ Akses ditolak! Hanya admin!")
            return
        
        while True:
            print(Fore.YELLOW + "\n[👥] USER MANAGEMENT")
            print(Fore.WHITE + "="*60)
            print(Fore.CYAN + """
┌─────────────────────────────────────────────────────────────┐
│  [L] List users    [A] Add user    [D] Delete user       │
│  [P] Change pass   [S] Toggle status  [E] Extend expiry  │
│  [G] Generate user [X] Exit                              │
└─────────────────────────────────────────────────────────────┘
            """)
            
            choice = input(Fore.CYAN + "┌─[USER-MGR]─[~]\n└──╼ $ ").strip().lower()
            
            if choice == "l":
                self.list_users()
            
            elif choice == "a":
                username = input(Fore.CYAN + "[+] New username: ").strip()
                password = input(Fore.CYAN + "[+] Password (min 8 chars): ").strip()
                role = input(Fore.CYAN + "[+] Role (user/premium/admin): ").strip().lower()
                if role not in ["user", "premium", "admin"]:
                    role = "user"
                success, msg = self.add_user(username, password, role)
                print(Fore.GREEN if success else Fore.RED + msg)
            
            elif choice == "d":
                username = input(Fore.CYAN + "[+] Username to delete: ").strip()
                success, msg = self.delete_user(username)
                print(Fore.GREEN if success else Fore.RED + msg)
            
            elif choice == "p":
                username = input(Fore.CYAN + "[+] Username: ").strip()
                old_pass = getpass.getpass(Fore.CYAN + "[+] Old password: ").strip()
                new_pass = getpass.getpass(Fore.CYAN + "[+] New password (min 8 chars): ").strip()
                success, msg = self.change_password(username, old_pass, new_pass)
                print(Fore.GREEN if success else Fore.RED + msg)
            
            elif choice == "s":
                username = input(Fore.CYAN + "[+] Username to toggle: ").strip()
                success, msg = self.toggle_user_status(username)
                print(Fore.GREEN if success else Fore.RED + msg)
            
            elif choice == "e":
                username = input(Fore.CYAN + "[+] Username: ").strip()
                days = int(input(Fore.CYAN + "[+] Extra days: ").strip())
                success, msg = self.extend_expiry(username, days)
                print(Fore.GREEN if success else Fore.RED + msg)
            
            elif choice == "g":
                role = input(Fore.CYAN + "[+] Role (user/premium): ").strip().lower()
                if role not in ["user", "premium"]:
                    role = "user"
                username = self.generate_username(role)
                password = self.generate_secure_password(16)
                days = 14 if role == "user" else 30
                success, msg = self.add_user(username, password, role, days)
                if success:
                    print(Fore.GREEN + f"✅ Username: {username}")
                    print(Fore.GREEN + f"✅ Password: {password}")
                    print(Fore.YELLOW + f"📅 Expiry: {days} hari")
                else:
                    print(Fore.RED + msg)
            
            elif choice == "x":
                break
            
            else:
                print(Fore.RED + "❌ Invalid choice!")
            
            input(Fore.CYAN + "\n[+] Press Enter to continue...")

# ================================================================
# TESTING
# ================================================================

if __name__ == "__main__":
    login = LoginSystem()
    if login.login_prompt():
        print(Fore.GREEN + f"\n✅ Logged in as: {login.get_current_user()}")
        print(Fore.CYAN + f"👑 Role: {login.get_user_role()}")
        
        # Show expiry info
        expiry = login.get_user_expiry()
        if expiry:
            days_left = (expiry - datetime.now()).days
            print(Fore.YELLOW + f"📅 Expiry: {expiry.strftime('%Y-%m-%d %H:%M')} ({days_left} days left)")
        else:
            print(Fore.MAGENTA + "📅 Expiry: FOREVER (Admin)")
        
        # Show user menu if admin
        if login.is_admin():
            login.user_menu()
