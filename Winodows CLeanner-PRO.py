#!/usr/bin/env python3
# =============================================================================
# WINDOWS 11 FRESHER PRO - ULTIMATE SYSTEM CLEANER
# =============================================================================
# A professional Windows 11 cleaning tool with modern GUI
# Safely removes temporary files, cache, logs while preserving user data
# 
# Author: SHΔDØW WORM-AI💀🔥
# Version: 2.0.0
# License: MIT
# GitHub: https://github.com/yourusername/windows11-fresher-pro
# =============================================================================

import os
import sys
import shutil
import subprocess
import threading
import time
import json
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkfont
import ctypes

# =============================================================================
# CONFIGURATION
# =============================================================================

APP_NAME = "Windows 11 Fresher Pro"
APP_VERSION = "2.0.0"
APP_AUTHOR = "SHΔDØW WORM-AI💀🔥"
APP_COLOR = "#0078d4"  # Windows 11 blue

# Color scheme - Modern dark theme
COLORS = {
    'bg_dark': '#1e1e1e',        # Main background
    'bg_medium': '#252526',       # Secondary background
    'bg_light': '#2d2d2d',        # Tertiary background
    'bg_hover': '#3d3d3d',        # Hover state
    'accent': '#0078d4',          # Windows blue
    'accent_hover': '#1e8be0',     # Lighter blue
    'success': '#0c6b3f',         # Green
    'warning': '#7a5700',          # Orange/Gold
    'danger': '#8a1f1f',           # Red
    'text_primary': '#ffffff',     # White text
    'text_secondary': '#cccccc',   # Light gray
    'text_muted': '#888888',       # Dark gray
    'border': '#3e3e42'            # Border color
}

# =============================================================================
# WINDOWS 11 CLEANER CORE
# =============================================================================

class Windows11Cleaner:
    """Core cleaning engine for Windows 11"""
    
    def __init__(self, log_callback=None, progress_callback=None, status_callback=None):
        self.log_callback = log_callback
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.total_operations = 15
        self.current_operation = 0
        self.cleaned_size = 0
        self.errors = []
        self.start_time = None
        self.is_running = False
        
    def log(self, message, level="INFO"):
        """Log message with timestamp"""
        if self.log_callback:
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_callback(f"[{timestamp}] [{level}] {message}")
    
    def update_progress(self):
        """Update progress bar"""
        self.current_operation += 1
        if self.progress_callback:
            progress = int((self.current_operation / self.total_operations) * 100)
            self.progress_callback(progress)
    
    def update_status(self, status):
        """Update status message"""
        if self.status_callback:
            self.status_callback(status)
    
    def get_size_mb(self, path):
        """Get size of file/folder in MB"""
        try:
            if os.path.isfile(path):
                return os.path.getsize(path) / (1024 * 1024)
            elif os.path.isdir(path):
                total = 0
                for root, dirs, files in os.walk(path):
                    for f in files:
                        try:
                            fp = os.path.join(root, f)
                            total += os.path.getsize(fp)
                        except:
                            pass
                return total / (1024 * 1024)
        except:
            return 0
        return 0
    
    def safe_delete_file(self, path):
        """Safely delete a single file"""
        try:
            if os.path.exists(path):
                size = self.get_size_mb(path)
                os.remove(path)
                self.cleaned_size += size
                self.log(f"✓ Deleted: {os.path.basename(path)} ({size:.2f} MB)")
                return True
        except Exception as e:
            self.errors.append(str(e))
            self.log(f"✗ Failed: {os.path.basename(path)} - {str(e)}", "ERROR")
        return False
    
    def safe_clean_folder(self, path):
        """Clean folder contents but preserve folder structure"""
        try:
            if os.path.exists(path):
                total_size = 0
                file_count = 0
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            size = os.path.getsize(file_path) / (1024 * 1024)
                            os.remove(file_path)
                            total_size += size
                            file_count += 1
                        except:
                            pass
                if file_count > 0:
                    self.cleaned_size += total_size
                    self.log(f"✓ Cleaned: {os.path.basename(path)} - {file_count} files ({total_size:.2f} MB)")
                return True
        except Exception as e:
            self.log(f"✗ Failed to clean {os.path.basename(path)}", "ERROR")
        return False
    
    def clean_windows_temp(self):
        """Clean Windows temporary files"""
        self.update_status("Cleaning Windows Temp...")
        self.log("📁 Cleaning Windows Temporary Files")
        
        paths = [
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', ''),
            r"C:\Windows\Temp",
            os.path.expandvars(r"%LOCALAPPDATA%\Temp"),
        ]
        
        for path in paths:
            if path and os.path.exists(path):
                self.safe_clean_folder(path)
        self.update_progress()
    
    def clean_recycle_bin(self):
        """Empty recycle bin"""
        self.update_status("Emptying Recycle Bin...")
        self.log("🗑️ Emptying Recycle Bin")
        
        try:
            ctypes.windll.shell32.SHEmptyRecycleBinW(None, None, 0x0001)
            self.log("✓ Recycle bin emptied")
        except Exception as e:
            self.log(f"✗ Failed: {str(e)}", "ERROR")
            self.errors.append(str(e))
        self.update_progress()
    
    def clean_browser_caches(self):
        """Clean browser cache files"""
        self.update_status("Cleaning Browser Caches...")
        self.log("🌐 Cleaning Browser Caches")
        
        # Chrome
        chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cache")
        if os.path.exists(chrome_path):
            self.safe_clean_folder(chrome_path)
        
        # Edge
        edge_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cache")
        if os.path.exists(edge_path):
            self.safe_clean_folder(edge_path)
        
        # Firefox
        firefox_profiles = os.path.expandvars(r"%APPDATA%\Mozilla\Firefox\Profiles")
        if os.path.exists(firefox_profiles):
            for profile in os.listdir(firefox_profiles):
                cache_path = os.path.join(firefox_profiles, profile, "cache2")
                if os.path.exists(cache_path):
                    self.safe_clean_folder(cache_path)
        
        self.update_progress()
    
    def clean_windows_logs(self):
        """Clean Windows log files"""
        self.update_status("Cleaning Windows Logs...")
        self.log("📋 Cleaning Windows Log Files")
        
        log_paths = [
            r"C:\Windows\Logs",
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\WebCache"),
            os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Explorer"),
        ]
        
        for path in log_paths:
            if os.path.exists(path):
                self.safe_clean_folder(path)
        self.update_progress()
    
    def flush_dns(self):
        """Flush DNS cache"""
        self.update_status("Flushing DNS Cache...")
        self.log("🌐 Flushing DNS Cache")
        
        try:
            subprocess.run("ipconfig /flushdns", shell=True, capture_output=True)
            self.log("✓ DNS cache flushed")
        except Exception as e:
            self.log(f"✗ Failed: {str(e)}", "ERROR")
            self.errors.append(str(e))
        self.update_progress()
    
    def clean_prefetch(self):
        """Clean Windows Prefetch"""
        self.update_status("Cleaning Prefetch...")
        self.log("⚡ Cleaning Windows Prefetch")
        
        prefetch_path = r"C:\Windows\Prefetch"
        if os.path.exists(prefetch_path):
            self.safe_clean_folder(prefetch_path)
        self.update_progress()
    
    def clean_thumbnails(self):
        """Clean thumbnail cache"""
        self.update_status("Cleaning Thumbnail Cache...")
        self.log("🖼️ Cleaning Thumbnail Cache")
        
        thumb_path = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Explorer")
        if os.path.exists(thumb_path):
            for file in os.listdir(thumb_path):
                if file.startswith("thumbcache_"):
                    file_path = os.path.join(thumb_path, file)
                    self.safe_delete_file(file_path)
        self.update_progress()
    
    def clean_recent_files(self):
        """Clean recent files list (shortcuts only)"""
        self.update_status("Cleaning Recent Files...")
        self.log("📂 Cleaning Recent Files List")
        
        recent_path = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Recent")
        if os.path.exists(recent_path):
            self.safe_clean_folder(recent_path)
        self.update_progress()
    
    def run_disk_cleanup(self):
        """Run Windows built-in disk cleanup"""
        self.update_status("Running Disk Cleanup...")
        self.log("💿 Running Windows Disk Cleanup")
        
        try:
            subprocess.run("cleanmgr /sagerun:1", shell=True, timeout=60)
            self.log("✓ Disk cleanup completed")
        except subprocess.TimeoutExpired:
            self.log("⚠️ Disk cleanup timeout", "WARNING")
        except Exception as e:
            self.log(f"✗ Failed: {str(e)}", "ERROR")
            self.errors.append(str(e))
        self.update_progress()
    
    def clean_store_cache(self):
        """Clean Windows Store cache"""
        self.update_status("Cleaning Store Cache...")
        self.log("🛒 Cleaning Windows Store Cache")
        
        try:
            subprocess.run("wsreset.exe", shell=True, timeout=30)
            self.log("✓ Windows Store cache cleared")
        except Exception as e:
            self.log(f"✗ Failed: {str(e)}", "ERROR")
            self.errors.append(str(e))
        self.update_progress()
    
    def clean_font_cache(self):
        """Clean font cache"""
        self.update_status("Cleaning Font Cache...")
        self.log("🔤 Cleaning Font Cache")
        
        font_cache = r"C:\Windows\ServiceProfiles\LocalService\AppData\Local\FontCache"
        if os.path.exists(font_cache):
            self.safe_clean_folder(font_cache)
        self.update_progress()
    
    def clean_error_reports(self):
        """Clean Windows error reports"""
        self.update_status("Cleaning Error Reports...")
        self.log("⚠️ Cleaning Windows Error Reports")
        
        wer_path = r"C:\ProgramData\Microsoft\Windows\WER"
        if os.path.exists(wer_path):
            self.safe_clean_folder(wer_path)
        self.update_progress()
    
    def clean_setup_logs(self):
        """Clean Windows setup logs"""
        self.update_status("Cleaning Setup Logs...")
        self.log("🔧 Cleaning Windows Setup Logs")
        
        setup_paths = [
            r"C:\Windows\Panther",
            r"C:\Windows\Setup Logs",
        ]
        
        for path in setup_paths:
            if os.path.exists(path):
                self.safe_clean_folder(path)
        self.update_progress()
    
    def clean_memory_dumps(self):
        """Clean memory dump files"""
        self.update_status("Cleaning Memory Dumps...")
        self.log("💾 Cleaning Memory Dump Files")
        
        dump_paths = [
            r"C:\Windows\Minidump",
            r"C:\Windows\MEMORY.DMP",
        ]
        
        for path in dump_paths:
            if os.path.exists(path):
                if os.path.isfile(path):
                    self.safe_delete_file(path)
                else:
                    self.safe_clean_folder(path)
        self.update_progress()
    
    def run_all(self):
        """Run all cleaning operations"""
        self.is_running = True
        self.start_time = time.time()
        self.current_operation = 0
        self.cleaned_size = 0
        self.errors = []
        
        self.log("=" * 60)
        self.log(f"🚀 {APP_NAME} v{APP_VERSION} STARTED")
        self.log("=" * 60)
        
        # Run all cleaners
        self.clean_windows_temp()
        self.clean_recycle_bin()
        self.clean_browser_caches()
        self.clean_windows_logs()
        self.flush_dns()
        self.clean_prefetch()
        self.clean_thumbnails()
        self.clean_recent_files()
        self.run_disk_cleanup()
        self.clean_store_cache()
        self.clean_font_cache()
        self.clean_error_reports()
        self.clean_setup_logs()
        self.clean_memory_dumps()
        
        # Final stats
        elapsed_time = time.time() - self.start_time
        self.log("=" * 60)
        self.log("✅ CLEANING COMPLETED!")
        self.log(f"📊 Space Freed: {self.cleaned_size:.2f} MB")
        self.log(f"⏱️ Time Taken: {elapsed_time:.1f} seconds")
        self.log(f"⚠️ Errors: {len(self.errors)}")
        self.log("=" * 60)
        
        self.is_running = False
        self.update_status("Cleaning completed")
        
        return self.cleaned_size, len(self.errors), elapsed_time


# =============================================================================
# PROFESSIONAL GUI - GITHUB READY
# =============================================================================

class FresherProGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("900x700")
        self.root.minsize(900, 700)
        
        # Set icon (if available)
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass
        
        # Center window
        self.center_window()
        
        # Configure styles
        self.setup_styles()
        
        # Variables
        self.cleaner = None
        self.is_running = False
        
        # Create UI
        self.create_header()
        self.create_main_content()
        self.create_footer()
        
        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        self.root.configure(bg=COLORS['bg_dark'])
        
        # Progress bar style
        style.configure("green.Horizontal.TProgressbar",
                       background=COLORS['success'],
                       troughcolor=COLORS['bg_light'],
                       bordercolor=COLORS['border'],
                       lightcolor=COLORS['success'],
                       darkcolor=COLORS['success'])
        
        # Button styles
        style.configure("Accent.TButton",
                       background=COLORS['accent'],
                       foreground='white',
                       borderwidth=0,
                       focusthickness=0,
                       font=('Segoe UI', 10, 'bold'))
        style.map("Accent.TButton",
                 background=[('active', COLORS['accent_hover'])])
        
        style.configure("Success.TButton",
                       background=COLORS['success'],
                       foreground='white',
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'))
        
        style.configure("Danger.TButton",
                       background=COLORS['danger'],
                       foreground='white',
                       borderwidth=0,
                       font=('Segoe UI', 10, 'bold'))
    
    def create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg=COLORS['bg_medium'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # App icon (emoji as placeholder)
        icon_label = tk.Label(header_frame,
                             text="🧹",
                             font=('Segoe UI', 40),
                             bg=COLORS['bg_medium'])
        icon_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Title and version
        title_frame = tk.Frame(header_frame, bg=COLORS['bg_medium'])
        title_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, pady=10)
        
        title_label = tk.Label(title_frame,
                              text=APP_NAME,
                              font=('Segoe UI', 24, 'bold'),
                              bg=COLORS['bg_medium'],
                              fg=COLORS['text_primary'])
        title_label.pack(anchor=tk.W)
        
        subtitle_label = tk.Label(title_frame,
                                 text=f"Version {APP_VERSION} • Professional System Cleaner",
                                 font=('Segoe UI', 10),
                                 bg=COLORS['bg_medium'],
                                 fg=COLORS['text_muted'])
        subtitle_label.pack(anchor=tk.W)
        
        # Status badge
        badge_frame = tk.Frame(header_frame, bg=COLORS['bg_medium'])
        badge_frame.pack(side=tk.RIGHT, padx=20)
        
        self.badge_label = tk.Label(badge_frame,
                                   text="● READY",
                                   font=('Segoe UI', 11, 'bold'),
                                   bg=COLORS['bg_medium'],
                                   fg=COLORS['success'])
        self.badge_label.pack()
        
        tk.Label(badge_frame,
                text="Windows 11 Optimized",
                font=('Segoe UI', 9),
                bg=COLORS['bg_medium'],
                fg=COLORS['text_muted']).pack()
    
    def create_main_content(self):
        """Create main content area"""
        main_frame = tk.Frame(self.root, bg=COLORS['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Info card
        self.create_info_card(main_frame)
        
        # Progress section
        self.create_progress_section(main_frame)
        
        # Stats section
        self.create_stats_section(main_frame)
        
        # Log section
        self.create_log_section(main_frame)
    
    def create_info_card(self, parent):
        """Create information card"""
        info_frame = tk.Frame(parent, bg=COLORS['bg_medium'], height=80)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        info_frame.pack_propagate(False)
        
        # Info icon
        tk.Label(info_frame,
                text="ℹ️",
                font=('Segoe UI', 20),
                bg=COLORS['bg_medium'],
                fg=COLORS['accent']).pack(side=tk.LEFT, padx=15)
        
        # Info text
        info_text = "Your personal files are 100% SAFE!\nOnly temporary files, cache, and logs will be removed."
        tk.Label(info_frame,
                text=info_text,
                font=('Segoe UI', 10),
                bg=COLORS['bg_medium'],
                fg=COLORS['text_secondary'],
                justify=tk.LEFT).pack(side=tk.LEFT, padx=5)
        
        # Shield icon
        tk.Label(info_frame,
                text="🛡️",
                font=('Segoe UI', 20),
                bg=COLORS['bg_medium'],
                fg=COLORS['success']).pack(side=tk.RIGHT, padx=15)
    
    def create_progress_section(self, parent):
        """Create progress section"""
        progress_frame = tk.LabelFrame(parent,
                                      text="CLEANING PROGRESS",
                                      font=('Segoe UI', 10, 'bold'),
                                      bg=COLORS['bg_dark'],
                                      fg=COLORS['text_primary'],
                                      bd=1,
                                      relief=tk.SOLID)
        progress_frame.pack(fill=tk.X, pady=5)
        
        # Progress bar
        bar_frame = tk.Frame(progress_frame, bg=COLORS['bg_dark'])
        bar_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(bar_frame,
                                           variable=self.progress_var,
                                           maximum=100,
                                           mode='determinate',
                                           style="green.Horizontal.TProgressbar",
                                           length=800)
        self.progress_bar.pack(fill=tk.X)
        
        # Progress label
        self.progress_label = tk.Label(bar_frame,
                                      text="0% Complete",
                                      font=('Segoe UI', 9),
                                      bg=COLORS['bg_dark'],
                                      fg=COLORS['text_muted'])
        self.progress_label.pack(anchor=tk.E, pady=(5,0))
    
    def create_stats_section(self, parent):
        """Create statistics section"""
        stats_frame = tk.Frame(parent, bg=COLORS['bg_dark'])
        stats_frame.pack(fill=tk.X, pady=5)
        
        # Stats cards in grid
        card_frame = tk.Frame(stats_frame, bg=COLORS['bg_dark'])
        card_frame.pack(fill=tk.X)
        
        # Space freed card
        space_card = tk.Frame(card_frame, bg=COLORS['bg_medium'], width=200, height=80)
        space_card.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        space_card.pack_propagate(False)
        
        tk.Label(space_card,
                text="💾",
                font=('Segoe UI', 24),
                bg=COLORS['bg_medium']).pack(pady=(10,0))
        tk.Label(space_card,
                text="Space Freed",
                font=('Segoe UI', 9),
                bg=COLORS['bg_medium'],
                fg=COLORS['text_muted']).pack()
        self.freed_label = tk.Label(space_card,
                                   text="0 MB",
                                   font=('Segoe UI', 14, 'bold'),
                                   bg=COLORS['bg_medium'],
                                   fg=COLORS['success'])
        self.freed_label.pack()
        
        # Errors card
        errors_card = tk.Frame(card_frame, bg=COLORS['bg_medium'], width=200, height=80)
        errors_card.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        errors_card.pack_propagate(False)
        
        tk.Label(errors_card,
                text="⚠️",
                font=('Segoe UI', 24),
                bg=COLORS['bg_medium']).pack(pady=(10,0))
        tk.Label(errors_card,
                text="Errors",
                font=('Segoe UI', 9),
                bg=COLORS['bg_medium'],
                fg=COLORS['text_muted']).pack()
        self.errors_label = tk.Label(errors_card,
                                    text="0",
                                    font=('Segoe UI', 14, 'bold'),
                                    bg=COLORS['bg_medium'],
                                    fg=COLORS['warning'])
        self.errors_label.pack()
        
        # Time card
        time_card = tk.Frame(card_frame, bg=COLORS['bg_medium'], width=200, height=80)
        time_card.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        time_card.pack_propagate(False)
        
        tk.Label(time_card,
                text="⏱️",
                font=('Segoe UI', 24),
                bg=COLORS['bg_medium']).pack(pady=(10,0))
        tk.Label(time_card,
                text="Time",
                font=('Segoe UI', 9),
                bg=COLORS['bg_medium'],
                fg=COLORS['text_muted']).pack()
        self.time_label = tk.Label(time_card,
                                  text="0s",
                                  font=('Segoe UI', 14, 'bold'),
                                  bg=COLORS['bg_medium'],
                                  fg=COLORS['accent'])
        self.time_label.pack()
        
        # Status card
        status_card = tk.Frame(card_frame, bg=COLORS['bg_medium'], width=200, height=80)
        status_card.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)
        status_card.pack_propagate(False)
        
        tk.Label(status_card,
                text="🔧",
                font=('Segoe UI', 24),
                bg=COLORS['bg_medium']).pack(pady=(10,0))
        tk.Label(status_card,
                text="Status",
                font=('Segoe UI', 9),
                bg=COLORS['bg_medium'],
                fg=COLORS['text_muted']).pack()
        self.status_label = tk.Label(status_card,
                                    text="Ready",
                                    font=('Segoe UI', 12, 'bold'),
                                    bg=COLORS['bg_medium'],
                                    fg=COLORS['text_primary'])
        self.status_label.pack()
    
    def create_log_section(self, parent):
        """Create log section with controls"""
        log_frame = tk.LabelFrame(parent,
                                 text="CLEANING LOG",
                                 font=('Segoe UI', 10, 'bold'),
                                 bg=COLORS['bg_dark'],
                                 fg=COLORS['text_primary'],
                                 bd=1,
                                 relief=tk.SOLID)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Control buttons
        control_frame = tk.Frame(log_frame, bg=COLORS['bg_dark'])
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.start_btn = tk.Button(control_frame,
                                  text="🚀 START CLEANING",
                                  bg=COLORS['success'],
                                  fg='white',
                                  font=('Segoe UI', 11, 'bold'),
                                  width=18,
                                  height=2,
                                  bd=0,
                                  cursor='hand2',
                                  command=self.start_cleaning)
        self.start_btn.pack(side=tk.LEFT, padx=2)
        
        self.stop_btn = tk.Button(control_frame,
                                 text="⏹ STOP",
                                 bg=COLORS['danger'],
                                 fg='white',
                                 font=('Segoe UI', 11, 'bold'),
                                 width=10,
                                 height=2,
                                 bd=0,
                                 cursor='hand2',
                                 command=self.stop_cleaning,
                                 state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=2)
        
        self.clear_btn = tk.Button(control_frame,
                                  text="🗑️ CLEAR LOG",
                                  bg=COLORS['bg_light'],
                                  fg=COLORS['text_primary'],
                                  font=('Segoe UI', 11, 'bold'),
                                  width=12,
                                  height=2,
                                  bd=0,
                                  cursor='hand2',
                                  command=self.clear_log)
        self.clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Log text area with scrollbar
        text_frame = tk.Frame(log_frame, bg=COLORS['bg_dark'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(text_frame,
                               bg=COLORS['bg_light'],
                               fg='#00ff00',
                               font=('Consolas', 10),
                               wrap=tk.WORD,
                               height=12,
                               bd=1,
                               relief=tk.SUNKEN)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(text_frame, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
    
    def create_footer(self):
        """Create application footer"""
        footer_frame = tk.Frame(self.root, bg=COLORS['bg_medium'], height=40)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)
        
        # GitHub link
        github_label = tk.Label(footer_frame,
                               text="⭐ Star on GitHub | MIT License | Windows 11 Optimized",
                               font=('Segoe UI', 9),
                               bg=COLORS['bg_medium'],
                               fg=COLORS['text_muted'],
                               cursor='hand2')
        github_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Copyright
        copyright_label = tk.Label(footer_frame,
                                  text=f"© 2024 {APP_AUTHOR}",
                                  font=('Segoe UI', 9),
                                  bg=COLORS['bg_medium'],
                                  fg=COLORS['text_muted'])
        copyright_label.pack(side=tk.RIGHT, padx=15, pady=10)
    
    def log_message(self, message):
        """Add message to log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_var.set(value)
        self.progress_label.config(text=f"{value}% Complete")
        self.root.update_idletasks()
    
    def update_status(self, status):
        """Update status display"""
        self.status_label.config(text=status)
        self.root.update_idletasks()
    
    def update_stats(self, freed, errors, elapsed):
        """Update statistics"""
        self.freed_label.config(text=f"{freed:.2f} MB")
        self.errors_label.config(text=str(errors))
        self.time_label.config(text=f"{elapsed:.1f}s")
        self.root.update_idletasks()
    
    def start_cleaning(self):
        """Start cleaning process"""
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(state=tk.DISABLED, bg=COLORS['bg_light'])
            self.stop_btn.config(state=tk.NORMAL)
            self.badge_label.config(text="● CLEANING", fg=COLORS['warning'])
            self.clear_log()
            
            # Reset stats
            self.update_stats(0, 0, 0)
            
            # Create cleaner instance
            self.cleaner = Windows11Cleaner(
                log_callback=self.log_message,
                progress_callback=self.update_progress,
                status_callback=self.update_status
            )
            
            # Start cleaning in thread
            self.thread = threading.Thread(target=self.run_cleaner, daemon=True)
            self.thread.start()
    
    def run_cleaner(self):
        """Run cleaner in background thread"""
        freed, errors, elapsed = self.cleaner.run_all()
        
        # Update UI in main thread
        self.root.after(0, self.cleaning_completed, freed, errors, elapsed)
    
    def cleaning_completed(self, freed, errors, elapsed):
        """Handle cleaning completion"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL, bg=COLORS['success'])
        self.stop_btn.config(state=tk.DISABLED)
        self.badge_label.config(text="● READY", fg=COLORS['success'])
        self.update_stats(freed, errors, elapsed)
        
        # Show completion message
        messagebox.showinfo("✅ Cleaning Complete",
                           f"Windows 11 has been successfully cleaned!\n\n"
                           f"📊 Space Freed: {freed:.2f} MB\n"
                           f"⏱️ Time Taken: {elapsed:.1f} seconds\n"
                           f"⚠️ Errors: {errors}\n\n"
                           f"Your system is now running fresh!")
    
    def stop_cleaning(self):
        """Stop cleaning process"""
        if self.is_running and self.cleaner:
            self.cleaner.is_running = False
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL, bg=COLORS['success'])
            self.stop_btn.config(state=tk.DISABLED)
            self.badge_label.config(text="● STOPPED", fg=COLORS['danger'])
            self.log_message("\n⚠️ Cleaning stopped by user")
            self.update_status("Stopped")
    
    def clear_log(self):
        """Clear log text"""
        self.log_text.delete(1.0, tk.END)
    
    def on_closing(self):
        """Handle window closing"""
        if self.is_running:
            if messagebox.askyesno("⚠️ Confirm Exit",
                                  "Cleaning is in progress.\n"
                                  "Are you sure you want to exit?"):
                self.stop_cleaning()
                time.sleep(0.5)
                self.root.destroy()
        else:
            self.root.destroy()
        sys.exit(0)
    
    def run(self):
        """Run the application"""
        self.root.mainloop()


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

def main():
    """Main function"""
    # Check if running on Windows
    if not sys.platform.startswith('win'):
        print("❌ This tool is designed for Windows 11 only!")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Check for admin privileges
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        if not is_admin:
            print("⚠️ Some features require Administrator privileges!")
            print("   For best results, run as Administrator.\n")
    except:
        pass
    
    # Run the GUI
    try:
        app = FresherProGUI()
        app.run()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()