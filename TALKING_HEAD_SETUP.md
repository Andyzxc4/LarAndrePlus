# 🎬 Talking-Head Generator (SadTalker)

Everything you need to animate Andre or Lara locally on macOS (MPS or CPU).

## 1. Requirements

- macOS 13+ (Apple Silicon preferred, Intel works with CPU)
- Python 3.10+
- `ffmpeg` (`brew install ffmpeg`)
- Virtual environment with the project `requirements.txt` installed

Optional but recommended:

- `export PYTORCH_ENABLE_MPS_FALLBACK=1` to gracefully fall back when an op
  is missing on MPS.

## 2. One-Time Setup

```bash
cd /Users/lara/dre-proj-git/LarAndrePlus
source venv/bin/activate
pip install -r requirements.txt
python tools/setup_talking_head.py
```

The setup script:
- Creates `vendors/SadTalker`
- Downloads the official checkpoints + GFPGAN enhancers
- Keeps everything inside the repo so it works offline

## 3. Generate a Video from CLI

```bash
python tools/generate_talking_head.py \
    --character lara \
    --audio /path/to/lara-tts.wav
```

Flags:
- `--image /custom/path.png` to override the default face
- `--expression-scale 1.3` to exaggerate lip motion
- `--no-still` to allow full head movement

Output file: `generated_media/talking_head/lara_<timestamp>.mp4`  
Public URL: `http://localhost:8000/media/talking_head/<filename>.mp4`

## 4. Generate via API

```bash
curl -X POST http://localhost:8000/talking-head \
  -F "character=andre" \
  -F "expression_scale=1.0" \
  -F "audio_file=@/path/to/andre.wav"
```

Response:

```json
{
  "character": "andre",
  "filename": "andre_20241117_153015.mp4",
  "video_url": "/media/talking_head/andre_20241117_153015.mp4",
  "device": "mps"
}
```

Check readiness at any time:

```bash
curl http://localhost:8000/talking-head/status
```

## 5. Choosing the Device

Order of preference:
1. `TALKING_HEAD_DEVICE` env var (`mps` or `cpu`)
2. Apple Metal (MPS) if available
3. CPU fallback

Examples:

```bash
# Force CPU
export TALKING_HEAD_DEVICE=cpu

# Force Metal
export TALKING_HEAD_DEVICE=mps
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

## 6. Feeding TTS Audio

You can use any TTS provider. Tips:
- Ensure audio is clean mono/stereo `.wav` or `.mp3`
- Trim leading/trailing silence to reduce video render time
- Keep clips short (5–15 seconds) for faster SadTalker turnaround

## 7. Troubleshooting

| Issue | Fix |
| --- | --- |
| `SadTalker finished but no MP4 was produced` | Verify audio file plays correctly and that checkpoints are in `vendors/SadTalker/checkpoints`. |
| `ModuleNotFoundError: torch` | Re-run `pip install -r requirements.txt` inside the active virtual environment. |
| `RuntimeError: Missing SadTalker repo or checkpoints` | Run `python tools/setup_talking_head.py --force`. |
| Video looks blurry | Install `ffmpeg` from Homebrew and rerun generation (GFPGAN enhancer relies on it). |

Happy animating! 💃🕺

