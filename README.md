# JSON Video Editor

A powerful and flexible programmatic video editor built with Python. This tool allows you to automate video editing workflows, apply precise visual and audio effects, and composite complex videos using structured JSON configurations or programmatic scripts.

---

## 🚀 Features Implemented

* **Merge Video Clips:** Seamlessly combine multiple video segments into a single cohesive output file.
* **Trim Video Clips:** Cut and extract specific start and end timestamps from media clips.
* **Background Audio:** Add custom background audio tracks to accompany your video project.
* **Normalize Audio:** Automatically balance and normalize audio levels across different clips for a professional sound.
* **Resolution Control:** Customize and scale output resolutions to fit specific formats (e.g., 1080p, 720p, vertical/horizontal).
* **FPS (Frames Per Second):** Adjust and standardize the frame rate of your output video.
* **Transitions:** Smoothly transition between video clips using built-in transition effects.
* **Clip Speed Control:** Speed up or slow down individual video clips for slow-motion or timelapse effects.
* **Image as a Clip:** Import and insert standalone static images directly into your video timeline.
* **Text Overlay:** Add custom text over your video with fully configurable display start and end times.
* **Per-Clip Volume Control:** Independently adjust the audio volume level for individual video clips.
* **Ken Burns Effects:** Apply cinematic panning and zooming motion effects to static images and clips.

---

## 🛠️ Tech Stack & Requirements

* **Python**
* **FFmpeg** (Required for video/audio processing backend)

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
```bash
git clone https://github.com/sajannepali328/Json-Video-Editor.git
cd "Video Editor"

```


2. **Install dependencies:**
Make sure you have your required Python packages and FFmpeg installed on your system.
3. **Configure your project:**
Ensure your `.gitignore` is set up to exclude local generated outputs and cache files (`media/`, `__pycache__/`, `output.mp4`).