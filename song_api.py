from flask import Flask, request
from song_manager import SongManager
from song import Song
import json
import random

app = Flask(__name__)

song_mgr = SongManager('song_db.sqlite')


@app.route('/song', methods=['POST'])
def add_song():
    """ Add a song to the database    """
    content = request.json

    try:
        song = Song(content['title'],
                        content['artist'],
                        content['runtime'],
                        content['path_name'],
                        content['album'],
                        content['genre'])
        song_mgr.add_song(song)

        response = app.response_class(
                status=200
        )
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=400
        )
    return response


@app.route('/song/<string:id>', methods=['GET'])
def get_song(id):
    """ Get a song from the database """
    try:
        song = song_mgr.get_song(id)
        if song is None:
            raise ValueError(f"Song {id} does not exist")

        response = app.response_class(
                status=200,
                response=json.dumps(song.meta_data()),
                mimetype='application/json'
        )
        return response
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=404
        )
        return response


@app.route('/song/random', methods=['GET'])
def random_song():
    """ Return a random song from the database """
    try:
        names = song_mgr.get_all_songs()

        if len(names) > 0:
            idx = random.randint(0, len(names) - 1)
            random_song = names[idx]
        else:
            raise ValueError("No Songs in DB")

        response = app.response_class(
                status=200,
                response=json.dumps(random_song.to_dict()),
                mimetype='application/json'
        )
        return response
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=404
        )
        return response


@app.route('/song/<string:song_info>', methods=['DELETE'])
def delete_song(song_info):
    """ Delete a song from the DB   """
    try:

        song_mgr.delete_song(song_info)

        response = app.response_class(
                status=200
        )
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=404
        )
    return response


@app.route('/song/songs', methods=['GET'])
def get_all_songs():
    """ Return a list of all song id and titles    """
    songs = song_mgr.get_all_songs()

    response = app.response_class(
            status=200,
            response=json.dumps([s.meta_data() for s in songs]),
            mimetype='application/json'
    )

    return response


@app.route('/song/<string:song_id>', methods=['PUT'])
def update_song(song_id):
    """ Update the song information  """
    content = request.json

    try:
        song = song_mgr.get_song(song_id)
        if 'rating' in content:
            song.rating = content['rating']
        if 'album' in content:
            song.album = content['album']
        if 'genre' in content:
            song.genre = content['genre']
        song_mgr.update_song(song)
        response = app.response_class(
                status=200
        )
    except ValueError as e:
        response = app.response_class(
                response=str(e),
                status=400
        )

    return response

@app.route('/song/all', methods=['DELETE'])
def delete_all_songs():
     """ Delete a song from the DB """
     try:
         song_mgr.delete_all_songs()

         response = app.response_class(
             status=200
         )
     except ValueError as e:
         response = app.response_class(
             response=str(e),
             status=404
     )
     return response

if __name__ == "__main__":
    app.run(debug=True)
