from PIL import Image
import subprocess


class PillowCommands:

    @staticmethod
    def ken_burns(
        input_file,
        output_file,
        effect,
        width,
        height,
        fps,
        duration,
        preset,
    ):
        img = Image.open(input_file).convert("RGB")
        img_w, img_h = img.size

        scale = 1.3
        scaled_w = int(img_w * scale)
        scaled_h = int(img_h * scale)
        img = img.resize((scaled_w, scaled_h), Image.LANCZOS)

        total_frames = int(fps * duration)

        encode_command = [
            "ffmpeg", "-y",
            "-f", "rawvideo",
            "-vcodec", "rawvideo",
            "-s", f"{width}x{height}",
            "-pix_fmt", "rgb24",
            "-r", str(fps),
            "-i", "pipe:0",
            "-c:v", "libx264",
            "-preset", preset,
            "-pix_fmt", "yuv420p",
            output_file,
        ]

        process = subprocess.Popen(encode_command, stdin=subprocess.PIPE)

        for i in range(total_frames):
            t = i / (total_frames - 1)

            if effect == "zoom_in":
                crop_w = int(scaled_w / (1 + 0.3 * t))
                crop_h = int(scaled_h / (1 + 0.3 * t))
                crop_x = (scaled_w - crop_w) // 2
                crop_y = (scaled_h - crop_h) // 2

            elif effect == "zoom_out":
                crop_w = int(scaled_w / (1.3 - 0.3 * t))
                crop_h = int(scaled_h / (1.3 - 0.3 * t))
                crop_x = (scaled_w - crop_w) // 2
                crop_y = (scaled_h - crop_h) // 2

            elif effect == "pan_right":
                crop_w = width
                crop_h = height
                crop_x = int((scaled_w - width) * t)
                crop_y = (scaled_h - height) // 2

            elif effect == "pan_left":
                crop_w = width
                crop_h = height
                crop_x = int((scaled_w - width) * (1 - t))
                crop_y = (scaled_h - height) // 2

            else:
                crop_w, crop_h = scaled_w, scaled_h
                crop_x, crop_y = 0, 0

            frame = img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
            frame = frame.resize((width, height), Image.LANCZOS)
            process.stdin.write(frame.tobytes())

        process.stdin.close()
        process.wait()