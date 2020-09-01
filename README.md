# MovieReviews
## Description
An Mp3 player inspired by the Super Nintendo that allows all basic functionalities such as:
- Add
- Delete
- Play/Pause/Resume/Stop
- Queues (Add/Remove)

![Alt text](./gui.png?raw=true "Mp3 Player GUI")

## Technologies Used

**Built Using:**
- Python
- SqlAlchemy
- Flask
- Sqlite
- python-vlc


## Installation

You must have a VLC player installed already.

Installation instructions are for Python 3.

**Dependencies**

Install modules via `pip install -r requirements.txt`.

Or individually: 

```
pip install sqlalchemy
pip install flask
pip install requests
pip install eyed3
pip install python-vlc
```

## How to Use

Run both song_api.py and main_app_controller.py

**_Note_**

Tracks must have their **Artist** and **Title** details filled out for you to add songs to the mp3 player.
