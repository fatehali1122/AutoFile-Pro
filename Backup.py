from pathlib import Path
import shutil
from Logger import setup_logger
from datetime import datetime
from config.Config_manager import ConfigManager


class Backup:
    def __init__(self, sourceFolder:Path, destinationFolder:Path):
        self.sourceFolder = sourceFolder
        self.fileCount = 0
        self.folderCount = 0
        self.size = 0
        self.cfg = ConfigManager.get_instance()
        backup_cfg = self.cfg.get("backup")
        if destinationFolder is None:
            default_backup_dir = backup_cfg["default_folder"]
            self.destinationFolder = self.sourceFolder.parent / default_backup_dir
            self.destinationFolder.mkdir(parents=True, exist_ok=True)
        else:
            self.destinationFolder = destinationFolder
        self.compress = backup_cfg["compress"]
        timeStamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S") + "_Backup"
        self.temp_folder = self.destinationFolder/timeStamp
        self.temp_folder.mkdir(parents=True,exist_ok=True)
        self.proceedAfterCopy = False
        self.logger = setup_logger(sourceFolder,"Backup")

    def preview(self):
        self.fileCount = 0
        self.folderCount = 0
        self.size = 0
        for file in self.sourceFolder.rglob("*"):
            if file.is_dir():
                self.folderCount += 1
            else:
                self.fileCount +=1
                self.size += file.stat().st_size
        self.size = (self.size)/(1024*1024)

        summary = {"files": self.fileCount,
                   "folders": self.folderCount,
                   "size": round(self.size,2),
                   "src": str(self.sourceFolder),
                   "dst": str(self.destinationFolder)
        }
        self.logger.info("Preview generated successfully")
        return summary
    
    def copyData(self):
        shutil.copytree(self.sourceFolder,self.temp_folder,dirs_exist_ok=True)
        self.logger.info(f"Data Successfully Copied to Temp Folder {self.temp_folder.name}")

    def compressing(self):
        if self.compress == True:
            shutil.make_archive(f"{str(self.temp_folder)}","zip",self.temp_folder)
            self.logger.info(f"{self.temp_folder.name} Compressed Successfully")
 
    def del_tempFolder(self):
        shutil.rmtree(self.temp_folder)
        self.logger.info(f"Temp Folder Deleted.")
    
    def run_Backup(self):
        self.logger.info("=" * 60)
        self.logger.info("Backup started")
        self.logger.info(f"Source folder: {self.sourceFolder}")
        self.logger.info(f"Destination folder: {self.destinationFolder}")
        self.preview()
        self.copyData()
        if self.compress:
            self.compressing()
            self.del_tempFolder()
            self.logger.info("Backup Created Successfully !")
        else:
            self.logger.info("Backup Cancelled")