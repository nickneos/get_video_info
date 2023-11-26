import os
import re
import json
from videoprops import get_video_properties, get_audio_properties
from pathlib import Path

VALID_EXT_PATTERN = r"\.(?:mp4|mkv|avi|mpe?g|mov)$"


class VideoInfo:
    def __init__(self, location) -> None:
        self.location = location
        self.filename = str(Path(location).name)
        self.folder = str(Path(location).parent)
        # self.parse()

        try:
            self.size = os.path.getsize(self.location)
        except FileNotFoundError:
            self.size = None

        for key, value in get_video_properties(self.location).items():
            setattr(self, "v_" + key, value)

        for key, value in get_audio_properties(self.location).items():
            setattr(self, "a_" + key, value)

    def __str__(self) -> str:
        return str(json.dumps(vars(self), indent=2))

    def is_video(self):
        if Path(self.location).is_file():
            if re.search(VALID_EXT_PATTERN, self.location, re.IGNORECASE):
                return True
        return False

    # def parse(self):
    #     try:
    #         self.size = os.path.getsize(self.location)
    #     except FileNotFoundError:
    #         self.size = None

    #     try:
    #         vp = get_video_properties(self.location)
    #         self.video_codec = vp["codec_name"]
    #         self.width = vp["width"]
    #         self.height = vp["height"]
    #     except:
    #         self.video_codec = None
    #         self.width = None
    #         self.height = None

    #     try:
    #         ap = get_audio_properties(self.location)
    #         self.audio_codec = ap["codec_name"]
    #         self.channels = ap["channels"]
    #     except:
    #         self.audio_codec = None
    #         self.channels = None

    # def keys(self):
    #     return list(vars(self).keys())

    # def to_dict(self):
    #     return vars(self)

    # @property
    # def height(self):
    #     return self._height

    # @height.setter
    # def height(self, height):
    #     try:
    #         self._height = int(height)
    #     except (ValueError, TypeError):
    #         self._height = None

    # @property
    # def width(self):
    #     return self._width

    # @width.setter
    # def width(self, width):
    #     try:
    #         self._width = int(width)
    #     except (ValueError, TypeError):
    #         self._width = None

    # @property
    # def channels(self):
    #     return self._channels

    # @channels.setter
    # def channels(self, channels):
    #     try:
    #         self._channels = channels
    #     except (ValueError, TypeError):
    #         self._channels = None


if __name__ == "__main__":
    vi = VideoInfo(r"Z:\Videos\Movies\LEGO Marvel Super Heroes Black Panther - Trouble in Wakanda (2018)\LEGO Marvel Super Heroes - Black Panther - Trouble in Wakanda (2018) 720p WEBRip [Dual Audio].mkv")
    print(vi)