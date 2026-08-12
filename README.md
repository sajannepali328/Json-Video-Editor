```markdown
# JSON Video Editor 🎬

A simple Python tool that allows you to edit and render videos using a single `settings.json` file. 

## Features
* **Merge & Trim:** Combine multiple video and image clips with custom start/end times.
* **Ken Burns Effect:** Apply smooth zoom-in, zoom-out, or panning effects to images.
* **Text Overlays:** Add customized text with specific positions and timeframes.
* **Transitions:** Smoothly transition between clips using fade, dissolve, and more.
* **Audio Control:** Adjust clip volumes, mix background music with fade effects, and normalize final audio.

---

## Getting Started

### 1. Requirements
Make sure you have **Python**, **FFmpeg**, and **FFprobe** installed on your system and added to your PATH.

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone [https://github.com/sajannepali328/Json-Video-Editor.git](https://github.com/sajannepali328/Json-Video-Editor.git)
cd Json-Video-Editor
pip install pillow

```

### 3. Usage

1. Place your media files (videos, images, music) inside a folder named `media/`.
2. Configure your project in `settings.json`.
3. Run the editor:

```bash
python test.py

```

Your rendered video will be saved as `output.mp4`.

---

## Example `settings.json`

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
        "file_name": "media/intro.jpg",
        "duration": 4,
        "text": {
          "content": "Welcome",
          "position": "center",
          "font_size": 72,
          "color": "white",
          "start": 0,
          "end": 4
        },
        "ken_burns": {
          "effect": "zoom_in"
        },
        "transition": {
          "type": "fade",
          "duration": 0.5
        }
      }
    ]
  },
  "audio": {
    "file_name": "media/music.mp3",
    "volume": 0.3,
    "fade_in": 2.0,
    "fade_out": 3.0
  }
}

```