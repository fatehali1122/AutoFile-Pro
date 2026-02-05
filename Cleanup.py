from pathlib import Path
import shutil
from send2trash import send2trash
import time
from Logger import setup_logger
from config.Config_manager import ConfigManager

class CleanupMode:
    def __init__(self,name : str, limit : int):
        self.name = name
        self.limit = limit
        
class Cleanup:

    def __init__(self, sourceFolder : Path):
        self.sourceFolder = sourceFolder
        self.fileCount = 0
        self.size = 0
        self.cleanup_files = []
        self.logger = setup_logger(sourceFolder,"Cleanup")
        self.cfg = ConfigManager.get_instance()
        cleanup_cfg = self.cfg.get("cleanup")

        if cleanup_cfg["mode"] == "size":
            self.mode = CleanupMode("size", cleanup_cfg["size_limit_mb"])

        elif cleanup_cfg["mode"] == "age":
            self.mode = CleanupMode("age", cleanup_cfg["age_limit_days"])
        self.protected_dirs = set(self.cfg.get("advanced", "protected_dirs"))

            
    def is_cleanup_file(self,file : Path):
        if file.is_dir() and file.name in self.protected_dirs:
            return False
        elif self.mode.name == "size":
            return (file.stat().st_size/(1024 * 1024)) > self.mode.limit
        elif self.mode.name == "age":
            currentTime = time.time()
            fileTime = file.stat().st_mtime
            return (currentTime - fileTime)/86400 > self.mode.limit
        else:
            return False

    def preview(self):
        self.fileCount = 0
        self.size = 0
        self.cleanup_files.clear()
        for file in self.sourceFolder.iterdir():
            if self.is_cleanup_file(file):
                self.fileCount += 1
                self.size += file.stat().st_size/(1024 * 1024)
                self.cleanup_files.append(file) 
        summary = {"count":self.fileCount,
                   "size":round(self.size,2)}
        self.logger.info("Preview generated successfully")
        return summary

    def move_to_recyclebin(self):
        for file in self.cleanup_files:
            self.logger.info(f"{file.name} Moved to Recycle Bin")
            send2trash(file)
        self.logger.info("Cleanup Done Successfully")

    def move_to_archive(self):
        archive_name = self.cfg.get("cleanup", "archive_folder")
        archive = self.sourceFolder / archive_name
        archive.mkdir(parents=True,exist_ok=True)
        self.logger.info("Archive Folder Created!")
        for file in self.cleanup_files:
            self.logger.info(f"{file.name} Moved to {archive}")
            shutil.move(file,archive)
        self.logger.info("Cleanup Done Successfully")

    def run_cleanup(self):
        self.logger.info("=" * 60)
        self.logger.info("Cleanup started")
        self.logger.info(f"Source folder: {self.sourceFolder}")
        self.logger.info(f"Mode: {self.mode.name}")
