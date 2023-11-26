import os
from project import *
from videoinfo import VideoInfo


def test_resolution():
    assert quality_from_res(3836, 2072) == "4KUHD"
    assert quality_from_res(1920, 1080) == "1080p"
    assert quality_from_res(1920, 796) == "1080p"
    assert quality_from_res(1280, 720) == "720p"
    assert quality_from_res(720, 400) == "480p"
    assert quality_from_res(10000, 10000) == None
    assert quality_from_res("dog", "cat") == None


def test_audio_type():
    assert audio_type(1) == "Mono"
    assert audio_type(2) == "Stereo"
    assert audio_type(4) == "Stereo"
    assert audio_type(5) == "Surround"
    assert audio_type(99) == "Surround"
    assert audio_type(0) == None
    assert audio_type(-1) == None
    assert audio_type("dog") == None


def test_video_or_folder():
    assert video_or_folder("sample_video/") == "Folder"
    assert (
        video_or_folder("sample_video/sample__480__libx264__aac__30s__video.mp4")
        == "Video"
    )
    assert video_or_folder(os.path.realpath(__file__)) == None
    assert video_or_folder("/path/that/doesnt/exist") == None


def test_pretty_video_info():
    assert pretty_video_info(
        VideoInfo("sample_video/sample__1080__libx264__aac__30s__video.mp4")
    ) == {
        "filename": "sample__1080__libx264__aac__30s__video.mp4",
        "folder": "sample_video",
        "size_gb": 0.02,
        "video_quality": "1080p",
        "video_codec": "h264",
        "audio_type": "Stereo",
        "audio_codec": "aac",
    }
