Here is a complete, well-structured `README.md` for your GitHub repository that includes the configuration overview, the JSON schema example, setup instructions, and how an AI can easily interact with or generate configs for your editor.

---

# JSON Video Editor 🎬

A programmatic, JSON-driven video editor built with Python, FFmpeg, and Pillow. This tool allows you to automate video creation, apply Ken Burns effects to images, trim and speed up video clips, add text overlays, mix background music with audio fades, and apply smooth transitions between clips—all defined entirely through a simple JSON configuration file.

---

## Features

* **JSON-Driven Pipeline:** Define your entire video timeline, clips, text overlays, and audio tracks in a single configuration file.
* **Image & Video Support:** Mix images (with custom durations and Ken Burns effects) and video clips seamlessly.
* **Ken Burns & Effects:** Built-in Python/Pillow frame generation supporting `zoom_in`, `zoom_out`, `pan_right`, and `pan_left`.
* **Dynamic Text Overlays:** Custom font sizes, colors, positioning (`top`, `center`, `bottom`), and timestamp controls (`start`, `end`).
* **Transitions:** Supports FFmpeg `xfade` and `acrossfade` transitions like `fade`, `dissolve`, `wipeleft`, `circleopen`, and `slideup`.
* **Audio Mixing & Normalization:** Background music looping, volume adjustment, fade-in/fade-out support, and broadcast-standard loudness normalization (EBU R128).
* **Developer Mode (`dev`):** Instant toggle in settings to lower resolution, drop framerate, and use the `ultrafast` preset for rapid debugging and test renders.

---

## Project Structure

```text
├── main.py                # Main execution script
├── video_editor.py        # Core orchestration logic
├── ffmpeg_commands.py     # FFmpeg wrapper commands & filters
├── pillow_commands.py     # Pillow frame generation (Ken Burns)
├── settings.json          # Active project configuration
└── media/                 # Directory for your source assets (images, videos, music)

```

---

## ⚙️ Settings Configuration Schema

To create a new video project, configure your `settings.json` file. This layout is also fully structured so that AI assistants can easily read, write, or generate valid project files for you.

### Example `settings.json`

```json
{
    "resolution": {
        "width": 1080,
        "height": 1920
    },
    "fps": 30,
    "normalize_audio": true,
    "dev": false,
    "media": {
        "clips": [
            {
                "order": 1,
                "type": "image",
                "file_name": "media/your_image.jpg",
                "duration": 5,
                "text": {
                    "content": "Display Text",
                    "position": "center",
                    "font_size": 72,
                    "color": "white",
                    "start": 0,
                    "end": 5
                },
                "ken_burns": {
                    "effect": "zoom_in"
                },
                "transition": {
                    "type": "fade",
                    "duration": 0.5
                }
            },
            {
                "order": 2,
                "type": "video",
                "file_name": "media/your_video.mp4",
                "start": 0,
                "end": 5,
                "volume": 0.8,
                "text": {
                    "content": "Video Subtitle",
                    "position": "top",
                    "font_size": 40,
                    "color": "yellow"
                }
            }
        ]
    },
    "audio": {
        "file_name": "media/background_music.mp3",
        "volume": 0.2,
        "fade_in": 1.0,
        "fade_out": 2.0
    }
}

```

---

## Configuration Field Reference

* **`resolution`**: Target output dimensions (`width` and `height`).
* **`fps`**: Target frames per second for the rendered video.
* **`normalize_audio`**: Set to `true` to apply broadcast-standard audio leveling (loudnorm filter).
* **`dev`**: When `true`, automatically overrides resolution and framerate to lower values and uses the `ultrafast` preset for quick testing.
* **`media.clips`**: An array of objects representing each sequential piece of media ordered by `order`:
* `type`: Can be `"image"` or `"video"`.
* `file_name`: Path to the source asset.
* `duration` (Images only): How long the image frame should persist in seconds.
* `start` / `end` (Videos only): Trimming windows for source video clips.
* `text`: Optional overlay configuration (`content`, `position`, `font_size`, `color`, `start`, `end`).
* `ken_burns` (Images only): Animation effect (`zoom_in`, `zoom_out`, `pan_right`, `pan_left`).
* `transition`: Transition into the next clip (`type`, `duration`).


* **`audio`**: Global background track configuration (`file_name`, `volume`, `fade_in`, `fade_out`).

---

## Requirements & Installation

Make sure you have **Python**, **FFmpeg**, and **FFprobe** installed and available in your system's PATH.

1. Clone the repository:
```bash
git clone https://github.com/your-username/json-video-editor.git
cd json-video-editor

```


2. Install Python dependencies:
```bash
pip install pillow

```


3. Add your media assets into a folder named `media/` and modify your `settings.json` file accordingly.
4. Run the editor:
```bash
python main.py

```