import os
import csv
import re
import argparse
import pprint
from videoinfo import VideoInfo

PATH = r"Z:\Videos\Movies"
EXT = r"\.(?:mp4|mkv|avi|mpe?g|mov)$"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="full path of video file or folder")
    parser.add_argument("-r", "--resolution", action="store_true", help="returns video resolution")
    parser.add_argument("-a", "--audio", action="store_true", help="returns audio type")
    parser.add_argument("-f", "--folder", action="store_true", help="scans all videos in folder recursively")

    args = parser.parse_args()

    v = VideoInfo(args.file)
    
    if args.resolution:
        print(f"Resolution is {resolution(v.width, v.height)}")
    if args.audio:
        print(f"Audio is {audio_type(v.channels)}")
    else:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(v.to_dict())

        
    # data = build_video_data(PATH)
    # video_data_to_csv(data, "output.csv")


def resolution(w, h):
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


def audio_type(channels):
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
    main()
