---
name: c-pi-ai-video-studio
description: Create and edit branded videos from user-provided footage with Remotion and React. Use for C Pi Media or client reels, LinkedIn videos, testimonials, social ads, explainers, highlight cuts, subtitles, aspect-ratio variants, motion graphics, previews, and MP4 rendering.
---

# C Pi AI Video Studio

Turn a brief and supplied clips into a reviewable, reproducible Remotion video project, then render approved deliverables. Follow official Remotion guidance and the user's actual brand brief; never invent client branding or claim a render succeeded without checking the resulting file.

## Workflow

1. **Intake.** Confirm goal, target audience, platform, required duration, orientation, language, call to action, assets, and whether the edit may use licensed music or stock material. If unspecified, propose a 30-second, 9:16 social cut with restrained business-friendly styling; ask before making consequential creative assumptions.
2. **Inspect.** Inventory footage, audio, fonts, logos, and reference samples. Probe each clip's resolution, frame rate, duration, rotation, codec, and audio track with `ffprobe` or Remotion's media tools. Flag corrupt or poor-quality shots. Keep originals unchanged.
3. **Storyboard.** Draft a timecoded shot list with source file, in/out points, purpose, on-screen text, caption treatment, transition, and audio plan. Prioritize a strong first 2–3 seconds; avoid unverified claims. Present for approval when the brief is open-ended.
4. **Build.** Prefer an existing Remotion project. Otherwise create an isolated Remotion app following current official instructions. Avoid committing large client videos by default. Implement compositions as React components with frame-based timing, sequences, deterministic animations, and explicit dimensions/FPS. Keep client configuration separate from generic components.
5. **Captions and sound.** Transcribe only when speech exists and tooling is available. Review names and timing; never fabricate transcripts. Duck music under speech, avoid clipping, and use assets with appropriate rights.
6. **Review.** Launch Remotion Studio or render a low-resolution preview/contact sheet. Inspect the opening, transitions, captions, CTA, logo, aspect-ratio crops, audio, and blank frames. Seek approval before the final render when relevant.
7. **Render.** Render the requested format (normally H.264 MP4), inspect command status and output with `ffprobe`, and verify dimensions, duration, and audio. Deliver the rendered file, source project, and edit summary. If rendering is unavailable, provide editable code and identify what remains unverified.

## Remotion implementation rules

- Check [Remotion's official agent skills](https://www.remotion.dev/docs/ai/skills) and current documentation before selecting APIs. Follow project-local Remotion skills for creation, markup, captions, Studio, rendering, and upgrades when present.
- Prefer `npx create-video@latest` for an empty project, subject to network/runtime approval. Do not clone the full Remotion monorepo merely to make a client video.
- Use `staticFile()` for local assets in `public/` when appropriate and Remotion media components compatible with installed versions.
- Preserve footage aspect ratio by intentional crop or letterbox. Never stretch video or place key text outside safe margins.
- Use frame-based `Sequence` or `Series` timing. Derive durations from verified clips and in/out points.
- Make B2B motion restrained by default. Ensure animations are deterministic across renders.
- Separate text, branding, clip timing, and export format from generic reusable components. Keep secrets and client private media out of public repositories.
- Check [Remotion licensing](https://www.remotion.dev/license) before commercial work; company licensing may be necessary.

## Output presets

| Preset | Resolution | Default FPS | Typical use |
|---|---|---|---|
| Vertical | 1080×1920 | 30 | Reels, Shorts, Stories |
| Square | 1080×1080 | 30 | Social feed |
| Landscape | 1920×1080 | 30 | LinkedIn, website, YouTube |

Use current platform requirements and source footage to choose actual FPS, codec, and safe areas; these are starting defaults.

## Brand and client boundaries

- For Creative Pi Media, use the customer-facing name **C Pi Media**. Request approved logo, fonts, colors, and slogan; do not assume colors from unrelated client projects.
- Isolate brand configuration by client. Never reuse another client's private footage, artwork, or unapproved claims.
- Seek approval before AI-generated scenes, synthetic voices, fabricated testimonials, copyrighted music, or third-party stock.
- Do not publish externally or spend on rendering services without authorization.

Read [references/brief-and-qa.md](references/brief-and-qa.md) for the intake, storyboard, export, and handoff checklists.
