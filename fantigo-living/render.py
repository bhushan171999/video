#!/usr/bin/env python3
"""Render the Fantigo Living tour locally. Requires FFmpeg and no Python packages."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run(command, *, capture=False):
    return subprocess.run(command, check=True, text=True, capture_output=capture)


def probe(path):
    data = json.loads(run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,width,height", "-of", "json", str(path)
    ], capture=True).stdout)
    return {
        "duration": float(data["format"]["duration"]),
        "video": any(s["codec_type"] == "video" for s in data.get("streams", [])),
        "audio": any(s["codec_type"] == "audio" for s in data.get("streams", [])),
    }


def font_files(args):
    candidates = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
        ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"),
    ]
    regular, bold = next(((a, b) for a, b in candidates if Path(a).exists() and Path(b).exists()), (None, None))
    regular = args.font_file or regular
    bold = args.bold_font_file or bold
    if not regular or not bold or not Path(regular).is_file() or not Path(bold).is_file():
        raise RuntimeError("Fonts not found. Supply --font-file and --bold-font-file paths.")
    return regular, bold


def escape_filter_value(value):
    """Escape text for FFmpeg's nested filtergraph/drawtext parsing."""
    return str(value).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace(",", "\\,").replace("[", "\\[").replace("]", "\\]")


def create_filter(config, infos, fonts):
    width, height, fps = (int(config[key]) for key in ("width", "height", "fps"))
    parts = []
    for i, _ in enumerate(infos):
        parts.append(
            f"[{i}:v]fps={fps},scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,setpts=PTS-STARTPTS[v{i}]"
        )
        parts.append(f"[{i}:a]aresample=48000,volume={float(config['audio_volume'])},asetpts=PTS-STARTPTS[a{i}]")
    inputs = "".join(f"[v{i}][a{i}]" for i in range(len(infos)))
    parts.append(f"{inputs}concat=n={len(infos)}:v=1:a=1[base][aud]")

    offsets = [0.0]
    for info in infos:
        offsets.append(offsets[-1] + info["duration"])
    regular, bold = fonts
    filters = []
    for label in config["labels"]:
        clip_index = int(label["clip"]) - 1
        if clip_index < 0 or clip_index >= len(infos):
            raise ValueError(f"Invalid clip number: {label['clip']}")
        start, end = float(label["start"]), float(label["end"])
        if start < 0 or start >= end or end > infos[clip_index]["duration"] + 0.1:
            raise ValueError(f"Label outside clip {clip_index + 1}: {label['text']}")
        absolute_start, absolute_end = offsets[clip_index] + start, offsets[clip_index] + end
        font = bold if label.get("bold", True) else regular
        # Pass font paths as safely escaped FFmpeg filter values, including Windows colons.
        filters.append(
            "drawtext="
            f"fontfile='{escape_filter_value(font)}':"
            f"text='{escape_filter_value(label['text'])}':"
            f"fontsize={int(label.get('size', 35))}:fontcolor=white:"
            f"x=38:y={int(label.get('y', 1080))}:"
            "box=1:boxcolor=0x152f35@0.72:boxborderw=18:"
            f"enable='between(t,{absolute_start:.3f},{absolute_end:.3f})'"
        )
    parts.append("[base]" + ",".join(filters) + "[outv]")
    return ";\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "project.json")
    parser.add_argument("--media-dir", type=Path, default=ROOT / "media")
    parser.add_argument("--output", type=Path, default=ROOT / "output" / "Fantigo_Living_Full_Property_Tour.mp4")
    parser.add_argument("--crf", type=int, help="Override quality (18 high quality; 31 smaller size)")
    parser.add_argument("--font-file", type=str)
    parser.add_argument("--bold-font-file", type=str)
    args = parser.parse_args()
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        parser.error("Install FFmpeg and ensure ffmpeg and ffprobe are on PATH.")
    config = json.loads(args.config.read_text(encoding="utf-8"))
    sources = [args.media_dir / filename for filename in config["clips"]]
    missing = [str(p) for p in sources if not p.is_file()]
    if missing:
        parser.error("Missing private clips in media folder: " + ", ".join(missing))
    infos = [probe(p) for p in sources]
    if not all(i["video"] and i["audio"] for i in infos):
        parser.error("Every input must have a video and audio stream. Supply audio or adjust the script before rendering.")
    fonts = font_files(args)
    filter_text = create_filter(config, infos, fonts)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    filter_file = args.output.parent / "render_filter.txt"
    filter_file.write_text(filter_text, encoding="utf-8")
    command = ["ffmpeg", "-y", "-hide_banner", "-i", str(sources[0])]
    for source in sources[1:]:
        command.extend(["-i", str(source)])
    command.extend([
        "-filter_complex_script", str(filter_file),
        "-map", "[outv]", "-map", "[aud]", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", str(args.crf if args.crf is not None else config["crf"]),
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart", "-shortest", str(args.output)
    ])
    print("Rendering", len(sources), "clips in the specified order...", flush=True)
    run(command)
    info = probe(args.output)
    if not info["video"] or not info["audio"] or info["duration"] < sum(i["duration"] for i in infos) - 1:
        raise RuntimeError("Render verification failed")
    print(f"Ready: {args.output} ({info['duration']:.1f} seconds, {args.output.stat().st_size / 1048576:.1f} MiB)")


if __name__ == "__main__":
    try:
        main()
    except (subprocess.CalledProcessError, ValueError, RuntimeError, KeyError) as exc:
        print("ERROR:", exc, file=sys.stderr)
        sys.exit(1)
