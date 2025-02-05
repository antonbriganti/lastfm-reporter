import os
import pylast
import re
from pprint import pprint
from dotenv import load_dotenv
class Album:
    def __init__(self, name, artist, track_count, listens):
        self.name = name
        self.artist = artist
        self.track_count = track_count
        self.listens = listens
        self.full_listens = listens/track_count
    
def get_monthly_top_albums(network):
    # get top albums
    user = network.get_authenticated_user()
    albums = []
    for album in user.get_top_albums("PERIOD_1MONTH", 5):
        
        artist_name, album_name = str(album.item).split(" - ")
        album_listens = album.item.get_userplaycount()

        if len(album.item.get_tracks()) > 0:
            track_listing = album.item.get_tracks()
        else:
            # this probably means the artist is wrong, and we need to fix it 
            # remove any non ascii characters from name, then search for it
            searchable_name = re.sub(r'[^\x00-\x7f]|[()]', r'', str(album.item))
            search_results = network.search_for_album(searchable_name).get_next_page()

            for result in search_results:
                # naively assume that if I get a hit with any track list, it's the correct one
                if len(result.get_tracks()) > 0:
                    track_listing = result.get_tracks()
                    break

        album_track_count = len(track_listing)

        tmp = {}
        for track in track_listing:
            tmp[track.get_name()] = track.get_userplaycount()
        
        # print(album_name)
        # pprint(tmp)
        
        albums.append(Album(album_name, artist_name, album_track_count, album_listens))  

        # input()

    for album in albums:
        pprint(vars(album))

load_dotenv()
network = pylast.LastFMNetwork(
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET"),
    username=os.environ.get("USERNAME"),
    password_hash=os.environ.get("PASSWORD_HASH")
)

