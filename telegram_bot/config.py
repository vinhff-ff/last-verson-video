"""Config: đọc biến môi trường từ .env, cung cấp hằng số toàn cục."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(Path(__file__).resolve().parent / ".env")
load_dotenv(BASE_DIR / ".env")


def _required(name: str) -> str:
    val = os.getenv(name, "").strip()
    if not val:
        raise SystemExit(f"Thiếu biến môi trường bắt buộc: {name} (xem telegram_bot/env.example)")
    return val


BOT_TOKEN = _required("BOT_TOKEN")

BASE_DIR = Path(__file__).resolve().parent.parent
JOBS_DIR = BASE_DIR / "telegram_bot" / "jobs"
ASSETS_DIR = BASE_DIR / "telegram_bot" / "assets"

# Pipeline (kaggle-pipeline/src) + thư mục venv để chạy render local.
# Bot render qua subprocess bằng venv python này để không cần cài
# playwright/edge-tts vào python hệ thống của bot.
LOCAL_VENV_PYTHON = os.getenv(
    "LOCAL_VENV_PYTHON",
    str(BASE_DIR / "kaggle-pipeline" / ".venv" / "bin" / "python"),
)

# Asset cố định dùng lại cho mọi video (phục vụ trực tiếp từ máy local).
# image_a/image_b được bot tải từ 2 ảnh nhân vật user gửi theo từng job.
FIXED_ASSETS = ["background.jpg", "character.png", "character_confused.png"]

# Giọng TTS mặc định (edge-tts, miễn phí, chạy local): nam miền Bắc.
DEFAULT_VOICE = os.getenv("DEFAULT_VOICE", "vi-VN-NamMinhNeural")