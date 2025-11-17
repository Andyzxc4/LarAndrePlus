"""
Talking head video generation service powered by SadTalker.

This module keeps all filesystem paths contained inside the project and exposes
an easy-to-call Python API + FastAPI integration layer that can run on MPS
or CPU.  It assumes that the SadTalker repository + checkpoints live under
`vendors/SadTalker`.  Use `python tools/setup_talking_head.py` to install all
assets automatically.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

try:
    import torch  # type: ignore
except Exception:  # pragma: no cover - torch optional during import time
    torch = None  # type: ignore


@dataclass
class TalkingHeadStatus:
    ready: bool
    repo_dir: str
    checkpoints_present: bool
    device: str
    message: str


class TalkingHeadService:
    """
    Thin wrapper around the SadTalker CLI that hides all the boilerplate and
    exposes a Python-first API.
    """

    def __init__(
        self,
        project_root: Optional[str] = None,
        media_dir_name: str = "generated_media",
    ) -> None:
        self.project_root = Path(project_root or Path(__file__).resolve().parents[1])
        self.media_dir = self.project_root / media_dir_name / "talking_head"
        self.media_dir.mkdir(parents=True, exist_ok=True)

        self.vendors_dir = self.project_root / "vendors"
        self.repo_dir = self.vendors_dir / "SadTalker"
        self.inference_script = self.repo_dir / "inference.py"

        self.default_faces: Dict[str, Path] = {
            "andre": self.project_root / "faces" / "Andre.JPG",
            "lara": self.project_root / "faces" / "Lara.png",
        }

        self.device = self._detect_device()

    # --------------------------------------------------------------------- #
    # Helpers
    # --------------------------------------------------------------------- #
    def _detect_device(self) -> str:
        """
        Choose the best available device for SadTalker.  Preference order:
        1. value from TALKING_HEAD_DEVICE env variable (if valid)
        2. Apple MPS (Metal) if torch reports availability
        3. CPU fallback
        """
        requested = os.getenv("TALKING_HEAD_DEVICE", "").strip().lower()
        if requested in {"cpu", "mps"}:
            return requested

        if torch is not None:
            try:
                if torch.backends.mps.is_available():  # type: ignore[attr-defined]
                    return "mps"
            except Exception:
                pass

        return "cpu"

    def _checkpoints_present(self) -> bool:
        checkpoints_dir = self.repo_dir / "checkpoints"
        return checkpoints_dir.exists() and any(checkpoints_dir.iterdir())

    def status(self) -> TalkingHeadStatus:
        """
        Return a richer status payload for API + CLI consumers.
        """
        ready = self.inference_script.exists() and self._checkpoints_present()
        message = (
            "SadTalker ready"
            if ready
            else "Missing SadTalker repo or checkpoints. Run python tools/setup_talking_head.py"
        )
        return TalkingHeadStatus(
            ready=ready,
            repo_dir=str(self.repo_dir),
            checkpoints_present=self._checkpoints_present(),
            device=self.device,
            message=message,
        )

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def ensure_ready(self) -> None:
        status = self.status()
        if not status.ready:
            raise RuntimeError(status.message)

    def _resolve_face(self, character: str, custom_image: Optional[str]) -> Path:
        if custom_image:
            candidate = Path(custom_image).expanduser().resolve()
            if not candidate.exists():
                raise FileNotFoundError(f"Custom image not found: {candidate}")
            return candidate

        key = (character or "").lower().strip()
        if key not in self.default_faces:
            raise ValueError(
                f"Unknown character '{character}'. Use one of: {', '.join(self.default_faces)}"
            )

        face_path = self.default_faces[key]
        if not face_path.exists():
            raise FileNotFoundError(
                f"Default face image missing: {face_path}. Place an image inside faces/."
            )
        return face_path

    def generate_video(
        self,
        character: str,
        audio_path: str,
        *,
        custom_image: Optional[str] = None,
        expression_scale: float = 1.0,
        still_mode: bool = True,
    ) -> Path:
        """
        Generate a talking-head video for `character` using SadTalker.

        Returns the absolute path to the finalized MP4 inside generated_media/.
        """
        self.ensure_ready()

        audio_file = Path(audio_path).expanduser().resolve()
        if not audio_file.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        source_image = self._resolve_face(character, custom_image)

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        output_basename = f"{character.lower()}_{timestamp}.mp4"
        session_dir = Path(tempfile.mkdtemp(prefix="talking_head_", dir=self.media_dir))

        cmd = [
            sys.executable,
            str(self.inference_script),
            "--driven_audio",
            str(audio_file),
            "--source_image",
            str(source_image),
            "--result_dir",
            str(session_dir),
            "--preprocess",
            "full",
            "--expression_scale",
            str(expression_scale),
            "--device",
            self.device,
        ]

        if still_mode:
            cmd.append("--still")

        # We default to GFPGAN enhancer when downloaded.  It's optional.
        gfpgan_dir = self.repo_dir / "gfpgan"
        if gfpgan_dir.exists():
            cmd.extend(["--enhancer", "gfpgan"])
            cmd.extend(["--gfpgan_dir", str(gfpgan_dir)])

        process_env = os.environ.copy()
        # Make sure PyTorch gracefully falls back when MPS ops are missing.
        process_env.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

        subprocess.run(
            cmd,
            check=True,
            cwd=str(self.repo_dir),
            env=process_env,
        )

        mp4_candidates = sorted(session_dir.glob("*.mp4"), key=os.path.getmtime)
        if not mp4_candidates:
            raise RuntimeError("SadTalker finished but no MP4 was produced.")

        final_path = self.media_dir / output_basename
        shutil.move(str(mp4_candidates[-1]), final_path)
        shutil.rmtree(session_dir, ignore_errors=True)
        return final_path


__all__ = ["TalkingHeadService", "TalkingHeadStatus"]

