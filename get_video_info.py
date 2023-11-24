from videoprops import get_video_properties, get_audio_properties
import os
import json
import csv
import re

PATH = r"Z:\Videos\Movies"
EXT = r"\.(?:mp4|mkv|avi|mpe?g|mov)$"


def build_video_data(path):
    """Returns video info for all videos found recursively in `path` as a list of dicts"""
    data = []

    # loop through path
    for root, dirs, files in os.walk(path):
        for file in files:
            if re.search(EXT, file, re.IGNORECASE):
                print(os.path.join(root, file))
                row = {
                    "folder": root,
                    "filename": file,
                    "size_gb": round(
                        os.path.getsize(os.path.join(root, file)) / 1073741824, 2
                    ),
                }

                try:
                    vp = get_video_properties(os.path.join(root, file))
                    row["video_codec"] = vp["codec_name"]
                    row["width"] = vp["width"]
                    row["height"] = vp["height"]
                except:
                    pass

                try:
                    ap = get_audio_properties(os.path.join(root, file))
                    row["audio_codec"] = ap["codec_name"]
                    row["channels"] = ap["channels"]
                except:
                    pass
                # print(json.dumps(vp, indent=2))
                # print(json.dumps(ap, indent=2))
                data.append(row)
    return data


def video_data_to_csv(data, csv_out):
    """outputs `data` to a csv"""

    with open(csv_out, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in data:
            writer.writerow(row)


if __name__ == "__main__":
    data = build_video_data(PATH)
    video_data_to_csv(data, "output.csv")
