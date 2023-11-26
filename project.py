import os
import csv
import re
import argparse
import json
from videoinfo import VideoInfo
from pathlib import Path

VALID_EXT_PATTERN = r"\.(?:mp4|mkv|avi|mpe?g|mov)$"
BYTES_IN_GB = 1073741824


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="full path of video file or folder")
    parser.add_argument(
        "-v", "--video", action="store_true", help="returns video quality"
    )
    parser.add_argument("-a", "--audio", action="store_true", help="returns audio type")
    parser.add_argument(
        "-f",
        "--folder",
        action="store_true",
        help="scans all videos in folder recursively",
    )

    args = parser.parse_args()

    if video_or_folder(args.path) == "Video":
        v = VideoInfo(args.path)

        if args.video:
            print(f"Resolution is {resolution(v.v_width, v.v_height)}")
        if args.audio:
            print(f"Audio is {audio_type(v.a_channels)}")
        else:
            print(json.dumps(pretty_video_info(v), indent=4))

    elif video_or_folder(args.path) == "Folder":
        folder_info(args.path)


def video_or_folder(path):
    if Path(path).is_file():
        if re.search(VALID_EXT_PATTERN, path, re.IGNORECASE):
            return "Video"
        else:
            return None
    if Path(path).is_dir():
        return "Folder"


def resolution(w: int, h: int):
    try:
        if w <= 792 and h <= 528:
            return "480p"
        elif w <= 792 and h <= 634:
            return "576p"
        elif w <= 1408 and h <= 792:
            return "720p"
        elif w <= 2112 and h <= 1188:
            return "1080p"
        elif w <= 2816 and h <= 1584:
            return "1440p"
        elif w <= 4224 and h <= 2376:
            return "4KUHD"
        elif w <= 4506 and h <= 2376:
            return "DCI4K"
        elif w <= 8448 and h <= 5752:
            return "4KUHD"
        else:
            return None

    except TypeError:
        return None


def audio_type(channels: int):
    try:
        if channels == 1:
            return "Mono"
        elif 1 < channels < 5:
            return "Stereo"
        elif channels >= 5:
            return "Surround"
        else:
            return None

    except TypeError:
        return None


def pretty_video_info(v: VideoInfo):
    return {
        "filename": v.filename,
        "folder": v.folder,
        "size_gb": round(os.path.getsize(v.location) / BYTES_IN_GB, 2),
        "video_quality": resolution(v.v_width, v.v_height),
        "video_codec": v.v_codec_name,
        "audio_type": audio_type(v.a_channels),
        "audio_codec": v.a_codec_name,
    }


def folder_info(path, print_screen=True):
    """Returns video info for all videos found recursively in `path` as a list of dicts"""
    data = []

    # loop through path
    for root, dirs, files in os.walk(path):
        for file in files:
            if re.search(VALID_EXT_PATTERN, file, re.IGNORECASE):
                video_file = os.path.join(root, file)
                vi = pretty_video_info(VideoInfo(video_file))
                if print_screen:
                    print("\n", json.dumps(vi, indent=4))
                data.append(vi)
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
    main()
