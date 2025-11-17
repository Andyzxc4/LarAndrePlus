#!/usr/bin/env python3
"""
CLI helper to create a talking-head video from an audio file.

Example:
    python tools/generate_talking_head.py \\
        --character lara \\
        --audio /path/to/tts-output.wav
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = PROJECT_ROOT / "backend"

sys.path.insert(0, str(BACKEND_DIR))

from talking_head_service import TalkingHeadService  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a talking-head video using SadTalker.")
    parser.add_argument(
        "--character",
        choices=["andre", "lara"],
        required=True,
        help="Whose face should be animated.",
    )
    parser.add_argument(
        "--audio",
        required=True,
        help="Path to the TTS audio file (.wav or .mp3).",
    )
    parser.add_argument(
        "--image",
        default=None,
        help="Optional custom image path. Defaults to faces/Andre.JPG or faces/Lara.png.",
    )
    parser.add_argument(
        "--expression-scale",
        type=float,
        default=1.0,
        help="Higher values exaggerate lip motion (default: 1.0).",
    )
    parser.add_argument(
        "--no-still",
        action="store_true",
        help="Disable SadTalker's --still flag for full-head motion.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    service = TalkingHeadService(project_root=str(PROJECT_ROOT))
    video_path = service.generate_video(
        character=args.character,
        audio_path=args.audio,
        custom_image=args.image,
        expression_scale=args.expression_scale,
        still_mode=not args.no_still,
    )

    print("✅ Talking-head video generated!")
    print(f"   Character:  {args.character}")
    print(f"   Audio:      {Path(args.audio).resolve()}")
    print(f"   Saved to:   {video_path}")
    print(f"   Device:     {service.device.upper()}")
    print(f"   Serve via:  http://localhost:8000/media/talking_head/{video_path.name}")


if __name__ == "__main__":
    main()

