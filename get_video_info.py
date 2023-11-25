import os
import json
import csv
import re

from videoprops import get_video_properties, get_audio_properties
from pathlib import Path


PATH = r"Z:\Videos\Movies"
EXT = r"\.(?:mp4|mkv|avi|mpe?g|mov)$"


class VideoInfo:
    def __init__(self, location) -> None:
        self.location = location
        self.filename = Path(location).name
        self.folder = Path(location).parent
        self.parse()

    def parse(self):
        self.size_gb = round(os.path.getsize(self.location) / 1073741824, 2)

        try:
            vp = get_video_properties(self.location)
            self.video_codec = vp["codec_name"]
            self.width = vp["width"]
            self.height = vp["height"]
        except:
            pass

        try:
            ap = get_audio_properties(self.location)
            self.audio_codec = ap["codec_name"]
            self.channels = ap["channels"]
        except:
            pass

    def keys(self):
        return list(vars(self).keys())

    def to_dict(self):
        return vars(self)

    @property
    def size_gb(self):
        return self._size_gb

    @size_gb.setter
    def size_gb(self, size_gb):
        self._size_gb = size_gb

    @property
    def video_codec(self):
        return self._video_codec

    @video_codec.setter
    def video_codec(self, video_codec):
        self._video_codec = video_codec

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def audio_codec(self):
        return self._audio_codec

    @audio_codec.setter
    def audio_codec(self, audio_codec):
        self._audio_codec = audio_codec

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, channels):
        self._channels = channels


def build_video_data(path):
    """Returns video info for all videos found recursively in `path` as a list of dicts"""
    data = []

    # loop through path
    for root, dirs, files in os.walk(path):
        for file in files:
            if re.search(EXT, file, re.IGNORECASE):
                video_file = os.path.join(root, file)
                print(video_file)
                data.append(VideoInfo(video_file))
    return data


def video_data_to_csv(data, csv_out):
    """outputs `data` to a csv"""

    with open(csv_out, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in data:
            writer.writerow(row.to_dict())


if __name__ == "__main__":
    data = build_video_data(PATH)
    video_data_to_csv(data, "output.csv")
