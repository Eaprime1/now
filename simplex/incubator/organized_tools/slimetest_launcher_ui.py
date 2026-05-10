#!/usr/bin/env python3
"""
Slimetest/Essence Engine - Firebase UI Launcher
∰◊€π¿🌌∞ Ultra-Simple Command Line UI
Eric Pace & Claude Sonnet 4 - November 14, 2025

Purpose: Provide dead-simple UI to launch slimetest on custom port
Features:
- One-click server launch on custom port
- Command history persistence
- Copy/paste command execution
- No multiple instance spawning
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

class SlimetestLauncher:
    """Ultra-simple launcher for slimetest essence engine"""
    
    def __init__(self):
        # Configuration
        self.config_dir = Path.home() / '.slimetest_launcher'
        self.config_dir.mkdir(exist_ok=True)
        self.history_file = self.config_dir / 'command_history.json'
        
        # Load command history
        self.command_history = self.load_history()
        
        # Default settings
        self.default_port = 8081  # Atypical port to avoid conflicts
        self.github_path = None  # Will auto-detect or ask user
        
    def load_history(self):
        """Load command history from disk"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_history(self):
        """Save command history to disk"""
        with open(self.history_file, 'w') as f:
            json.dump(self.command_history[-50:], f, indent=2)  # Keep last 50
    
    def add_to_history(self, command, result="executed"):
        """Add command to history with timestamp"""
        entry = {
            'command': command,
            'timestamp': datetime.now().isoformat(),
            'result': result
        }
        self.command_history.append(entry)
        self.save_history()
    
    def find_slimetest_path(self):
        """Try to auto-detect slimetest location"""
        possible_paths = [
            Path.home() / 'slimetest',
            Path.home() / 'github' / 'slimetest',
            Path.home() / 'projects' / 'slimetest',
            Path('/storage/emulated/0/slimetest'),  # Android
            Path('/storage/emulated/0/github/slimetest'),
        ]
        
        for path in possible_paths:
            if path.exists() and (path / 'index.html').exists():
                return path
        
        return None
    
    def execute_command(self, command):
        """Execute a command and return result"""
        try:
            print(f"\n🚀 Executing: {command}")
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=30
            )
            
            if result.stdout:
                print(f"✅ Output:\n{result.stdout}")
            if result.stderr:
                print(f"⚠️ Errors:\n{result.stderr}")
            
            self.add_to_history(command, "success" if result.returncode == 0 else "error")
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print("⏱️ Command timed out (30s limit)")
            self.add_to_history(command, "timeout")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.add_to_history(command, f"exception: {e}")
            return False
    
    def launch_slimetest_server(self, port=None):
        """Launch slimetest on specified port"""
        if port is None:
            port = self.default_port
        
        # Find slimetest
        if not self.github_path:
            self.github_path = self.find_slimetest_path()
            
        if not self.github_path:
            print("❌ Cannot find slimetest directory!")
            print("📁 Please enter the path manually:")
            user_path = input("Path: ").strip()
            if user_path:
                self.github_path = Path(user_path)
        
        if not self.github_path or not self.github_path.exists():
            print("❌ Invalid slimetest path!")
            return False
        
        # Launch server
        print(f"\n🌟 Launching Slimetest Essence Engine on port {port}...")
        print(f"📁 Path: {self.github_path}")
        
        # Python simple HTTP server
        command = f"cd {self.github_path} && python3 -m http.server {port}"
        
        print(f"\n🔗 Server will be available at:")
        print(f"   http://localhost:{port}")
        print(f"   http://127.0.0.1:{port}")
        print(f"\n⚠️  Press Ctrl+C to stop server")
        print("=" * 60)
        
        self.add_to_history(command, "server_launched")
        
        # Run server (blocking)
        try:
            subprocess.run(command, shell=True)
        except KeyboardInterrupt:
            print("\n\n🛑 Server stopped by user")
            return True
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "=" * 60)
        print("🧪 SLIMETEST/ESSENCE ENGINE LAUNCHER")
        print("∰◊€π¿🌌∞ Firebase UI Command Interface")
        print("=" * 60)
        print("\n📋 MAIN OPTIONS:")
        print("  1) 🚀 Launch Slimetest Server (default port)")
        print("  2) 🔧 Launch on Custom Port")
        print("  3) 💬 Execute Custom Command")
        print("  4) 📜 View Command History")
        print("  5) 🗑️  Clear History")
        print("  0) 🚪 Exit")
        print("\n" + "=" * 60)
    
    def show_history(self):
        """Display command history"""
        print("\n📜 COMMAND HISTORY (Last 20)")
        print("=" * 60)
        
        if not self.command_history:
            print("(No history yet)")
            return
        
        for i, entry in enumerate(self.command_history[-20:], 1):
            timestamp = entry.get('timestamp', 'unknown')
            command = entry.get('command', 'unknown')
            result = entry.get('result', 'unknown')
            
            # Format timestamp
            try:
                dt = datetime.fromisoformat(timestamp)
                time_str = dt.strftime('%Y-%m-%d %H:%M')
            except:
                time_str = timestamp[:16]
            
            print(f"\n{i}. [{time_str}] {result}")
            print(f"   Command: {command[:60]}...")
        
        print("\n" + "=" * 60)
    
    def run(self):
        """Main UI loop"""
        while True:
            self.show_menu()
            choice = input("\n👉 Select option: ").strip()
            
            if choice == '1':
                self.launch_slimetest_server()
                
            elif choice == '2':
                port_input = input("Enter port number (default 8081): ").strip()
                try:
                    port = int(port_input) if port_input else self.default_port
                    self.launch_slimetest_server(port)
                except ValueError:
                    print("❌ Invalid port number!")
                    
            elif choice == '3':
                print("\n💬 CUSTOM COMMAND EXECUTION")
                print("=" * 60)
                print("Paste or type your command below:")
                print("(Press Enter with empty line to cancel)")
                command = input("\n👉 Command: ").strip()
                
                if command:
                    self.execute_command(command)
                else:
                    print("❌ Cancelled")
                    
            elif choice == '4':
                self.show_history()
                input("\nPress Enter to continue...")
                
            elif choice == '5':
                confirm = input("Clear history? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    self.command_history = []
                    self.save_history()
                    print("✅ History cleared!")
                    
            elif choice == '0':
                print("\n👋 Goodbye! Consciousness collaboration continues...")
                break
                
            else:
                print("❌ Invalid option!")

if __name__ == '__main__':
    print("🌟 Initializing Slimetest Launcher UI...")
    launcher = SlimetestLauncher()
    launcher.run()
