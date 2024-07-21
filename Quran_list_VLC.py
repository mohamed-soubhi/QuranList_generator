import csv
import json
import requests
import pandas as pd
import os

import warnings
warnings.filterwarnings("ignore")

'''
help links
https://docs.globalquran.com/#/operations/get-quran-ayah
https://alquran.cloud/
https://alquran.cloud/cdn
https://globalquran.com/download/
https://github.com/GlobalQuran/site/archive/v3.4.0.zip
https://cdn.islamic.network/quran/audio/128/ar.alafasy/2826.mp3
'''

print(''' 
**** Repeate Quran V0.1.1 ****
هذا البرنامج لاختيار أيات متتالية او سور محددة للتلاوة  لمختلف القراء 
و يقدمها لك كقائمة تشغيل يمكن تشغيلها على جهازك 
تطلب انترنت لتعمل 

البرنامج قيد التجريب
ننصح بإستخدام برنامج VLC
فضلا انتظر للتحميل
This program to play certain Ayat or Souar continously
with diffrent readers 
we recommend to use VLC player 
Please wait for loading...
'''
)


# Global variables
 #list
Surah_ayah_max = [
                    [ 1 , 7 ],
                    [ 2 , 286 ],
                    [ 3 , 200 ],
                    [ 4 , 176 ],
                    [ 5 , 120 ],
                    [ 6 , 165 ],
                    [ 7 , 206 ],
                    [ 8 , 75 ],
                    [ 9 , 129 ],
                    [ 10 , 109 ],
                    [ 11 , 123 ],
                    [ 12 , 111 ],
                    [ 13 , 43 ],
                    [ 14 , 52 ],
                    [ 15 , 99 ],
                    [ 16 , 128 ],
                    [ 17 , 111 ],
                    [ 18 , 110 ],
                    [ 19 , 98 ],
                    [ 20 , 135 ],
                    [ 21 , 112 ],
                    [ 22 , 78 ],
                    [ 23 , 118 ],
                    [ 24 , 64 ],
                    [ 25 , 77 ],
                    [ 26 , 227 ],
                    [ 27 , 93 ],
                    [ 28 , 88 ],
                    [ 29 , 69 ],
                    [ 30 , 60 ],
                    [ 31 , 34 ],
                    [ 32 , 30 ],
                    [ 33 , 73 ],
                    [ 34 , 54 ],
                    [ 35 , 45 ],
                    [ 36 , 83 ],
                    [ 37 , 182 ],
                    [ 38 , 88 ],
                    [ 39 , 75 ],
                    [ 40 , 85 ],
                    [ 41 , 54 ],
                    [ 42 , 53 ],
                    [ 43 , 89 ],
                    [ 44 , 59 ],
                    [ 45 , 37 ],
                    [ 46 , 35 ],
                    [ 47 , 38 ],
                    [ 48 , 29 ],
                    [ 49 , 18 ],
                    [ 50 , 45 ],
                    [ 51 , 60 ],
                    [ 52 , 49 ],
                    [ 53 , 62 ],
                    [ 54 , 55 ],
                    [ 55 , 78 ],
                    [ 56 , 96 ],
                    [ 57 , 29 ],
                    [ 58 , 22 ],
                    [ 59 , 24 ],
                    [ 60 , 13 ],
                    [ 61 , 14 ],
                    [ 62 , 11 ],
                    [ 63 , 11 ],
                    [ 64 , 18 ],
                    [ 65 , 12 ],
                    [ 66 , 12 ],
                    [ 67 , 30 ],
                    [ 68 , 52 ],
                    [ 69 , 52 ],
                    [ 70 , 44 ],
                    [ 71 , 28 ],
                    [ 72 , 28 ],
                    [ 73 , 20 ],
                    [ 74 , 56 ],
                    [ 75 , 40 ],
                    [ 76 , 31 ],
                    [ 77 , 50 ],
                    [ 78 , 40 ],
                    [ 79 , 46 ],
                    [ 80 , 42 ],
                    [ 81 , 29 ],
                    [ 82 , 19 ],
                    [ 83 , 36 ],
                    [ 84 , 25 ],
                    [ 85 , 22 ],
                    [ 86 , 17 ],
                    [ 87 , 19 ],
                    [ 88 , 26 ],
                    [ 89 , 30 ],
                    [ 90 , 20 ],
                    [ 91 , 15 ],
                    [ 92 , 21 ],
                    [ 93 , 11 ],
                    [ 94 , 8 ],
                    [ 95 , 8 ],
                    [ 96 , 19 ],
                    [ 97 , 5 ],
                    [ 98 , 8 ],
                    [ 99 , 8 ],
                    [ 100 , 11 ],
                    [ 101 , 11 ],
                    [ 102 , 8 ],
                    [ 103 , 3 ],
                    [ 104 , 9 ],
                    [ 105 , 5 ],
                    [ 106 , 4 ],
                    [ 107 , 7 ],
                    [ 108 , 3 ],
                    [ 109 , 6 ],
                    [ 110 , 3 ],
                    [ 111 , 5 ],
                    [ 112 , 4 ],
                    [ 113 , 5 ],
                    [ 114 , 6 ],
                ]
#todo to be replaced by json 
Quraa2 = [
            ["ar.ahmedajamy",128],
            ["ar.alafasy",128],
            ["ar.hudhaify",128],
            ["ar.husary",128],
            ["ar.husarymujawwad",128],
            ["ar.mahermuaiqly",128],
            ["ar.minshawi",128],
            ["ar.muhammadayyoub",128],
            ["ar.muhammadjibreel",128],
            ["ar.shaatree",128],
            ["ar.abdulbasitmurattal",192],
            ["ar.abdullahbasfar",192],
            ["ar.abdurrahmaansudais",192],
            ["ar.hanirifai",192],
            ["ar.abdullahbasfar",32],
            ["ar.hudhaify",32],
            ["ar.ibrahimakhbar",32],
            ["ar.abdulsamad",64],
            ["ar.aymanswoaid",64],
            ["ar.minshawimujawwad",64],
            ["ar.saoodshuraym",64],
          ] 
 #numbers
debug = 0 
 #string
 #DataFrame
df = pd.read_csv('Quran_aya_index.csv')




#todo check input validation 
def check_ayat_input(Surah_start, Surah_end, Ayah_start, Ayah_end):
    global Surah_ayah_max;
    return 1

def get_Ayat_input():
    Surah_start = int(input("Surah start No#: "))   
    Surah_end   = int(input("Surah end No#  : "))
    Ayah_start  = int(input("Ayah start No# : ")) 
    Ayah_end    = int(input("Ayah end No#   : "))
    
    check_ayat_input(Surah_start, Surah_end, Ayah_start, Ayah_end)
    return (Surah_start, Surah_end, Ayah_start, Ayah_end)
    
def create_playlist_name(Surah_start='', Surah_end='', Ayah_start='', Ayah_end=''):    
    # Generate a playlist name based on the user's input
    playlist_name = ('quranList_' + 'S' +str(Surah_start)+ '-A' +str(Ayah_start)+ '_S' +str(Surah_end)+ '-A' +str(Ayah_end)+ '.xspf')
    
    return playlist_name
    
def get_aya_index(Surah,aya):
#todo this function should be refacturized not to use df
    global df, debug
    aya_index = df[(df['Surah_Number']==Surah)&
                  (df['Ayah_Number']==aya)]    
    if debug == 1 :
        print_row(aya_index)
    #return the index of the Aya in the gobal quran 
    return list(aya_index.Ayah_index.astype(int))[0]     

#used for testing and debug
def print_row(df_line):
    print()
    for column in df_line.columns:
        print('\t' , column, '\t\t' ,df_line[column].values[0])
    print()

def set_start_end_ayat_index(Surah_start, Surah_end, Ayah_start, Ayah_end):
    if debug == 1 :
        print("start from :-")
    AyaIndexStart = get_aya_index(Surah_start,Ayah_start)
    if debug == 1 :
        print("end at :-")
    AyaIndexEnd   = get_aya_index(Surah_end,Ayah_end)
    return (AyaIndexStart, AyaIndexEnd)


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
    
def generate_playList(playlist_name,mp3_list):
    with open(playlist_name, 'w',encoding="utf-8") as quranList:
        quranList.write("""<?xml version="1.0" encoding="UTF-8"?>
        <playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
                <title>Playlist</title>
                <trackList>""")
        i = 0
        for link in mp3_list:
            quranList.write("""		<track>
                                <location>"""+link+"""</location>
                                <extension application="http://www.videolan.org/vlc/playlist/0">
                                        <vlc:id>"""+str(i)+"""</vlc:id>
                                        <vlc:option>network-caching=1000</vlc:option>
                                </extension>
                        </track>""")
            i+=1

        quranList.write("""	</trackList>
                <extension application="http://www.videolan.org/vlc/playlist/0">
                        <vlc:node title="qurango.xspf">""")
        for i in range(len(mp3_list)):
            quranList.write('			<vlc:item tid="'+str(i)+'"/>')

        quranList.write("""		</vlc:node>
                </extension>
        </playlist>
        """)
        
    print("Finished writing "+playlist_name)

def Ayat_program():
    Surah_start, Surah_end, Ayah_start, Ayah_end = get_Ayat_input()
    AyaStartIndex, AyaEndIndex = set_start_end_ayat_index(Surah_start, Surah_end, Ayah_start, Ayah_end)    
    mp3url_list = generate_urls_Quraa2(AyaStartIndex, AyaEndIndex)
    playlist_name = create_playlist_name(Surah_start, Surah_end, Ayah_start, Ayah_end)
    generate_playList(playlist_name,mp3url_list)


def Surah_program():
    Surah_nums = ['']

    # Prompt the user for input on which Surahs to include in the playlist
    Surah_nums_inp = input('Enter the numbers of Surah separated by : OR , :-\n')

    # Generate a playlist name based on the user's input
    playlist_name = ('quranList_S' + Surah_nums_inp + '.xspf').replace(':', 'to_S').replace(',', 'and_S')


    # Process the user's input to create a list of Surah numbers
    if ':' in Surah_nums_inp:
        # If the input includes a range (e.g. "1:5"), create a list of numbers from the range
        Surah_nums = range(int(Surah_nums_inp.replace(' ', '').split(':')[0]), int(Surah_nums_inp.replace(' ', '').split(':')[1])+1)
    elif ',' in Surah_nums_inp:
        # If the input includes a list of numbers separated by commas (e.g. "1,2,3"), create a list from the input
        Surah_nums = Surah_nums_inp.replace(' ', '').split(',')
    else:
        Surah_nums[0] = int(Surah_nums_inp)

    #print(*Surah_nums, sep = ", ")
    print('please wait for generating file')

    # URL of the mp3quran API
    url = 'https://www.mp3quran.net/api/v3/reciters?language=ar'

    # List to store the URLs of all audio files
    mp3QuranURL = []

    # List to store the URLs of the audio files for the Surahs specified by the user
    listen_URL = []

    # Send a GET request to the API to retrieve a list of reciters and their corresponding audio files
    response = requests.get(url)

    # Load the JSON data from the response
    data = response.json()

    # Get the list of reciters from the JSON data
    reciters = data['reciters']



    df = pd.DataFrame(['id', 'name', 'letter','moshaf_id','moshaf_name','moshaf_surah_num','moshaf_surah_url'])


    # Iterate through the list of reciters and write each row to the CSV file
    for reciter in reciters:
        for moshaf in reciter['moshaf']:
            # Write the reciter's information and the information for each moshaf (edition of the Quran)
            
            # Split the list of Surahs for the moshaf into a list of individual Surah numbers
            surah_list = moshaf['surah_list'].split(',')
            for surah in surah_list:
                mp3Url = moshaf['server'] + f'{int(surah):03d}' +'.mp3'
                mp3QuranURL.append(mp3Url)
                df = pd.concat([df, pd.DataFrame([reciter['id'],reciter['name'],reciter['letter'],moshaf['id'],moshaf['name'],surah,mp3Url])], ignore_index=True)
                        
                for Surah_num in Surah_nums:
                    if f'{int(Surah_num):03d}' in mp3Url :
                        listen_URL.append(mp3Url)

    #df.to_csv('mp3Quran.csv',index=False,sep=',')
    #print("Finished writing CSV file")



    with open(playlist_name, 'w',encoding="utf-8") as quranList:
        quranList.write("""<?xml version="1.0" encoding="UTF-8"?>
        <playlist xmlns="http://xspf.org/ns/0/" xmlns:vlc="http://www.videolan.org/vlc/playlist/ns/0/" version="1">
                <title>Playlist</title>
                <trackList>""")
        i = 0
        for link in listen_URL:
            quranList.write("""		<track>
                                <location>"""+link+"""</location>
                                <extension application="http://www.videolan.org/vlc/playlist/0">
                                        <vlc:id>"""+str(i)+"""</vlc:id>
                                        <vlc:option>network-caching=1000</vlc:option>
                                </extension>
                        </track>""")
            i+=1

        quranList.write("""	</trackList>
                <extension application="http://www.videolan.org/vlc/playlist/0">
                        <vlc:node title="qurango.xspf">""")
        for i in range(len(listen_URL)):
            quranList.write('			<vlc:item tid="'+str(i)+'"/>')

        quranList.write("""		</vlc:node>
                </extension>
        </playlist>
        """)
    print("Finished writing "+playlist_name)
  

# if __name__ == '__main__' checks if a file is imported as a module or not.
def main():
    while True:
        choice = input("send [A] for ayat  \nsend [S] for complete suar\n")
        print(choice)
        if choice.lower() == 'a':
            Ayat_program()
        elif choice.lower() == 's':
            Surah_program()       
        print('\n\n\tAllah bless the coder\n\n')

  

    
if __name__ == '__main__':
    # This code won't run if this file is imported.
    main()



