import json
import os
import subprocess
import shutil

from ffmpeg_commands import FFmpegCommands
from pillow_commands import PillowCommands


class VideoEditor:

    def __init__(self, settings_path="settings.json"):

        self.settings = self.load_settings(settings_path)

        self.temp_dir = self._temp_dir()

        self.output = "output.mp4"

        self.process_videos = []

        if self.settings.get("dev", False):
            self.preset = "ultrafast"
            self.settings["normalize_audio"] = False
            self.settings["resolution"]["width"] = 540
            self.settings["resolution"]["height"] = 960
            self.settings["fps"] = 15

        else:
            self.preset = "medium"

    def _temp_dir(self):
        temp_dir = "temp"
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    def load_settings(self, settings_path):

        with open(settings_path, "r") as file:
            return json.load(file)

    def _run_command(self, command):

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:

            print(result.stderr)

            raise RuntimeError("Command failed.")

        return result

    def format_media(self):

        width = self.settings["resolution"]["width"]
        height = self.settings["resolution"]["height"]
        fps = self.settings["fps"]
        clips = self.settings["media"]["clips"]

        sorted_clips = sorted(clips, key=lambda x: x["order"])

        for index, clip in enumerate(sorted_clips):

            if clip.get("type") == "image":

                input_file = clip["file_name"]
                output_file = f"{self.temp_dir}/video_{index}.mp4"

                ken_burns = clip.get("ken_burns")

                if ken_burns:
                    PillowCommands.ken_burns(
                        input_file=input_file,
                        output_file=output_file,
                        effect=ken_burns.get("effect", "zoom_in"),
                        width=width,
                        height=height,
                        fps=fps,
                        duration=clip.get("duration", 3),
                        preset=self.preset,
                    )
                else:
                    command = FFmpegCommands.format_image(
                        input_file=input_file,
                        output_file=output_file,
                        width=width,
                        height=height,
                        fps=fps,
                        duration=clip.get("duration"),
                        text=clip.get("text"),
                        preset=self.preset,
                    )
                    self._run_command(command)

                self.process_videos.append(output_file)

            if clip.get("type") == "video":

                input_file = clip["file_name"]
                output_file = f"{self.temp_dir}/video_{index}.mp4"

                command = FFmpegCommands.format_video(
                    input_file=input_file,
                    output_file=output_file,
                    width=width,
                    height=height,
                    fps=fps,
                    start=clip.get("start"),
                    end=clip.get("end"),
                    text=clip.get("text"),
                    volume=clip.get("volume"),
                    speed=clip.get("speed"),
                    preset=self.preset,
                )
                self._run_command(command)

                self.process_videos.append(output_file)

    def merge_videos(self):

        audio_check = {}

        for video_path in self.process_videos:
            command = FFmpegCommands.check_audio(video_path)
            result = self._run_command(command)
            has_audio = bool(result.stdout.strip())
            audio_check[video_path] = has_audio

        if any(audio_check.values()):

            for file, has_audio in audio_check.items():

                if not has_audio:
                    _file = file.replace(".mp4", "_.mp4")
                    command = FFmpegCommands.add_silent_audio(file, _file)
                    self._run_command(command)

                    os.remove(file)
                    os.rename(_file, file)

        merged_file = f"{self.temp_dir}/merged.mp4"

        clips = self.settings["media"]["clips"]
        clips = sorted(clips, key=lambda x: x["order"])

        transitions = []

        for clip in clips[:-1]:
            transition = clip.get("transition")
            if transition:
                transitions.append(transition)

        if any(transitions):
            """
            in case of transition
            """

            has_no_transition = []

            for index, clip in enumerate(clips[:-1]):

                if not clip.get("transition"):
                    has_no_transition.append(self.process_videos[index])

            temp_paths = []
            process_videos_copy = self.process_videos.copy()

            for video_path in process_videos_copy:

                if video_path in has_no_transition:
                    temp_paths.append(video_path)
                    self.process_videos.remove(video_path)

                else:
                    if temp_paths:

                        temp_paths.append(video_path)

                        list_file = f"{self.temp_dir}/list.txt"

                        with open(list_file, "w") as f:
                            for _video_path in temp_paths:
                                f.write(f"file '{os.path.abspath(_video_path)}'\n")

                        _file = video_path.replace(".mp4", "_.mp4")
                        command = FFmpegCommands.merge(list_file, _file)
                        self._run_command(command)

                        os.remove(video_path)
                        os.rename(_file, video_path)

                        temp_paths = []

            durations = []

            for video_path in self.process_videos:
                command = FFmpegCommands.get_duration(video_path)
                result = self._run_command(command)
                duration = float(result.stdout.strip())
                durations.append(duration)

            command = FFmpegCommands.merge_with_transitions(
                file_list=self.process_videos,
                durations=durations,
                transitions=transitions,
                output_file=merged_file,
            )
            self._run_command(command)

            return merged_file

        else:
            """
            Now we are good to merge
            """

            list_file = f"{self.temp_dir}/list.txt"

            with open(list_file, "w") as f:
                for video_path in self.process_videos:
                    f.write(f"file '{os.path.abspath(video_path)}'\n")

            command = FFmpegCommands.merge(list_file, merged_file)
            self._run_command(command)

            return merged_file

    def add_background_music(self, video_file):

        audio_settings = self.settings.get("audio")
        if not audio_settings:
            return video_file

        audio_file = audio_settings["file_name"]
        volume = audio_settings.get("volume")
        fade_in = audio_settings.get("fade_in")
        fade_out = audio_settings.get("fade_out")

        output_file = f"{self.temp_dir}/with_music.mp4"

        command = FFmpegCommands.get_duration(video_file)
        result = self._run_command(command)
        duration = float(result.stdout.strip())

        command = FFmpegCommands.add_audio(
            video_file=video_file,
            audio_file=audio_file,
            volume=volume,
            output_file=output_file,
            duration=duration,
            fade_in=fade_in,
            fade_out=fade_out,
        )
        self._run_command(command)

        return output_file

    def normalize_final_audio(self, video_file):
        if not self.settings.get("normalize_audio"):
            return video_file

        output_file = f"{self.temp_dir}/normalized.mp4"
        command = FFmpegCommands.normalize_audio(video_file, output_file)
        self._run_command(command)
        return output_file

    def clean(self):
        shutil.rmtree(self.temp_dir)

    def render(self):
        self.format_media()
        output = self.merge_videos()
        output = self.add_background_music(output)
        output = self.normalize_final_audio(output)

        shutil.move(output, self.output)

        self.clean()
