from pathlib import Path
import shutil
from datetime import datetime
import time
from Logger import setup_logger
from config.Config_manager import ConfigManager

class OrganizerMode:
    def __init__(self,name:str,low=None,high=None):
        self.name = name
        self.low = low
        self.high = high
        
class Organizer:
    
    def __init__(self,sourceFolder : Path):
        self.sourceFolder = sourceFolder
        self.logger = setup_logger(sourceFolder,"Organizer")
        self.cfg = ConfigManager.get_instance()
        org_cfg = self.cfg.get("organizer")
        mode_name = org_cfg["mode"]

        if mode_name == "extension":
            self.mode = OrganizerMode("extension")

        elif mode_name == "size":
            self.mode = OrganizerMode(
                "size",
                org_cfg["size_low_mb"],
                org_cfg["size_high_mb"]
            )

        elif mode_name == "age":
            self.mode = OrganizerMode(
                "age",
                org_cfg["age_low_days"],
                org_cfg["age_high_days"]
            )

        else:
            raise ValueError("Invalid organizer mode")
        self.protected_dirs = set(self.cfg.get("advanced", "protected_dirs"))
        self.extension_groups = self.cfg.get("advanced", "extension_groups")

    def preview(self):
        if(self.mode.name == "extension"):
            docCount = 0
            imageCount = 0
            videoCount = 0
            codefilesCount = 0
            audioCount = 0
            othersCount = 0
            for file in self.sourceFolder.iterdir():

                if file.is_dir() or file.name in self.protected_dirs:
                    continue

                elif file.suffix in self.extension_groups["documents"]:
                    docCount += 1                
                    
                elif file.suffix in self.extension_groups["images"]:
                    imageCount += 1
                
                elif file.suffix in self.extension_groups["videos"]:
                    videoCount += 1

                elif file.suffix in self.extension_groups["audios"]:
                    audioCount += 1

                elif file.suffix in self.extension_groups["code_files"]:
                    codefilesCount += 1
                else:
                    othersCount += 1
            summary_ext = {"mode" : self.mode.name,
                       "src" : self.sourceFolder,
                       "docs" : docCount,
                       "images" : imageCount,
                       "videos" : videoCount,
                       "audios" : audioCount,
                       "codes" : codefilesCount,
                       "others" : othersCount}

            return summary_ext

        elif self.mode.name == "size":
            smallCount = 0
            largeCount = 0
            v_largeCount = 0
            for file in self.sourceFolder.iterdir():
                fileSize = (file.stat().st_size)/(1024 * 1024)

                if file.is_dir() or file.name in self.protected_dirs:
                    continue
                elif fileSize < self.mode.low:
                    smallCount += 1
                elif fileSize >= self.mode.low and fileSize < self.mode.high:
                    largeCount += 1
                elif fileSize >= self.mode.high:
                    v_largeCount += 1
            summary_size = {"mode" : self.mode.name,
                            "src": self.sourceFolder,
                            "small": smallCount,
                            "large": largeCount,
                            "very_large": v_largeCount} 
            return summary_size
                
        elif self.mode.name == "age":
            recentCount = 0
            oldCount = 0
            v_oldCount = 0
            current_time = time.time()
            for file in self.sourceFolder.iterdir():
                fileTime = file.stat().st_mtime
                if file.is_dir() or file.name in self.protected_dirs:
                    print(f"Skipped! {file.name} is a Folder\n")
                    continue

                elif (current_time - fileTime)/86400 < self.mode.low:
                    recentCount += 1
                
                elif (current_time - fileTime)/86400 >= self.mode.low and (current_time - fileTime)/86400 < self.mode.high:
                    oldCount += 1

                elif (current_time - fileTime)/86400 >= self.mode.high:
                    v_oldCount += 1

            summary_age = {"mode" : self.mode.name,
                            "src": self.sourceFolder,
                            "recent": recentCount,
                            "old": oldCount,
                            "very_old": v_oldCount} 
            return summary_age
            
        self.logger.info("Preview generated successfully")

    def checkDuplicate(self,src:Path,dst:Path):
        for file in dst.iterdir():
            if file.name == src.name:
                return True
            else:
                continue
        return False

    def renameFile(self,file: Path, dst : Path):
        fileNewName = f"{file.stem}_{datetime.now().strftime("%Y-%m-%d")}{file.suffix}"

        return dst / fileNewName
    
    def organizeByExtension(self):
        for file in self.sourceFolder.iterdir():

            if file.is_dir() or file.name in self.protected_dirs:
                self.logger.debug(f"Skipped protected directory: {file.name}")
                continue

            elif file.suffix in self.extension_groups["documents"]:
                documents = self.sourceFolder / "documents/"
                documents.mkdir(parents=True, exist_ok=True)

                if self.checkDuplicate(file,documents):
                    self.logger.warning(f"Duplicate detected: {file.name} in {documents}")
                    dest = self.renameFile(file,documents)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {documents}")

                else:    
                    shutil.move(file,documents)
                    self.logger.info(f"{file.name} Successfully moved to -> {documents}")
                
            elif file.suffix in self.extension_groups["images"]:
                images = self.sourceFolder / "images/"
                images.mkdir(parents=True, exist_ok=True)
                if self.checkDuplicate(file,images):
                    self.logger.warning(f"Duplicate detected: {file.name} in {images}")
                    dest = self.renameFile(file,images)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {images}")
                else:
                    shutil.move(file,images)
                    self.logger.info(f"{file.name} Successfully moved to -> {images}")
    
            elif file.suffix in self.extension_groups["videos"]:
                videos = self.sourceFolder / "videos/"
                videos.mkdir(parents=True, exist_ok=True)
                if self.checkDuplicate(file,videos):
                    self.logger.warning(f"Duplicate detected: {file.name} in {videos}")
                    dest = self.renameFile(file,videos)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {videos}")
                else:
                    shutil.move(file,videos)
                    self.logger.info(f"{file.name} Successfully moved to -> {videos}")

            elif file.suffix in self.extension_groups["audios"]:
                audio = self.sourceFolder / "audios/"
                audio.mkdir(parents=True, exist_ok=True)
                if self.checkDuplicate(file,audio):
                    self.logger.warning(f"Duplicate detected: {file.name} in {audio}")
                    dest = self.renameFile(file,audio)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {audio}")
                else:
                    shutil.move(file,audio)
                    self.logger.info(f"{file.name} Successfully moved to -> {audio}")

            elif file.suffix in self.extension_groups["code_files"]:
                code = self.sourceFolder / "code_files/"
                code.mkdir(parents=True, exist_ok=True)
                if self.checkDuplicate(file,code):
                    self.logger.warning(f"Duplicate detected: {file.name} in {code}")
                    dest = self.renameFile(file,code)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {code}")
                else:
                    shutil.move(file,code)
                    self.logger.info(f"{file.name} Successfully moved to -> {code}")

            else:
                other = self.sourceFolder / "others/"
                other.mkdir(parents=True, exist_ok=True)
                if self.checkDuplicate(file,other):
                    self.logger.warning(f"Duplicate detected: {file.name} in {other}")
                    dest = self.renameFile(file,other)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {other}")
                else:
                    shutil.move(file,other)
                    self.logger.info(f"{file.name} Successfully moved to -> {other}")
                
        self.logger.info(f"All Files in {self.sourceFolder} are Organized by Extensions!")
        
    def organizeBySize(self):
        for file in self.sourceFolder.iterdir():
            fileSize = (file.stat().st_size)/(1024 * 1024)
            if file.is_dir() or file.name in self.protected_dirs:
                self.logger.debug(f"Skipped protected directory: {file.name}")
                continue

            elif fileSize < self.mode.low:
                small = self.sourceFolder / "small/"
                small.mkdir(parents=True,exist_ok=True)
                if self.checkDuplicate(file,small):
                    self.logger.warning(f"Duplicate detected: {file.name} in {small}")
                    dest = self.renameFile(file,small)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {small}")
                else:
                    shutil.move(file,small)
                    self.logger.info(f"{file.name} Successfully moved to -> {small}")
                
            elif fileSize >= self.mode.low and fileSize < self.mode.high:
                large = self.sourceFolder /"large/"
                large.mkdir(parents=True,exist_ok=True)
                if self.checkDuplicate(file,large):
                    self.logger.warning(f"Duplicate detected: {file.name} in {large}")
                    dest = self.renameFile(file,large)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {large}")
                else:
                    shutil.move(file,large)
                    self.logger.info(f"{file.name} Successfully moved to -> {large}")

            elif fileSize >= self.mode.high:
                veryLarge = self.sourceFolder / "very_large/"
                veryLarge.mkdir(parents=True,exist_ok=True)
                if self.checkDuplicate(file,veryLarge):
                    self.logger.warning(f"Duplicate detected: {file.name} in {veryLarge}")
                    dest = self.renameFile(file,veryLarge)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {veryLarge}")
                else:
                    shutil.move(file,veryLarge)
                    self.logger.info(f"{file.name} Successfully moved to -> {veryLarge}")

        self.logger.info(f"All Files in {self.sourceFolder} are Organized by Size!")
    
    def organizeByAge(self):
        current_time = time.time()
        for file in self.sourceFolder.iterdir():
            fileTime = file.stat().st_mtime
            if file.is_dir() or file.name in self.protected_dirs:
                self.logger.debug(f"Skipped protected directory: {file.name}")
                continue

            elif (current_time - fileTime)/86400 < self.mode.low:
                recent = self.sourceFolder / "recent/"
                recent.mkdir(parents=True,exist_ok=True)

                if self.checkDuplicate(file,recent):
                    self.logger.warning(f"Duplicate detected: {file.name} in {recent}")
                    dest = self.renameFile(file,recent)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {recent}")
                else:
                    shutil.move(file,recent)
                    self.logger.info(f"{file.name} Successfully moved to -> {recent}")

                
            elif (current_time - fileTime)/86400 >= self.mode.low and (current_time - fileTime)/86400 < self.mode.high:
                old = self.sourceFolder /"old/"
                old.mkdir(parents=True,exist_ok=True)
                if self.checkDuplicate(file,old):
                    self.logger.warning(f"Duplicate detected: {file.name} in {old}")
                    dest = self.renameFile(file,old)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {old}")
                else:
                    shutil.move(file,old)
                    self.logger.info(f"{file.name} Successfully moved to -> {old}")

            elif (current_time - fileTime)/86400 >= self.mode.high:
                veryOld = self.sourceFolder / "very_old/"
                veryOld.mkdir(parents=True,exist_ok=True)
                if self.checkDuplicate(file,veryOld):
                    self.logger.warning(f"Duplicate detected: {file.name} in {veryOld}")
                    dest = self.renameFile(file,veryOld)
                    self.logger.info(f"Renamed {file.name} -> {dest.name}")
                    shutil.move(file,dest)
                    self.logger.info(f"{dest.name} Successfully moved to -> {veryOld}")
                else:
                    shutil.move(file,veryOld)
                    self.logger.info(f"{file.name} Successfully moved to -> {veryOld}")

        self.logger.info(f"All Files in {self.sourceFolder} are Organized by Age!")
    
    def run_organizer(self):
        self.logger.info("=" * 60)
        self.logger.info("Organizer started")
        self.logger.info(f"Mode selected: {self.mode.name}")
        self.logger.info(f"Source folder: {self.sourceFolder}") 
        self.preview()
        if self.mode.name == "extension":
            self.organizeByExtension()
        elif self.mode.name == "size":
            self.organizeBySize()
        elif self.mode.name == "age":
            self.organizeByAge()
        else:
            self.logger.warning("User cancelled the organizing process")