import os
from dataclasses import dataclass
from pathlib import Path
@dataclass(frozen=True)
class Settings:
    mode: str = "demo"
    origins: tuple[str,...] = ("http://localhost:5173", "http://127.0.0.1:5173")
    media_root: Path = Path("media")
    @classmethod
    def from_env(cls):
        mode = os.getenv("APP_MODE", "demo")
        if mode not in {"demo", "development"}: raise ValueError("unsupported APP_MODE; production needs persistence/auth")
        return cls(mode=mode,origins=tuple(x.strip() for x in os.getenv("CORS_ORIGINS", ",".join(cls.origins)).split(",") if x.strip()),
            media_root=Path(os.getenv("MEDIA_ROOT","media")))
