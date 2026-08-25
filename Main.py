#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONZ XTER OTP SPAMMER PRO v3.0
PREMIUM UNRESTRICTED EDITION
© 2090 MONZ XTER LABS
"""

import sys
import os
import json
from datetime import datetime
from colorama import Fore, init, Style

from login import LoginSystem
from main_engine import MainEngine
from targets import TargetManager

# Inisialisasi colorama
init(autoreset=True)

class MonzXterPro:
    def __init__(self):
        self.version = "3.0.0"
        self.login = LoginSystem()
        self.engine = MainEngine()
        self.target_manager = TargetManager()
        self.config = self.load_config()

    def load_config(self):
        """Load konfigurasi dari file config.json"""
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def banner(self):
        """Tampilkan banner utama"""
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
            print(Fore.GREEN + f"\n✅ Logged in as: {user} ({role})")
        else:
            print(Fore.RED + "\n❌ Not logged in!")

        print(Fore.CYAN + "="*60 + "\n")

    def menu(self):
        """Tampilkan menu utama"""
        print(Fore.WHITE + """
╔══════════════════════════════════════════════════════════════╗
║  📋 PREMIUM MENU                                           ║
╠══════════════════════════════════════════════════════════════╣
║  1. 🚀 START SPAM (Manual Input)                          ║
║  2. 📂 START SPAM (Batch from File)                      ║
║  3. ⚙️  CONFIGURATION                                    ║
║  4. 📊 TARGET MANAGER                                   ║
║  5. 📱 CEK STATUS WHATSAPP                             ║
║  6. 🔄 PROXY MANAGER                                   ║
║  7. 📝 VIEW LOGS                                      ║
║  8. 👥 USER MANAGEMENT (Admin Only)                  ║
║  9. 🔐 LOGOUT                                        ║
║  10. ❌ EXIT                                         ║
╚══════════════════════════════════════════════════════════════╝
        """)
        return input(Fore.CYAN + "┌─[MONZ@XTER]─[~]\n└──╼ $ ").strip()

    # ============================================================
    # FITUR 1: START SPAM MANUAL
    # ============================================================
    def start_spam_manual(self):
        """Input target manual dan jalankan spam"""
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

    # ============================================================
    # FITUR 2: START SPAM BATCH
    # ============================================================
    def start_spam_batch(self):
        """Jalankan spam dari file batch.txt"""
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

    # ============================================================
    # FITUR 3: LIHAT KONFIGURASI
    # ============================================================
    def show_config(self):
        """Tampilkan konfigurasi saat ini"""
        if not self.login.check_permission("user"):
            print(Fore.RED + "❌ Akses ditolak! Login terlebih dahulu!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return

        print(Fore.YELLOW + "\n[⚙️] CURRENT CONFIGURATION")
        print(Fore.WHITE + "="*60)
        print(json.dumps(self.config, indent=4))
        input(Fore.CYAN + "\n[+] Press Enter to continue...")

    # ============================================================
    # FITUR 4: TARGET MANAGER
    # ============================================================
    def target_manager(self):
        """Manajemen target (tambah/hapus/lihat)"""
        if not self.login.check_permission("user"):
            print(Fore.RED + "❌ Akses ditolak! Login terlebih dahulu!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return

        self.target_manager.manage()

    # ============================================================
    # FITUR 5: CEK STATUS WHATSAPP
    # ============================================================
    def check_whatsapp_status(self):
        """Cek status nomor WhatsApp menggunakan API kyuurzy.dev"""
        if not self.login.check_permission("user"):
            print(Fore.RED + "❌ Akses ditolak! Login terlebih dahulu!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return

        print(Fore.YELLOW + "\n[📱] CEK STATUS WHATSAPP")
        print(Fore.WHITE + "="*60)
        print(Fore.CYAN + "Masukkan nomor telepon untuk cek status WhatsApp\n")

        while True:
            phone = input(Fore.CYAN + "[+] Nomor (atau 'exit' untuk keluar): ").strip()
            if phone.lower() == "exit":
                break

            from utils import check_whatsapp_number
            result = check_whatsapp_number(phone)

            if "error" in result:
                print(Fore.RED + f"❌ {result['error']}")
            else:
                data = result.get("data", {})
                print(Fore.GREEN + "\n✅ HASIL CEK STATUS:")
                print(Fore.WHITE + "-"*50)
                print(f"📱 Nomor: {data.get('phone', 'N/A')}")
                print(f"🔒 Status: {data.get('status', 'N/A')}")
                print(f"🚫 Terblokir: {'Ya' if data.get('banned') else 'Tidak'}")
                print(f"✅ Terdaftar: {'Ya' if data.get('exists') else 'Tidak'}")

                detail = data.get("detail", {})
                if detail:
                    print(Fore.CYAN + "\n📋 Detail Teknis:")
                    print(f"   - SMS OTP: {detail.get('sms_length', 'N/A')} digit")
                    print(f"   - Voice OTP: {detail.get('voice_length', 'N/A')} digit")
                    print(f"   - Metode Fallback: {', '.join(detail.get('fallback_methods', []))}")
                print(Fore.WHITE + "-"*50)
            print()

    # ============================================================
    # FITUR 6: PROXY MANAGER
    # ============================================================
    def proxy_manager(self):
        """Lihat daftar proxy yang dimuat"""
        if not self.login.check_permission("user"):
            print(Fore.RED + "❌ Akses ditolak! Login terlebih dahulu!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return

        print(Fore.YELLOW + "\n[🔄] PROXY MANAGER")
        print(Fore.WHITE + "="*60)
        self.engine.show_proxies()
        input(Fore.CYAN + "\n[+] Press Enter to continue...")

    # ============================================================
    # FITUR 7: VIEW LOGS
    # ============================================================
    def view_logs(self):
        """Lihat log aktivitas"""
        if not self.login.check_permission("user"):
            print(Fore.RED + "❌ Akses ditolak! Login terlebih dahulu!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return

        print(Fore.YELLOW + "\n[📝] VIEW LOGS")
        print(Fore.WHITE + "="*60)
        self.engine.show_logs()
        input(Fore.CYAN + "\n[+] Press Enter to continue...")

    # ============================================================
    # FITUR 8: USER MANAGEMENT (ADMIN ONLY)
    # ============================================================
    def user_management(self):
        """Kelola user (hanya admin)"""
        if not self.login.is_admin():
            print(Fore.RED + "❌ Akses ditolak! Hanya admin!")
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
            return

        self.login.user_menu()

    # ============================================================
    # FITUR 9: LOGOUT
    # ============================================================
    def logout(self):
        """Logout dari sistem"""
        if self.login.is_logged_in():
            self.login.logout()
            print(Fore.GREEN + "✅ Logout berhasil!")
        else:
            print(Fore.YELLOW + "⚠️ Tidak ada user yang login!")
        input(Fore.CYAN + "\n[+] Press Enter to continue...")

    # ============================================================
    # MAIN LOOP
    # ============================================================
    def run(self):
        """Loop utama program"""
        # Login terlebih dahulu
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
                self.check_whatsapp_status()
            elif choice == "6":
                self.proxy_manager()
            elif choice == "7":
                self.view_logs()
            elif choice == "8":
                self.user_management()
            elif choice == "9":
                self.logout()
                if not self.login.login_prompt():
                    sys.exit(1)
            elif choice == "10":
                print(Fore.RED + "\n❌ Exiting...")
                print(Fore.CYAN + "© 2090 MONZ XTER LABS")
                sys.exit(0)
            else:
                print(Fore.RED + "❌ Invalid choice!")
                input(Fore.CYAN + "\n[+] Press Enter to continue...")

# ============================================================
# EKSEKUSI
# ============================================================
if __name__ == "__main__":
    app = MonzXterPro()
    app.run()