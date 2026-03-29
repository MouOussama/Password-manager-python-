import sys
import os
import secrets
import string
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.uic import loadUi

class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('password_manager.ui', self)
        
        self.generateButton.clicked.connect(self.generate_password)
        self.saveButton.clicked.connect(self.save_password)
        self.retrieveButton.clicked.connect(self.retrieve_password)
        
        self.outputTextEdit.clear()
        self.outputTextEdit.append("Welcome to Password Manager!\\nFill name/site, generate or enter pw, save/retrieve.")
    
    def get_charset(self, level):
        chars = string.ascii_letters + string.digits
        if level == "Medium":
            chars += "!@#$%^&*?"
        elif level == "High":
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return chars
    
    def generate_password(self):
        name = self.nameEdit.text().strip()
        if not name:
            self.show_message("Please enter your name.")
            return
        
        site = self.siteComboBox.currentText().strip()
        if not site:
            self.show_message("Please enter or select a site.")
            return
        
        level = self.levelComboBox.currentText()
        if level == "Low":
            length = 8
        elif level == "Medium":
            length = 12
        else:
            length = 16
        
        charset = self.get_charset(level)
        password = ''.join(secrets.choice(charset) for _ in range(length))
        self.passwordEdit.setText(password)
        self.show_message(f"Generated {level} password for {site}.")
    
    def save_password(self):
        name = self.nameEdit.text().strip()
        site = self.siteComboBox.currentText().strip()
        password = self.passwordEdit.text().strip()
        
        if not all([name, site, password]):
            self.show_message("Please fill name, site, password (generate or type).")
            return
        
        key = f"{name}:{site}:"
        entry = f"{name}:{site}:{password}\n"
        
        try:
            with open('passwords.txt', 'r') as f:
                lines = f.readlines()
            
            exists = any(line.startswith(key) for line in lines)
            
            if exists:
                reply = QMessageBox.question(self, 'Password Exists', 
                    f"Password for {name}:{site} already exists.\n Update it with the new password?", 
                    QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    new_lines = []
                    for line in lines:
                        if line.startswith(key):
                            new_lines.append(entry)
                        else:
                            new_lines.append(line)
                    with open('passwords.txt', 'w') as f:
                        f.writelines(new_lines)
                    self.show_message(f"Updated password for {name}:{site}.")
                else:
                    self.show_message("Save cancelled.")
            else:
                with open('passwords.txt', 'a') as f:
                    f.write(entry)
                self.show_message(f"Saved new password for {name}:{site}.")
        except FileNotFoundError:
            with open('passwords.txt', 'a') as f:
                f.write(entry)
            self.show_message(f"Saved new password for {name}:{site}.")
        
        self.passwordEdit.clear()
    
    def retrieve_password(self):
        self.passwordEdit.clear()
        self.outputTextEdit.clear()
        name = self.nameEdit.text().strip()
        if not name:
            self.show_message("Please enter your name to retrieve.")
            return
        site = self.siteComboBox.currentText().strip()
        try:
            with open('passwords.txt', 'r') as f:
                lines = f.readlines()
            if site:
                found = False
                for line in lines:
                    if line.startswith(f"{name}:{site}:"):
                        parts = line.strip().split(':', 2)
                        if len(parts) == 3:
                            password = parts[2]
                            self.outputTextEdit.append("=== Specific Password ===")
                            self.outputTextEdit.append(f"Site: {site}")
                            self.outputTextEdit.append(f"Password: {password}")
                            self.show_message(f"Retrieved for {name}:{site}.")
                            found = True
                            break
                if not found:
                    self.show_message(f"No password for {name}:{site}.")
            else:
                self.outputTextEdit.append(f"=== All Passwords for {name} ===")
                has_any = False
                for line in lines:
                    if line.startswith(f"{name}:"):
                        parts = line.strip().split(':', 2)
                        if len(parts) == 3:
                            s = parts[1]
                            p = parts[2]
                            self.outputTextEdit.append(f"Site: {s}")
                            self.outputTextEdit.append(f"Password: {p}")
                            self.outputTextEdit.append("")
                            has_any = True
                if has_any:
                    self.show_message(f"Retrieved all for {name}.")
                else:
                    self.show_message(f"No passwords for {name}.")
        except FileNotFoundError:
            self.show_message("No passwords.txt. Save first.")
    
    def show_message(self, msg):
        self.outputTextEdit.append(msg)
        scrollbar = self.outputTextEdit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordManager()
    window.show()
    sys.exit(app.exec_())

