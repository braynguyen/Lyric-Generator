import requests
from bs4 import BeautifulSoup
import re
import testing_genius
import json
from testing_genius import *

client_access_token = api_key.client_access_token

search_term = input("Enter artist/band name (check capitalization): ")
songs = main(search_term)
# print(songs)

for song_id in songs:
    # print()
    # print(song_id)
    genius = f"http://genius.com/songs/{song_id}"
    page = requests.get(genius)
    soup = BeautifulSoup(page.text, "html.parser")
    try:
        raw_lyrics = soup.find('div', {'data-lyrics-container': True}).find_all('a')
        if raw_lyrics == []:
            raw_lyrics = soup.find('div', {'data-lyrics-container': True})
    except:
        continue
    # raw_lyrics = soup.find('div', {'data-lyrics-container': True})
    formatted_lyrics = []
    # print(raw_lyrics)

    def split(x):
        for i in range(1,len(x)):
            if x[i-1].islower() and x[i].isupper():
                x = x[:i] + "*" + x[i:]
        return x.split("*")


    for x in raw_lyrics:
        x = str(x)
        #probably very inefficient
        x = re.sub("(<).*?(>)", "", x)

        lines = split(x)
        if lines != ['']:
            for line in lines:
                if line[0] != '[' and line[-1] != ']':
                    formatted_lyrics.append(line.replace('\u205f', " "))

    # print(formatted_lyrics)
    f = open(f"{search_term}.txt", "a", encoding="utf-8")
    for i in formatted_lyrics:
        # print(i)
        f.write(i + "\n")
    f.close()
    