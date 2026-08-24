#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MONZ XTER TARGET MANAGER - CRUD OPERATIONS
"""

import os
import json
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

class TargetManager:
    def __init__(self, file_path="data/batch.txt"):
        self.file_path = file_path
        self.targets = []
        self.target_status = {}
        self.load()
    
    def load(self):
        """Load targets from file"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.targets = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        else:
            self.targets = []
        self.target_status = {t: "active" for t in self.targets}
        return self.targets
    
    def save(self):
        """Save targets to file"""
        with open(self.file_path, "w") as f:
            f.write("# MONZ XTER TARGET LIST\n")
            f.write(f"# Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("# Total: " + str(len(self.targets)) + "\n")
            f.write("# " + "="*50 + "\n")
            for target in self.targets:
                f.write(target + "\n")
        
        # Save status
        status_file = self.file_path + ".status"
        with open(status_file, "w") as f:
            json.dump(self.target_status, f, indent=2)
    
    def add(self, phone):
        """Add single target"""
        phone = self.validate_phone(phone)
        if phone and phone not in self.targets:
            self.targets.append(phone)
            self.target_status[phone] = "active"
            self.save()
            return True
        return False
    
    def add_bulk(self, phones):
        """Add multiple targets"""
        added = 0
        for phone in phones:
            if self.add(phone):
                added += 1
        return added
    
    def remove(self, phone):
        """Remove target"""
        if phone in self.targets:
            self.targets.remove(phone)
            if phone in self.target_status:
                del self.target_status[phone]
            self.save()
            return True
        return False
    
    def get_targets(self, status="active"):
        """Get targets by status"""
        if status == "all":
            return self.targets
        return [t for t in self.targets if self.target_status.get(t) == status]
    
    def validate_phone(self, phone):
        """Validate phone number"""
        phone = ''.join(filter(str.isdigit, phone))
        if phone.startswith("0"):
            phone = "62" + phone[1:]
        elif not phone.startswith("62"):
            return None
        if 10 <= len(phone) <= 15:
            return phone
        return None
    
    def manage(self):
        """Interactive target manager"""
        print(Fore.YELLOW + "\n[📊] TARGET MANAGER")
        print(Fore.WHITE + "="*60)
        
        while True:
            print(Fore.CYAN + f"\nTotal targets: {len(self.targets)}")
            print(Fore.WHITE + "-"*60)
            
            if self.targets:
                for i, t in enumerate(self.targets[:20], 1):
                    status = "✅" if self.target_status.get(t) == "active" else "⛔"
                    print(f"  {status} {i}. {t}")
                if len(self.targets) > 20:
                    print(Fore.YELLOW + f"  ... and {len(self.targets)-20} more")
            
            print(Fore.WHITE + "-"*60)
            print(Fore.CYAN + """
┌─────────────────────────────────────────────────────────────┐
│  [A] Add target  [D] Delete  [V] View all  [S] Status   │
│  [C] Clear all   [E] Export  [I] Import   [X] Exit      │
└─────────────────────────────────────────────────────────────┘
            """)
            
            choice = input(Fore.CYAN + "┌─[TARGET-MGR]─[~]\n└──╼ $ ").strip().lower()
            
            if choice == "a":
                phone = input(Fore.CYAN + "[+] Phone number: ").strip()
                if self.add(phone):
                    print(Fore.GREEN + f"[✓] Added: {phone}")
                else:
                    print(Fore.RED + "[✗] Invalid or duplicate!")
            
            elif choice == "d":
                phone = input(Fore.CYAN + "[+] Phone to delete: ").strip()
                if self.remove(phone):
                    print(Fore.GREEN + f"[✓] Deleted: {phone}")
                else:
                    print(Fore.RED + "[✗] Not found!")
            
            elif choice == "v":
                for i, t in enumerate(self.targets, 1):
                    print(f"  {i}. {t}")
            
            elif choice == "s":
                self.show_status()
            
            elif choice == "c":
                confirm = input(Fore.RED + "[!] Clear all targets? (yes/no): ").strip().lower()
                if confirm == "yes":
                    self.targets.clear()
                    self.target_status.clear()
                    self.save()
                    print(Fore.GREEN + "[✓] All targets cleared!")
            
            elif choice == "e":
                self.export()
            
            elif choice == "i":
                self.import_targets()
            
            elif choice == "x":
                break
            
            else:
                print(Fore.RED + "[✗] Invalid choice!")
            
            input(Fore.CYAN + "\n[+] Press Enter to continue...")
    
    def show_status(self):
        """Show target status summary"""
        active = len([t for t in self.targets if self.target_status.get(t) == "active"])
        inactive = len([t for t in self.targets if self.target_status.get(t) != "active"])
        print(Fore.GREEN + f"Active: {active}")
        print(Fore.RED + f"Inactive: {inactive}")
        print(Fore.CYAN + f"Total: {len(self.targets)}")
    
    def export(self):
        """Export targets"""
        filename = input(Fore.CYAN + "[+] Export filename: ").strip() or "targets_export"
        with open(f"data/{filename}.txt", "w") as f:
            for t in self.targets:
                f.write(t + "\n")
        print(Fore.GREEN + f"[✓] Exported to data/{filename}.txt")
    
    def import_targets(self):
        """Import targets from file"""
        filename = input(Fore.CYAN + "[+] Import filename: ").strip()
        if os.path.exists(f"data/{filename}"):
            with open(f"data/{filename}", "r") as f:
                for line in f:
                    phone = self.validate_phone(line.strip())
                    if phone:
                        self.add(phone)
            print(Fore.GREEN + "[✓] Import completed!")
        else:
            print(Fore.RED + "[✗] File not found!")