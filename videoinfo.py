import os
import re
from videoprops import get_video_properties, get_audio_properties
from pathlib import Path

VALID_EXT_PATTERN = r"\.(?:mp4|mkv|avi|mpe?g|mov)$"


class VideoInfo:
    def __init__(self, location) -> None:
        self.location = location
        self.filename = Path(location).name
        self.folder = Path(location).parent
        self.parse()

    def __str__(self) -> str:
        return str(vars(self))

    def is_video(self):
        if Path(self.location).is_file():
            if re.search(VALID_EXT_PATTERN, self.location, re.IGNORECASE):
                return True
        return False

    def parse(self):
        try:
            self.size = os.path.getsize(self.location)
            self.size_gb = os.path.getsize(self.location) / 1073741824
        except FileNotFoundError:
            self.size = None
            self.size_gb = None

        try:
            vp = get_video_properties(self.location)
            self.video_codec = vp["codec_name"]
            self.width = vp["width"]
            self.height = vp["height"]
        except:
            self.video_codec = None
            self.width = None
            self.height = None

        try:
            ap = get_audio_properties(self.location)
            self.audio_codec = ap["codec_name"]
            self.channels = ap["channels"]
        except:
            self.audio_codec = None
            self.channels = None

    def keys(self):
        return list(vars(self).keys())

    def to_dict(self):
        return vars(self)

    @property
    def size_gb(self):
        return self._size_gb

    @size_gb.setter
    def size_gb(self, size_gb):
        try:
            self._size_gb = round(size_gb, 2)
        except TypeError:
            self._size_gb = None

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        try:
            self._height = int(height)
        except (ValueError, TypeError):
            self._height = None

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        try:
            self._width = int(width)
        except (ValueError, TypeError):
            self._width = None

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, channels):
        try:
            self._channels = channels
        except (ValueError, TypeError):
            self._channels = None
