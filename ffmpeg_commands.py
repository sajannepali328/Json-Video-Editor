class FFmpegCommands:

    @staticmethod
    def test():
        return "test successful"

    @staticmethod
    def _escape_text(text):
        """
        Escape characters that break ffmpeg's drawtext filter syntax.
        """
        return (
            text.replace("\\", "\\\\")
            .replace(":", "\\:")
            .replace("'", "\\'")
            .replace(",", "\\,")
        )

    @staticmethod
    def _build_drawtext(text_settings):
        """
        Builds a drawtext filter string from a clip's "text" settings dict.
        Returns None if text_settings is falsy.
        """
        if not text_settings:
            return None

        content = FFmpegCommands._escape_text(text_settings["content"])
        font_size = text_settings.get("font_size", 48)
        color = text_settings.get("color", "white")
        position = text_settings.get("position", "bottom")

        position_map = {
            "top": "x=(w-text_w)/2:y=60",
            "center": "x=(w-text_w)/2:y=(h-text_h)/2",
            "bottom": "x=(w-text_w)/2:y=h-text_h-60",
        }
        pos = position_map.get(position, position_map["bottom"])

        drawtext = (
            f"drawtext=text='{content}':"
            f"fontsize={font_size}:"
            f"fontcolor={color}:"
            f"{pos}:"
            f"box=1:boxcolor=black@0.4:boxborderw=10"
        )

        start = text_settings.get("start")
        end = text_settings.get("end")
        if start is not None and end is not None:
            drawtext += f":enable='between(t,{start},{end})'"

        return drawtext

    @staticmethod
    def format_video(
        input_file,
        output_file,
        width,
        height,
        fps,
        start,
        end,
        text,
        volume,
        speed,
        preset,
    ):
        """
        Builds the FFmpeg command dynamically using the provided parameters.
        """

        # Construct the video filter chain with dynamic width, height, and fps
        vf_filter = (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
            f"fps={fps}"
        )

        if speed:
            vf_filter += f",setpts=PTS/{speed}"

        drawtext = FFmpegCommands._build_drawtext(text)
        if drawtext:
            vf_filter += f",{drawtext}"

        command = ["ffmpeg", "-y"]

        if start is not None:
            command += ["-ss", str(start)]

        command += ["-i", input_file]

        if end is not None:
            duration = end - (start or 0)
            command += ["-t", str(duration)]

        command += ["-vf", vf_filter]

        if volume is not None:
            command += ["-af", f"volume={volume}"]

        command += [
            "-c:v",
            "libx264",
            "-preset",
            preset,
            "-crf",
            "23",
            "-c:a",
            "aac",
            output_file,
        ]

        return command

    @staticmethod
    def check_audio(input_file):

        command = [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a",
            "-show_entries",
            "stream=index",
            "-of",
            "csv=p=0",
            input_file,
        ]

        return command

    @staticmethod
    def add_silent_audio(input_file, output_file):
        command = [
            "ffmpeg",
            "-y",
            "-i",
            input_file,
            "-f",
            "lavfi",
            "-i",
            f"anullsrc=channel_layout=stereo:sample_rate=44100",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-shortest",
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            output_file,
        ]

        return command

    @staticmethod
    def merge(file_list, output_file):
        command = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            file_list,
            "-c:v",
            "libx264",
            "-crf",
            "23",
            "-c:a",
            "aac",
            output_file,
        ]
        return command

    @staticmethod
    def format_image(
        input_file,
        output_file,
        width,
        height,
        fps,
        duration,
        text,
        preset,
    ):

        vf_filter = (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
            f"fps={fps}"
        )

        drawtext = FFmpegCommands._build_drawtext(text)
        if drawtext:
            vf_filter += f",{drawtext}"

        command = [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            input_file,
            "-vf",
            vf_filter,
            "-t",
            str(duration),
            "-c:v",
            "libx264",
            "-preset",
            preset,
            "-pix_fmt",
            "yuv420p",
            "-r",
            str(fps),
            output_file,
        ]

        return command

    @staticmethod
    def add_audio(
        video_file,
        audio_file,
        volume,
        output_file,
        duration,
        fade_in,
        fade_out,
    ):
        """
        Mixes a background music track under the video's existing audio.
        Music is trimmed/looped to match the video's duration automatically.
        """

        if fade_in and fade_out:
            fade_out_start = duration - fade_out
            filter_complex = (
                f"[1:a]volume={volume},"
                f"aloop=loop=-1:size=2e9,"
                f"afade=t=in:st=0:d={fade_in},"
                f"afade=t=out:st={fade_out_start}:d={fade_out}"
                f"[music];"
                f"[0:a][music]amix=inputs=2:duration=first:dropout_transition=0[aout]"
            )
        else:
            filter_complex = (
                f"[1:a]volume={volume},aloop=loop=-1:size=2e9[music];"
                f"[0:a][music]amix=inputs=2:duration=first:dropout_transition=0[aout]"
            )

        command = [
            "ffmpeg",
            "-y",
            "-i",
            video_file,
            "-i",
            audio_file,
            "-filter_complex",
            filter_complex,
            "-map",
            "0:v",
            "-map",
            "[aout]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            output_file,
        ]

        return command

    @staticmethod
    def get_duration(input_file):
        command = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            input_file,
        ]
        return command

    @staticmethod
    def merge_with_transitions(file_list, durations, transitions, output_file):

        inputs = []
        for f in file_list:
            inputs += ["-i", f]

        n = len(file_list)
        filter_parts = []

        prev_v_label = "0:v"
        prev_a_label = "0:a"
        cumulative = durations[0]

        for i in range(1, n):
            transition = transitions[i - 1]

            v_out = f"v{i}"
            a_out = f"a{i}"

            t_type = transition.get("type", "fade")
            t_duration = transition["duration"]
            offset = cumulative - t_duration

            filter_parts.append(
                f"[{prev_v_label}][{i}:v]xfade=transition={t_type}:"
                f"duration={t_duration}:offset={offset}[{v_out}]"
            )
            filter_parts.append(
                f"[{prev_a_label}][{i}:a]acrossfade=d={t_duration}[{a_out}]"
            )
            cumulative += durations[i] - t_duration

            prev_v_label = v_out
            prev_a_label = a_out

        filter_complex = ";".join(filter_parts)

        command = [
            "ffmpeg",
            "-y",
            *inputs,
            "-filter_complex",
            filter_complex,
            "-map",
            f"[{prev_v_label}]",
            "-map",
            f"[{prev_a_label}]",
            "-c:v",
            "libx264",
            "-crf",
            "23",
            "-c:a",
            "aac",
            output_file,
        ]

        return command

    @staticmethod
    def normalize_audio(input_file, output_file):
        """
        Normalizes loudness to a broadcast-standard level (EBU R128).
        Useful for clips recorded at very different volumes.
        """
        command = [
            "ffmpeg",
            "-y",
            "-i",
            input_file,
            "-af",
            "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:v",
            "copy",
            output_file,
        ]
        return command
