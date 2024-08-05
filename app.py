import io
import csv
from flask import Flask, render_template, send_file, request, jsonify    # Import send_file
import requests
import pandas as pd

import warnings
warnings.filterwarnings("ignore")


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


def parse_surah_collections(surah_collections):
    collections = surah_collections.split(',')
    surah_list = []
    for item in collections:
        if ':' in item:
            start, end = map(int, item.split(':'))
            surah_list.extend(range(start, end + 1))
        else:
            surah_list.append(int(item))
    return surah_list

def generate_quran_list_content(surah_list_number):
    content = "#EXTM3U\n"
    url = "https://mp3quran.net/api/v3/reciters"
    data = fetch_data(url)
    for reciter in data['reciters']:
        #print(reciter)
        for moshaf in reciter['moshaf']:
            #print(moshaf)
            for surah in surah_list_number:
                #print(moshaf['surah_list'])
                surah_list = [int(item) for item in moshaf['surah_list'].split(',')]
                if int(surah) in surah_list:
                    url = f"{moshaf['server']}{surah:03}.mp3\n"
                    name = f"{surah:03} {reciter['name']} - {moshaf['name'].replace('-',' ')}"
                    content += f"#EXTINF:-1,{name}\n{url}\n"
                    
    return content

def generate_aya_list_content(url_list):
    content = "#EXTM3U\n"
    url = "https://mp3quran.net/api/v3/reciters"
    data = fetch_data(url)
    for url in url_list:
        content += f"#EXTINF:-1,\n{url}\n"
                    
    return content


#todo to be replaced by json 
Quraa2 = [
    ["ar.abdulbasitmurattal", 192],
    ["ar.abdullahbasfar", 192],
    ["ar.abdulsamad", 64],
    ["ar.abdurrahmaansudais", 192],
    ["ar.ahmedajamy", 128],
    ["ar.alafasy", 128],
    ["ar.aymanswoaid", 64],
    ["ar.hanirifai", 192],
    ["ar.hudhaify", 128],
    ["ar.husary", 128],
    ["ar.husarymujawwad", 128],
    ["ar.ibrahimakhbar", 32],
    ["ar.mahermuaiqly", 128],
    ["ar.minshawi", 128],
    ["ar.minshawimujawwad", 64],
    ["ar.muhammadayyoub", 128],
    ["ar.muhammadjibreel", 128],
    ["ar.parhizgar", 48],
    ["ar.saoodshuraym", 64],
    ["ar.shaatree", 128],
'''    ["en.walk", 192],
    ["fa.hedayatfarfooladvand", 40],
    ["fr.leclerc", 128],
    ["ur.khan", 64],
    ["zh.chinese", 128]'''
]

#todo this function should be by json or xml
def get_mp3_url(Qare2 , Aya_index):
    NAME = 0
    BITRATE = 1    
    url = "https://cdn.islamic.network/quran/audio/"+str(Qare2[BITRATE])+"/"+Qare2[NAME]+"/"+str(Aya_index)+".mp3"    
    return url
    
def generate_urls_Quraa2 ( AyaStartIndex, AyaEndIndex ):
    url_list =[]   
    for Q in Quraa2 :
        for i in range(AyaStartIndex,AyaEndIndex+1):
            Aya_index = str('{:0>4d}'.format(i))
            #print(Aya_index)
            generated_url = get_mp3_url(Q,Aya_index)
            url_list.append( generated_url )
            #print(url)
    #print(url_list)
    return url_list

df = pd.read_csv('Quran_aya_index.csv')

def create_playlist_name(Surah_start='', Surah_end='', Ayah_start='', Ayah_end=''):    
    # Generate a playlist name based on the user's input
    playlist_name = ('quranList_' + 'S' +str(Surah_start)+ '-A' +str(Ayah_start)+ '_S' +str(Surah_end)+ '-A' +str(Ayah_end)+ '.m3u')
    
    return playlist_name

def get_aya_index(Surah,aya):
#todo this function should be refacturized not to use df
    aya_index = df[(df['Surah_Number']==Surah)&
                  (df['Ayah_Number']==aya)]    
    #print_row(aya_index)
    #return the index of the Aya in the gobal quran 
    return list(aya_index.Ayah_index.astype(int))[0] 

def set_start_end_ayat_index(Surah_start, Surah_end, Ayah_start, Ayah_end):
    #print("start from :-")
    AyaIndexStart = get_aya_index(Surah_start,Ayah_start)
    #print("end at :-")
    AyaIndexEnd   = get_aya_index(Surah_end,Ayah_end)
    return (AyaIndexStart, AyaIndexEnd)

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

@app.route('/generate_quran_list', methods=['POST'])
def generate_audio_list():
    data = request.get_json()
    surah_collections = data.get('surahCollections', '')
    surah_list_number = parse_surah_collections(surah_collections)
    print(surah_list_number)
    audio_list_content = generate_quran_list_content(surah_list_number)
    
    output = io.BytesIO()
    output.write(audio_list_content.encode('utf-8'))
    output.seek(0)

    # Generate the file name based on the surah_collections
    file_name = f"quranList_S{surah_collections.replace(':', 'to_S').replace(',', 'and_S')}.m3u"
    
    return send_file(output, download_name=file_name, as_attachment=True)

@app.route('/generate_ayat_list', methods=['POST'])
def play_audio():
    data = request.get_json()
    start_surah = data.get('startSurah')
    start_ayah = data.get('startAyah')
    end_surah = data.get('endSurah')
    end_ayah = data.get('endAyah')
    # Logic to fetch and play the specified audio

    AyaStartIndex, AyaEndIndex = set_start_end_ayat_index(start_surah, end_surah, start_ayah, end_ayah)    
    audio_list_content = generate_urls_Quraa2(AyaStartIndex, AyaEndIndex)
    playlist_name = create_playlist_name(start_surah, end_surah, start_ayah, end_ayah)
    
    output = io.BytesIO()
    output.write(audio_list_content.encode('utf-8'))
    output.seek(0)

    # Generate the file name based on the surah_collections
    file_name = f"{playlist_name}"
    
    return send_file(output, download_name=file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


