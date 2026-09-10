"""local_job.py — worker render video cục bộ (chạy bằng venv python riêng).

Bot gọi worker này qua subprocess để không phụ thuộc playwright/edge-tts cài
trong python hệ thống của bot. Worker đọc job dir, render bằng pipeline
kaggle-pipeline (edge-tts + giọng mặc định), rồi ghi kết quả ra result.json.

Cách chạy (do bot gọi):
    <venv_python> -m telegram_bot.local_job <job_dir>
"""
import asyncio
import json
import sys
from pathlib import Path

JOB_DIR = Path(sys.argv[1])
PIPE_ROOT = Path(__file__).resolve().parent.parent.parent / "kaggle-pipeline"
SRC = PIPE_ROOT / "src"


async def main() -> int:
    meta = json.loads((JOB_DIR / "metadata.json").read_text(encoding="utf-8"))
    script_lines = meta["script_lines"]
    image_a = JOB_DIR / "image_a.jpg"
    image_b = JOB_DIR / "image_b.jpg"

    if not image_a.exists() or not image_b.exists():
        raise FileNotFoundError("Thiếu ảnh nhân vật A/B trong job dir.")

    sys.path.insert(0, str(SRC))
    from pipeline import generate_video_phase3

    assets = {
        "background": str(Path(__file__).resolve().parent / "assets" / "background.jpg"),
        "character": str(Path(__file__).resolve().parent / "assets" / "character.png"),
        "character_confused": str(Path(__file__).resolve().parent / "assets" / "character_confused.png"),
        "image_a": str(image_a),
        "image_b": str(image_b),
    }

    result = await generate_video_phase3(
        script_lines=script_lines,
        assets=assets,
        run_id=meta["run_id"],
        voice=meta.get("voice"),
    )

    (JOB_DIR / "result.json").write_text(
        json.dumps({"ok": True, "mp4": str(result)}, ensure_ascii=False),
        encoding="utf-8",
    )
    print("JOB_DONE", result)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(asyncio.run(main()))
    except Exception as e:  # noqa: BLE001 - ghi lỗi để bot đọc được
        (JOB_DIR / "result.json").write_text(
            json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"JOB_ERROR: {e}")
        raise SystemExit(1)