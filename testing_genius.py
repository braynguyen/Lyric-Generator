import api_key
import requests
import json
client_access_token = api_key.client_access_token

def main(search_term): 
    # making url for request
    # search_term = search_term.replace(" ", "%20")
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"
    # print(genius_search_url)

    response = requests.get(genius_search_url)
    json_data = response.json()
    # print(json_data)
    artist_id = json_data['response']['hits'][0]['result']['primary_artist']['id']

    #change artist_id in case first song is not the artist
    #literally because i want to do lucy dacus and boygenius comes up
    for song in json_data['response']['hits']:
        if song['result']['primary_artist']["name"] == search_term:
            artist_id = song['result']['primary_artist']["id"]

    artist_search_url = f"http://api.genius.com/artists/{artist_id}/songs"
    response = requests.get(artist_search_url)
    json_data = response.json()

    current_page = 1
    next_page = True
    songs = [] # to store final song ids

    def get_json(path, params=None, headers=None):
        '''Send request and get response in json format.'''
        # Generate request URL
        requrl = '/'.join(["https://api.genius.com", path])
        token = "Bearer {}".format(client_access_token)
        if headers:
            headers['Authorization'] = token
        else:
            headers = {"Authorization": token}

        # Get response object from querying genius api
        response = requests.get(url=requrl, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    while next_page:
        path = f"artists/{artist_id}/songs/"
        params = {'page': current_page} # the current page
        data = get_json(path=path, params=params) # get json of songs

        page_songs = data['response']['songs']
        if page_songs:
            # Add all the songs of current page
            songs += page_songs
            # Increment current_page value for next loop
            current_page += 1
            print("Page {} finished scraping".format(current_page))
            # If you don't wanna wait too long to scrape, un-comment this
            # if current_page == 2:
            #     break

        else:
            # If page_songs is empty, quit
            next_page = False

    print("Song id were scraped from {} pages".format(current_page))

    # Get all the song ids, excluding not-primary-artist songs.
    songs = [song["id"] for song in songs if song["primary_artist"]["id"] == artist_id]

    return songs
