# AI Video Comparison Tool

Personal tool to auto-generate A-vs-B comparison videos, chạy hoàn toàn local
(không cần Kaggle/GPU).

Luồng: kịch bản 10-15 câu (do AI ngoài viết, JSON) + 2 ảnh nhân vật A/B
-> designer map visual -> edge-tts (giọng NamMinh mặc định) -> HTML/CSS/JS
-> Playwright/Chromium record -> FFmpeg -> final.mp4

## Cấu trúc

```
tol/
├── kaggle-pipeline/   # pipeline render video local
└── telegram-bot/      # bot Telegram điều khiển pipeline
```

## Chạy (lần đầu)

```bash
bash kaggle-pipeline/setup_local.sh   # venv + playwright/chromium + edge-tts
sudo apt-get install -y ffmpeg        # thiếu ffmpeg thì render lỗi
```

## Chạy bot

```bash
cd telegram-bot
cp telegram_bot/env.example telegram_bot/.env   # điền token bot
setsid nohup python3 -m telegram_bot.bot >> bot.log 2>&1 < /dev/null &
```

## Test pipeline trực tiếp (không qua bot)

```bash
cd kaggle-pipeline && .venv/bin/python src/pipeline.py
```
