import io
import csv
from flask import Flask, render_template, send_file, request, jsonify    # Import send_file
import requests



app = Flask(__name__)


# Helpful functions 
def fetch_data(url):
    """Fetch data from the given URL."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def create_m3u_playlist(data, filename):
    """Create an M3U playlist from the given data."""
    playlist_content = "#EXTM3U\n"
    for radio in data['radios']:
        playlist_content += f"#EXTINF:-1,{radio['name']}\n{radio['url']}\n"
    playlist_file = f'{filename}.m3u'
    with open(playlist_file, 'w', encoding='utf-8') as file:
        file.write(playlist_content)
    return playlist_file


def handle_generate_radio_list():
    """Handle the task of fetching, saving, and creating a playlist."""
    url = "https://mp3quran.net/api/v3/radios"
    data = fetch_data(url)
    if data:
        m3u_file = create_m3u_playlist(data, 'radios_playlist')
        print(f"Files created: {csv_file}, {m3u_file}")   



# route

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_radio_list', methods=['POST'])
def generate_radio_list():
    try:
        url = "https://mp3quran.net/api/v3/radios"
        radio_data = fetch_data(url)
        
        playlist_content = "#EXTM3U\n"  # M3U header
        for item in radio_data['radios']:
            playlist_content += f"#EXTINF:-1,{item['name']}\n"  # Track info
            playlist_content += f"{item['url']}\n"
        download_name = 'radio_list.m3u'
        mimetype = 'audio/x-mpegurl'
        
        # Use BytesIO to create file-like object from string
        file_like_object = io.BytesIO(playlist_content.encode('utf-8'))  

        return send_file(
            file_like_object,
            as_attachment=True,
            download_name=download_name,
            mimetype=mimetype
        )

    except Exception as e:
        app.logger.error('Error generating playlist: %s', e)
        return jsonify({'error': 'An error occurred while generating the playlist.'}), 500

@app.route('/generate_audio_list', methods=['POST'])
def generate_audio_list():
    data = request.get_json()
    surah_collections = data.get('surahCollections')
    # Logic to generate audio list based on surah collections
    audio_list = []  
    # ... your processing logic ...
    return jsonify(audio_list)

@app.route('/play_audio', methods=['POST'])
def play_audio():
    data = request.get_json()
    start_surah = data.get('startSurah')
    start_ayah = data.get('startAyah')
    end_surah = data.get('endSurah')
    end_ayah = data.get('endAyah')
    # Logic to fetch and play the specified audio
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)


