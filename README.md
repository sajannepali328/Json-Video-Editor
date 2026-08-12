# JSON Video Editor 🎬

A lightweight Python tool that automates video editing and rendering through a single `settings.json` configuration file.

## Features

1. **Resolution Settings**
   * Configurable output width and height.

2. **FPS (Frames Per Second)**
   * Adjustable framerate for the rendered video.

3. **Clip Management & Processing**
   * **Clip Merging:** Combine multiple video and image clips sequentially based on an assigned order.
   * **Trimming:** Set custom start and end times for video clips.
   * **Speed Control:** Modify playback speed per clip.
   * **Text Overlays:** Add custom text with configurable content, font size, color, position, and start/end timestamps.
   * **Transitions:** Smoothly transition between clips using customizable effects and durations.
   * **Per-Clip Volume:** Control audio levels individually for each video clip.

4. **Background Audio**
   * Add a background music track with custom volume levels.
   * Configurable audio fade-in and fade-out durations.

5. **Audio Normalization**
   * Optional broadcast-standard audio normalization (EBU R128) for the final mix.
