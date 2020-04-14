
from song import Song


def main():

    song1 = Song('thank u, next', 'Ariana Grande', '3:02', r".\Music\Ariana Grande - thank u next.mp3", 'thank u, next')
    song1.user_rating = 6
    song1.increment_usage_stats()
    print(song1.get_description())
    # print(library1)
    # library1.add_audio_file(song1)
    # print(library1)
    # library1.remove_audio_file(song1)
    # print(library1)


if __name__ == "__main__":
    main()