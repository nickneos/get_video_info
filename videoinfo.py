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

    def to_dict(self):
        return vars(self)

    @property
    def v_height(self):
        return self._height

    @v_height.setter
    def v_height(self, h):
        try:
            self._height = int(h)
        except (ValueError, TypeError):
            self._height = None

    @property
    def v_width(self):
        return self._width

    @v_width.setter
    def v_width(self, w):
        try:
            self._width = int(w)
        except (ValueError, TypeError):
            self._width = None
