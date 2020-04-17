from flask import Flask, jsonify, request, make_response
from audio_library import AudioLibrary
from song import Song

app = Flask(__name__)

audio_library = AudioLibrary()


@app.route("/validate", methods=["GET", "POST", "PUT", "DELETE"])
def validate_setup():
    return jsonify(
        {
            "method": request.method,
            "Content-Type header": request.headers.get("Content-Type"),
            "data": request.data.decode(),
        }
    )


@app.route("/audiolib/songs", methods=["POST"])
def add_song():
    data = request.json
    if not data:
        return make_response("NoJSON.CheckheadersandJSONformat.", 400)
    try:
        song = Song(data["title"], data["artist"], data["album"], data["runtime"], data["file_location"], data["genre"])
        audio_library.add_song(song)
        return make_response("OK", 200)
    except ValueError as e:
        message = str(e)
        return make_response(message, 400)


@app.route("/audiolib/songs/<song_title>", methods=["GET"])
def get_song(song_title):
    song = audio_library.get_song(song_title)

    if not song:
        return make_response("Song does not exist.", 404)
    else:
        return make_response(jsonify(song.meta_data()), 200)


@app.route("/audiolib/songs/<song_title>", methods=["DELETE"])
def remove_song(song_title):
    try:
        song = audio_library.remove_song(song_title)
    except ValueError:
        return make_response("Song does not exist.", 404)

    return make_response("OK", 200)


@app.route("/audiolib/songs/titles", methods=["GET"])
def get_song_titles():
    song_list = audio_library.song_titles

    return make_response(jsonify(song_list), 200)


@app.route("/audiolib/songs/rating", methods=["PUT"])
def update_song_rating():
    data = request.json
    if not data:
        return make_response("No JSON. Check headers and JSON format.", 400)

    song = audio_library.get_song(data["title"])

    if not song:
        return make_response("Song not found.", 404)

    if "title" not in data.keys():
        return make_response("Invalid JSON: missing name", 400)

    try:
        song.rating = data["rating"]
        return make_response("OK", 200)
    except ValueError as e:
        return make_response(str(e), 400)


if __name__ == "__main__":
    app.run(debug=True)
