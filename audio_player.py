from time import sleep
import vlc
import os


# os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

def play_stuff(mp3_file):
    """Tests some methods"""
    player = vlc.MediaPlayer(mp3_file)
    player.play()
    sleep(25)
    player.pause()
    sleep(3)
    player.pause()
    sleep(5)
    player.stop()

if __name__ == "__main__":
    mp3_file = "./Music/Ariana Grande - thank u next.mp3"
    play_stuff(mp3_file)
