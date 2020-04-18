from flask import Flask, request
from song_manager import SongManager
from song import Song
import json
from datetime import datetime


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


@app.route('/song/<string:song_info>', methods=['GET'])
def get_song(song_info):
    """ Get a song from the database """
    try:
        song = song_mgr.get_song(song_info)
        if song is None:
            raise ValueError(f"Song does not exist")

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


@app.route('/song/<string:song_info>', methods=['PUT'])
def update_song(song_info):
    """ Update the song information  """

    content = request.json

    try:
        song = song_mgr.get_song(song_info)

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

@app.route('/song/usage/<string:song_info>', methods=['PUT'])
def update_usage(song_info):
    """ Update the song usage stats  """

    try:
        song = song_mgr.get_song(song_info)
        song_mgr.update_song_usage(song)

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
