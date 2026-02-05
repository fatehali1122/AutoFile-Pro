from pathlib import Path
import tomllib
import tomli_w


class ConfigManager:
    _instance = None

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.data = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            config_path = Path(__file__).parent / "autofile.toml"
            cls._instance = cls(config_path)
            cls._instance.load()
        return cls._instance

    def load(self):
        if not self.config_path.exists():
            self._create_default_config()

        with open(self.config_path, "rb") as f:
            self.data = tomllib.load(f)

    def reload(self):
        self.load()

    def save(self):
        with open(self.config_path, "wb") as f:
            tomli_w.dump(self.data, f)

    def get(self, section: str, key: str | None = None):
        if key is None:
            return self.data.get(section, {})
        return self.data.get(section, {}).get(key)

    def set(self, section: str, key: str, value):
        if section not in self.data:
            self.data[section] = {}
        self.data[section][key] = value
        self.save()

    # ------------------ DEFAULT CONFIG ------------------

    def _create_default_config(self):
        self.data = {
            "general": {
                "default_mode": "extension"
            },

            "organizer": {
                "mode": "extension",          # extension | size | age
                "size_low_mb": 10,
                "size_high_mb": 100,
                "age_low_days": 7,
                "age_high_days": 30
            },

            "backup": {
                "default_folder": "backups",
                "compress": True
            },

            "cleanup": {
                "mode": "size",               # size | age
                "size_limit_mb": 100,
                "age_limit_days": 30,
                "archive_folder": "archives"
            },

            "logging": {
                "log_dir": "logs",
                "level": "INFO"
            },

            "advanced": {
                "protected_dirs": [
                    "documents", "images", "videos", "audios",
                    "code_files", "others",
                    "small", "large", "very_large",
                    "recent", "old", "very_old"
                ],
                "extension_groups": {
                    "documents": [".txt", ".docx", ".pdf", ".csv"],
                    "images": [".jpg", ".png"],
                    "videos": [".mp4", ".mkv", ".webm", ".mov", ".wmv"],
                    "audios": [".mp3", ".m4a", ".wav"],
                    "code_files": [
                        ".py", ".cpp", ".java", ".js", ".php",
                        ".html", ".css", ".qss", ".xml", ".json"
                    ]
                }
            }
        }
        self.save()
