from song import Song

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base

engine = create_engine('sqlite:///' + 'song_db.sqlite')
Base.metadata.bind = engine
db_session = sessionmaker(bind=engine)


def main():

    song1 = Song('thank u, next', 'Ariana Grande', '3:02', r"C:\Users\royeo\Desktop\CIT Term 2\ACIT 2515 - Object Oriented Programming\Week 9 - Copy\Music\Ariana Grande - thank u next.mp3", 'thank u, next')
    song1.rating = 6
    song1.increment_usage_stats()
    print(song1.get_description())

    session = db_session()
    session.add(song1)

    session.commit()

    song_id = song1.song_id
    session.close()
    # print(library1)
    # library1.add_audio_file(song1)
    # print(library1)
    # library1.remove_audio_file(song1)
    # print(library1)


if __name__ == "__main__":
    main()