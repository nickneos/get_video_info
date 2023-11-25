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

    def __str__(self) -> str:
        return str(vars(self))

    def parse(self):
        self.size_gb = os.path.getsize(self.location) / 1073741824

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
        except ValueError:
            self._height = None

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        try:
            self._width = int(width)
        except ValueError:
            self._width = None

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, channels):
        try:
            self._channels = channels
        except ValueError:
            self._channels = None


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
