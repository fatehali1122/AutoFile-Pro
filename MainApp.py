import threading
from pathlib import Path
import customtkinter as ctk
from customtkinter import filedialog
from tkinter import messagebox
from Organizer import Organizer
from Backup import Backup
from Cleanup import Cleanup
COLORS = {
    "bg_main": "#0f172a",
    "bg_sidebar": "#020617",
    "accent": "#38bdf8",
    "text": "#e2e8f0",
    "panel": "#1e293b",
    "success": "#22c55e",
    "danger": "#f41414"
}

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class SectionFrame(ctk.CTkFrame):
    def __init__(self, master, title, **kwargs):
        super().__init__(master, fg_color=COLORS["bg_main"], corner_radius=0, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.title = ctk.CTkLabel(
            self, 
            text=title, 
            font=("Roboto Medium", 24), 
            text_color=COLORS["accent"],
            anchor="w"
        )
        self.title.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))
        
        self.h_rule = ctk.CTkProgressBar(self, height=2, progress_color=COLORS["panel"])
        self.h_rule.set(1) 
        self.h_rule.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 20))

class OrganizerFrame(SectionFrame):
    def __init__(self, master):
        super().__init__(master, title="Organizer")

        self.controls = ctk.CTkFrame(self, fg_color=COLORS["panel"])
        self.controls.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        self.run_btn = ctk.CTkButton(
            self.controls, 
            text="Run Organizer", 
            text_color= "white", 
            fg_color=COLORS["success"], 
            hover_color="#16a34a", 
        )
        self.run_btn.configure(command = self.start_organizing)
        self.run_btn.pack(side="bottom", pady=20)

        ctk.CTkLabel(self.controls, text="Source Folder:", font=("Roboto", 14, "bold")).pack(side="top", anchor="w", padx=20, pady=(10, 2))
        
        folder_frame = ctk.CTkFrame(self.controls, fg_color="transparent")
        folder_frame.pack(side="top", fill="x", padx=20, pady=2)
        
        self.folder_entry = ctk.CTkEntry(folder_frame, placeholder_text="C:\\Users\\Example\\Downloads...")
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.browse_btn = ctk.CTkButton(folder_frame, text="📂 Browse", width=100, fg_color=COLORS["accent"], text_color=COLORS["bg_sidebar"],command=self.browse_folder)
        self.browse_btn.pack(side="right")

        ctk.CTkLabel(self.controls, text="Organization Mode:", font=("Roboto", 14, "bold")).pack(side="top", anchor="w", padx=20, pady=(15, 5))
        
        from config.Config_manager import ConfigManager
        cfg = ConfigManager.get_instance()
        self.mode_var = ctk.StringVar(value=cfg.get("organizer", "mode"))
        
        mode_frame = ctk.CTkFrame(self.controls, fg_color="transparent")
        mode_frame.pack(side="top", fill="x", padx=20, pady=0)

        ctk.CTkRadioButton(mode_frame, text="By Extension", variable=self.mode_var, value="extension").pack(side="left", padx=(0, 20))
        ctk.CTkRadioButton(mode_frame, text="By Size", variable=self.mode_var, value="size").pack(side="left", padx=(0, 20))
        ctk.CTkRadioButton(mode_frame, text="By Age", variable=self.mode_var, value="age").pack(side="left")

        self.preview_container = ctk.CTkFrame(self.controls, fg_color=COLORS["bg_main"], corner_radius=10, border_width=1, border_color="#334155")
        self.preview_container.pack(side="top", fill="both", expand=True, padx=20, pady=20)

        self.scan_btn = ctk.CTkButton(
            self.preview_container,
            text="🔍 Scan Folder",
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["accent"],
            text_color=COLORS["accent"],
            height=30,
            width=120
        )
        self.scan_btn.configure(command = self.run_scan)
        self.scan_btn.pack(pady=(15, 10))

        self.log_panel = ctk.CTkScrollableFrame(
            self.preview_container, 
            fg_color="transparent", 
            height=140 
        )
        self.log_panel.pack(fill="both", expand=True, padx=5, pady=(0, 15))

        ctk.CTkLabel(self.log_panel, text="> Waiting to scan...", text_color="gray", font=("Roboto Mono", 12)).pack(anchor="w")

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, path)
    def run_scan(self):
        path = self.folder_entry.get()
        if not path: return
        
        from config.Config_manager import ConfigManager
        ConfigManager.get_instance().set("organizer", "mode", self.mode_var.get())
        
        self.organizer = Organizer(Path(path)) 
        summary = self.organizer.preview()
        
        for widget in self.log_panel.winfo_children(): widget.destroy()
        
        if "docs" in summary:
            ctk.CTkLabel(self.log_panel, text=f"Documents:   {summary['docs']}").pack(anchor="w")
            ctk.CTkLabel(self.log_panel, text=f"Images:      {summary['images']}").pack(anchor="w")
            ctk.CTkLabel(self.log_panel, text=f"Videos:      {summary['videos']}").pack(anchor="w")
            ctk.CTkLabel(self.log_panel, text=f"Audios:      {summary['audios']}").pack(anchor="w")
            ctk.CTkLabel(self.log_panel, text=f"Code Files:  {summary['codes']}").pack(anchor="w")
            ctk.CTkLabel(self.log_panel, text=f"Others:      {summary['others']}").pack(anchor="w")

        elif "small" in summary:
            ctk.CTkLabel(self.log_panel, text=f"Small Files:      {summary['small']}").pack(anchor="w")
            ctk.CTkLabel(self.log_panel, text=f"Large Files:      {summary['large']}").pack(anchor="w")
            ctk.CTkLabel(self.log_panel, text=f"Very Large Files: {summary['very_large']}").pack(anchor="w")

        elif "recent" in summary:
            ctk.CTkLabel(self.log_panel, text=f"Recent Files:   {summary['recent']}").pack(anchor="w")
            ctk.CTkLabel(self.log_panel, text=f"Old Files:      {summary['old']}").pack(anchor="w")
            ctk.CTkLabel(self.log_panel, text=f"Very Old Files: {summary['very_old']}").pack(anchor="w")

    def start_organizing(self):
        if not hasattr(self, 'organizer'): return
        
        def _task():
            self.run_btn.configure(state="disabled", text="Running...")
            self.organizer.run_organizer() 
            self.run_btn.configure(state="normal", text="Run Organizer")
            
            self.master.show_success_notification("Success", "Organization Complete!")

        threading.Thread(target=_task).start()

class BackupFrame(SectionFrame):
    def __init__(self, master):
        super().__init__(master, title="Backup")

        self.controls = ctk.CTkFrame(self, fg_color=COLORS["panel"])
        self.controls.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        
        self.controls.grid_columnconfigure(0, weight=1)
        self.controls.grid_rowconfigure(5, weight=1) 

        ctk.CTkLabel(self.controls, text="Source Folder:", font=("Roboto", 14, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
        
        source_frame = ctk.CTkFrame(self.controls, fg_color="transparent")
        source_frame.pack(fill="x", padx=20, pady=2)
        
        self.source_entry = ctk.CTkEntry(source_frame, placeholder_text="C:\\Users\\...")
        self.source_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.btn_browse_source = ctk.CTkButton(source_frame, text="📂 Browse", width=100, fg_color=COLORS["accent"], text_color=COLORS["bg_sidebar"],command=self.browse_source)
        self.btn_browse_source.pack(side="right")


        ctk.CTkLabel(self.controls, text="Destination Folder:", font=("Roboto", 14, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
        
        dest_frame = ctk.CTkFrame(self.controls, fg_color="transparent")
        dest_frame.pack(fill="x", padx=20, pady=2)
        
        self.dest_entry = ctk.CTkEntry(dest_frame, placeholder_text="D:\\MyBackups...")
        self.dest_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.btn_browse_dest = ctk.CTkButton(dest_frame, text="📂 Browse", width=100, fg_color=COLORS["accent"], text_color=COLORS["bg_sidebar"],command=self.browse_dest)
        self.btn_browse_dest.pack(side="right")


        self.zip_check = ctk.CTkCheckBox(self.controls, text="Compress Backup (Save as .ZIP)", font=("Roboto", 13))
        self.zip_check.pack(anchor="w", padx=20, pady=(15, 5))

        from config.Config_manager import ConfigManager
        cfg = ConfigManager.get_instance()
        if cfg.get("backup", "compress"):
            self.zip_check.select()


        self.preview_frame = ctk.CTkFrame(self.controls, fg_color=COLORS["bg_main"], corner_radius=10, border_width=1, border_color="#334155")
        self.preview_frame.pack(fill="x", padx=20, pady=20)

        self.scan_btn = ctk.CTkButton(
            self.preview_frame,
            text="🔍 Scan for Files",
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["accent"],
            text_color=COLORS["accent"],
            height=30,
            width=120
        )
        self.scan_btn.configure(command = self.run_scan)
        self.scan_btn.pack(pady=(15, 10))

        self.stats_container = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        self.stats_container.pack(pady=(0, 15))

        self.lbl_files = ctk.CTkLabel(self.stats_container, text="Files Found: 0", font=("Roboto Mono", 14), text_color="white")
        self.lbl_files.pack(side="left", padx=20)

        ctk.CTkLabel(self.stats_container, text="|", text_color="gray").pack(side="left", padx=10)

        self.lbl_size = ctk.CTkLabel(self.stats_container, text="Total Size: 0 MB", font=("Roboto Mono", 14), text_color="white")
        self.lbl_size.pack(side="left", padx=20)

        self.run_btn = ctk.CTkButton(
            self.controls, 
            text="Start Backup", 
            text_color= "white",
            fg_color=COLORS["success"], 
            hover_color="#16a34a", 
        )
        self.run_btn.configure(command = self.start_backup)
        self.run_btn.pack(pady=(20, 20), anchor="center")
    def browse_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_entry.delete(0, "end")
            self.source_entry.insert(0, path)
    def browse_dest(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_entry.delete(0, "end")
            self.dest_entry.insert(0, path)
    def run_scan(self):
        src = self.source_entry.get()
        dst = self.dest_entry.get()
        
        if not src: return

        self.backup = Backup(Path(src), Path(dst) if dst else None)
        
        stats = self.backup.preview()
        
        self.lbl_files.configure(text=f"Files Found: {stats['files']}")
        self.lbl_size.configure(text=f"Total Size: {stats['size']} MB")

    def start_backup(self):
        if not hasattr(self, 'backup'): return
        
        from config.Config_manager import ConfigManager
        is_compressed = bool(self.zip_check.get())
        ConfigManager.get_instance().set("backup", "compress", is_compressed)
        self.backup.compress = is_compressed # Update the instance directly

        def _task():
            self.run_btn.configure(state="disabled", text="Backing up...")
            try:
                self.backup.run_Backup()
                self.master.show_success_notification("Success", "Backup Created Successfully!")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                self.run_btn.configure(state="normal", text="Start Backup")

        threading.Thread(target=_task).start()

class CleanupFrame(SectionFrame):
    def __init__(self, master):
        super().__init__(master, title="Cleanup")

        self.controls = ctk.CTkFrame(self, fg_color=COLORS["panel"])
        self.controls.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        
        self.controls.grid_columnconfigure(0, weight=1)
        self.controls.grid_rowconfigure(6, weight=1) 


        ctk.CTkLabel(self.controls, text="Source Folder:", font=("Roboto", 14, "bold")).pack(anchor="w", padx=20, pady=(10, 2))
        
        folder_frame = ctk.CTkFrame(self.controls, fg_color="transparent")
        folder_frame.pack(fill="x", padx=20, pady=2)
        
        self.folder_entry = ctk.CTkEntry(folder_frame, placeholder_text="C:\\Users\\Example\\Downloads...")
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        self.browse_btn = ctk.CTkButton(folder_frame, text="📂 Browse", width=100, fg_color=COLORS["accent"], text_color=COLORS["bg_sidebar"],command=self.browse_folder)
        self.browse_btn.pack(side="right")


        ctk.CTkLabel(self.controls, text="Cleanup Mode:", font=("Roboto", 14, "bold")).pack(anchor="w", padx=20, pady=(15, 5))
        
        from config.Config_manager import ConfigManager
        cfg = ConfigManager.get_instance()

        self.clean_mode_var = ctk.StringVar(value=cfg.get("cleanup", "mode"))

        mode_frame = ctk.CTkFrame(self.controls, fg_color="transparent")
        mode_frame.pack(fill="x", padx=20, pady=0)

        ctk.CTkRadioButton(
            mode_frame, 
            text="By Size (Delete files > Limit)", 
            variable=self.clean_mode_var, 
            value="size"
        ).pack(side="left", padx=(0, 20))

        ctk.CTkRadioButton(
            mode_frame, 
            text="By Age (Delete files > Days)", 
            variable=self.clean_mode_var, 
            value="age"
        ).pack(side="left")

        self.preview_frame = ctk.CTkFrame(self.controls, fg_color=COLORS["bg_main"], corner_radius=10, border_width=1, border_color="#334155")
        self.preview_frame.pack(fill="x", padx=20, pady=10) 

        self.scan_btn = ctk.CTkButton(
            self.preview_frame,
            text="🔍 Scan for Files",
            fg_color="transparent",
            border_width=1,
            border_color=COLORS["accent"],
            text_color=COLORS["accent"],
            height=30,
            width=140
        )
        self.scan_btn.configure(command = self.run_scan)
        self.scan_btn.pack(pady=(10, 5), anchor="center")

        self.stats_container = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        self.stats_container.pack(pady=(0, 10))

        self.lbl_files = ctk.CTkLabel(self.stats_container, text="Files Found: 0", font=("Roboto Mono", 14), text_color="white")
        self.lbl_files.pack(side="left", padx=15)

        ctk.CTkLabel(self.stats_container, text="|", text_color="gray").pack(side="left", padx=5)

        self.lbl_size = ctk.CTkLabel(self.stats_container, text="Total Size: 0 MB", font=("Roboto Mono", 14), text_color="white")
        self.lbl_size.pack(side="left", padx=15)


        ctk.CTkLabel(self.controls, text="Action:", font=("Roboto", 14, "bold")).pack(anchor="w", padx=20, pady=(5, 5))
        
        self.action_var = ctk.StringVar(value="archive") 

        action_frame = ctk.CTkFrame(self.controls, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=0)

        ctk.CTkRadioButton(
            action_frame, 
            text="Move to Archive", 
            variable=self.action_var, 
            value="archive"
        ).pack(side="left", padx=(0, 20))

        ctk.CTkRadioButton(
            action_frame, 
            text="Move to Recycle Bin", 
            variable=self.action_var, 
            value="recycle"
        ).pack(side="left")

        self.run_btn = ctk.CTkButton(
            self.controls, 
            text="Run Cleanup",
            text_color= "white",
            fg_color=COLORS["danger"], 
            hover_color="#dc2626",
        )
        self.run_btn.configure(command = self.start_cleanup)
        self.run_btn.pack(pady=(20, 20), anchor="center")
    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, path)
    def run_scan(self):
        path = self.folder_entry.get()
        if not path: return
        
        from config.Config_manager import ConfigManager
        ConfigManager.get_instance().set("cleanup", "mode", self.clean_mode_var.get())
        
        self.cleanup = Cleanup(Path(path))
        
        self.cleanup.run_cleanup()
        stats = self.cleanup.preview()
        
        self.lbl_files.configure(text=f"Files Found: {stats['count']}")
        self.lbl_size.configure(text=f"Total Size: {stats['size']} MB")

    def start_cleanup(self):
        if not hasattr(self, 'cleanup'): return
        
        action = self.action_var.get()
        
        def _task():
            self.run_btn.configure(state="disabled", text="Cleaning...")
            try:
                if action == "recycle":
                    self.cleanup.move_to_recyclebin()
                else:
                    self.cleanup.move_to_archive()
                
                self.master.show_success_notification("Success", "Cleanup Completed!")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                self.run_btn.configure(state="normal", text="Run Cleanup")

        threading.Thread(target=_task).start()
        
class SettingsFrame(SectionFrame):
    def __init__(self, master):
        super().__init__(master, title="Settings")
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        ctk.CTkLabel(self.scroll, text="General", font=("Roboto", 16, "bold")).pack(anchor="w", padx=10, pady=(10,5))
        self.notify_switch = self.add_setting("Show notifications")

        ctk.CTkLabel(self.scroll, text="Organizer Thresholds", font=("Roboto", 16, "bold")).pack(anchor="w", padx=10, pady=(20,5))
                
        self.entry_size_low = self.add_input_setting("Small File Limit (MB)", "organizer", "size_low_mb")
        self.entry_size_high = self.add_input_setting("Large File Limit (MB)", "organizer", "size_high_mb")
        
        self.entry_age_low = self.add_input_setting("Recent File Age (Days)", "organizer", "age_low_days")
        self.entry_age_high = self.add_input_setting("Old File Age (Days)", "organizer", "age_high_days")

        ctk.CTkLabel(self.scroll, text="Cleanup Defaults", font=("Roboto", 16, "bold")).pack(anchor="w", padx=10, pady=(20,5))
        
        self.entry_clean_size = self.add_input_setting("Cleanup Size Limit (MB)", "cleanup", "size_limit_mb")
        
        self.entry_clean_age = self.add_input_setting("Cleanup Age Limit (Days)", "cleanup", "age_limit_days")
                
        self.save_btn = ctk.CTkButton(self.scroll, text="Save Settings", fg_color=COLORS["accent"], text_color=COLORS["bg_sidebar"])
        self.save_btn.configure(command=self.save_settings)
        self.save_btn.pack(pady=30)
    
    def add_setting(self, label_text, default_val=True):
        f = ctk.CTkFrame(self.scroll, fg_color=COLORS["panel"])
        f.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(f, text=label_text).pack(
            side="left", padx=10, pady=10
        )

        switch = ctk.CTkSwitch(f, text="")
        switch.pack(side="right", padx=10, pady=10)

        if default_val:
            switch.select()

        return switch
    def add_input_setting(self, label_text, section, key):
        from config.Config_manager import ConfigManager
        cfg = ConfigManager.get_instance()
        
        f = ctk.CTkFrame(self.scroll, fg_color=COLORS["panel"])
        f.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(f, text=label_text).pack(side="left", padx=10, pady=10)

        entry = ctk.CTkEntry(f, width=80)
        entry.pack(side="right", padx=10, pady=10)
        
        current_val = cfg.get(section, key)
        if current_val is not None:
            entry.insert(0, str(current_val))
            
        return entry
    def save_settings(self):
        from config.Config_manager import ConfigManager
        cfg = ConfigManager.get_instance()

        cfg.set("general", "show_notifications", self.notify_switch.get())

        try:
            cfg.set("organizer", "size_low_mb", int(self.entry_size_low.get()))
            cfg.set("organizer", "size_high_mb", int(self.entry_size_high.get()))
            cfg.set("organizer", "age_low_days", int(self.entry_age_low.get()))
            cfg.set("organizer", "age_high_days", int(self.entry_age_high.get()))
            
            cfg.set("cleanup", "size_limit_mb", int(self.entry_clean_size.get()))
            cfg.set("cleanup", "age_limit_days", int(self.entry_clean_age.get()))

            print("Settings Saved Successfully!") 
            
        except ValueError:
            print("Error: Please enter valid whole numbers.")

class AutoFileProApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AutoFile Pro")
        self.geometry("900x500")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=COLORS["bg_sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(5, weight=1) 

        self.logo_label = ctk.CTkLabel(self.sidebar, text="AutoFile Pro", font=("Roboto", 20, "bold"), text_color="white")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.nav_buttons = {}
        self.create_nav_button("Organizer", self.show_organizer, 1)
        self.create_nav_button("Backup", self.show_backup, 2)
        self.create_nav_button("Cleanup", self.show_cleanup, 3)
        self.create_nav_button("Settings", self.show_settings, 4)

        self.version_label = ctk.CTkLabel(self.sidebar, text="v1.0.0 Alpha", text_color="gray")
        self.version_label.grid(row=6, column=0, padx=20, pady=20)

        self.frames = {
            "Organizer": OrganizerFrame(self),
            "Backup": BackupFrame(self),
            "Cleanup": CleanupFrame(self),
            "Settings": SettingsFrame(self)
        }
        
        self.show_organizer()

    def create_nav_button(self, text, command, row):
        btn = ctk.CTkButton(
            self.sidebar, 
            text=text, 
            fg_color="transparent", 
            text_color="gray", 
            hover_color=COLORS["panel"], 
            anchor="w",
            command=command,
            height=40
        )
        btn.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        self.nav_buttons[text] = btn

    def highlight_nav(self, active_name):
        for name, btn in self.nav_buttons.items():
            btn.configure(fg_color="transparent", text_color="gray")
        self.nav_buttons[active_name].configure(fg_color=COLORS["panel"], text_color="white")

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.grid_forget()
        
        self.frames[name].grid(row=0, column=1, sticky="nsew")
        self.highlight_nav(name)
    def show_success_notification(self, title, message):
        from config.Config_manager import ConfigManager
        cfg = ConfigManager.get_instance()
        
        if cfg.get("general", "show_notifications"):
            messagebox.showinfo(title, message)

    def show_organizer(self): self.show_frame("Organizer")
    def show_backup(self): self.show_frame("Backup")
    def show_cleanup(self): self.show_frame("Cleanup")
    def show_settings(self): self.show_frame("Settings")

if __name__ == "__main__":
    app = AutoFileProApp()
    app.mainloop()