import project


def test_resolution():
    assert project.resolution(3836, 2072) == "4KUHD"
    assert project.resolution(1920, 1080) == "1080p"
    assert project.resolution(1920, 796) == "1080p"
    assert project.resolution(1280, 720) == "720p"
    assert project.resolution(720, 400) == "480p"
    assert project.resolution(10000, 10000) == None
    assert project.resolution("dog", "cat") == None


def test_audio_type():
    assert project.audio_type(1) == "Mono"
    assert project.audio_type(2) == "Stereo"
    assert project.audio_type(4) == "Stereo"
    assert project.audio_type(5) == "Surround"
    assert project.audio_type(99) == "Surround"
    assert project.audio_type(0) == None
    assert project.audio_type(-1) == None
    assert project.audio_type("dog") == None
