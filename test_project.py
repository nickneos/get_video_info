import project
import os


def test_resolution():
    assert project.quality_from_res(3836, 2072) == "4KUHD"
    assert project.quality_from_res(1920, 1080) == "1080p"
    assert project.quality_from_res(1920, 796) == "1080p"
    assert project.quality_from_res(1280, 720) == "720p"
    assert project.quality_from_res(720, 400) == "480p"
    assert project.quality_from_res(10000, 10000) == None
    assert project.quality_from_res("dog", "cat") == None


def test_audio_type():
    assert project.audio_type(1) == "Mono"
    assert project.audio_type(2) == "Stereo"
    assert project.audio_type(4) == "Stereo"
    assert project.audio_type(5) == "Surround"
    assert project.audio_type(99) == "Surround"
    assert project.audio_type(0) == None
    assert project.audio_type(-1) == None
    assert project.audio_type("dog") == None


def test_video_or_folder():
    assert project.video_or_folder(os.path.dirname(os.path.realpath(__file__))) == "Folder"
    assert project.video_or_folder(r"c:\path\that\doesnt\exist") == None
    # assert project.video_or_folder(r"c:\path\to\video.mp4") == "Video"
    assert project.video_or_folder(os.path.realpath(__file__)) == None
