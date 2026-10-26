# Fantigo Living — Local video renderer

This project recreates the full property-tour video using the five original clips in their numbered sequence. It adds timecoded amenity labels and exports a vertical MP4. **Client footage is not included in this public GitHub repository.**

## One-time setup

1. Install [Python 3](https://www.python.org/downloads/) and [FFmpeg](https://ffmpeg.org/download.html). Ensure `python` (or `python3`), `ffmpeg`, and `ffprobe` work in a terminal. On Windows, add FFmpeg's `bin` folder to PATH.
2. Download this repository to your computer, or use Git to clone it.
3. In the `fantigo-living` folder, create a folder named `media`.
4. Put your five original files in `media`, with these exact names: `1(1).mp4`, `2(1).mp4`, `3(1).mp4`, `4(2).mp4`, `5.mp4`.

Do not upload the clips to GitHub. The `.gitignore` in this folder excludes the footage and renders.

## Render

From the `fantigo-living` folder, run:

```bash
python render.py
```

On systems where Python is `python3`, run `python3 render.py` instead.

Output: `output/Fantigo_Living_Full_Property_Tour.mp4`

To create a smaller file, run:

```bash
python render.py --crf 31 --output output/Fantigo_Living_Smaller.mp4
```

The export defaults to 720×1280, 30 fps, H.264 video with AAC audio. Rendering all five full clips takes a few minutes depending on hardware.

## Edit text or timing

Edit `project.json`:

- `clips`: clip order. Preserve the listed order for the requested tour.
- `labels`: `clip` is 1–5; `start` and `end` are seconds **within that source clip**, not in the final merged timeline.
- `text`, `size`, `y`, and `bold`: on-screen label appearance.
- `crf`: video quality. Lower is better quality/larger file; 24 is the default.

For nonstandard fonts, supply a font path:

```bash
python render.py --font-file "C:\\Windows\\Fonts\\arial.ttf" --bold-font-file "C:\\Windows\\Fonts\\arialbd.ttf"
```

The script probes each input, warns if the soundtrack is missing, validates label timing against clip duration, and checks the rendered video. It neither uploads media nor accesses any online service.
