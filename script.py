import os
import pylast
import re
import calendar
from collections import defaultdict
from dotenv import load_dotenv
from datetime import datetime, timezone

class Album:
    def __init__(self, name, artist, track_count, listens):
        self.name = name
        self.artist = artist
        self.track_count = track_count
        self.listens = listens
        self.full_listens = listens/track_count

def get_month_as_epoch_weeks(month, year):
    days_in_month = calendar.monthrange(year, month)[1]
    week = []
    
    for day in range(1, days_in_month + 1, 7):
        start_date = datetime(year, month, day, tzinfo=timezone.utc)

        if day+6 > days_in_month:
            end_date = datetime(year, month, days_in_month, 23, 59, 59, tzinfo=timezone.utc)
        else:
            end_date = datetime(year, month, day+6, 23, 59, 59, tzinfo=timezone.utc)

        week.append((int(start_date.timestamp()), int(end_date.timestamp())))
    
    return week

def get_top_results(dict_result, count=3):
    count *= -1
    sorted_results = [k for k in sorted(dict_result.items(), key=lambda item: item[1])]
    return sorted_results[count:]

def search_album(network, name):
    # this probably means the artist is wrong, and we need to fix it 
    # remove any non ascii characters from name, then search for it
    searchable_name = re.sub(r'[^\x00-\x7f]|[()]', r'', name)
    search_results = network.search_for_album(searchable_name).get_next_page()
    
    for album in search_results:
        if len(album.get_tracks()) > 0:
            return album

def search_track_duration(network, artist_name, track_name):
    # this probably means the artist is wrong, and we need to fix it 
    # remove any non ascii characters from name, then search for it
    searchable_track_name = re.sub(r'[^\x00-\x7f]|[()]', r'', track_name).strip()
    searchable_artist_name = re.sub(r'[^\x00-\x7f]|[()]', r'', artist_name).strip()

    search_results = network.search_for_track(searchable_artist_name, searchable_track_name).get_next_page()
    
    for track in search_results:
        duration = track.get_duration()
        if duration > 0:
            return duration/60000
    return 0

def get_month_history(network, month, year):
    user = network.get_authenticated_user()
    weeks = get_month_as_epoch_weeks(month, year)

    albums = defaultdict(int)
    artists = defaultdict(int)
    tracks = defaultdict(int)
    
    for week in weeks:
        res = user.get_recent_tracks(time_from=week[0], time_to=week[1], limit=999)
        for it in res:
            albums[f"{str(it.track.get_artist())} - {it.album}"] += 1
            artists[str(it.track.get_artist())] += 1
            tracks[f"{str(it.track.get_artist())} - {it.track.get_name()}"] += 1
    
    return (albums, artists, tracks)
            

def create_top_report(albums, artists, tracks):
    print("Top 3 Albums")
    for album in get_top_results(albums):
        res = search_album(network, album[0])

        print(f"{album[0]}")
        print(f"Total Plays: {album[1]}")
        print(f"Average Full Listens: {round(album[1]/len(res.get_tracks()), 2)}")
        print(f"cover img: {res.get_cover_image()}")
        
        print()
    
    print("Top 3 Tracks")
    for track in get_top_results(tracks):
        print(f"{track[0]}")
        print(f"Total Plays: {track[1]}")
        print()
    
    print("Top 3 Artists")
    for artist in get_top_results(artists):
        print(f"{artist[0]}")
        print(f"Total Plays: {artist[1]}")
        print()

load_dotenv()
network = pylast.LastFMNetwork(
    api_key=os.environ.get("API_KEY"),
    api_secret=os.environ.get("API_SECRET"),
    username=os.environ.get("LASTFM_USERNAME"),
    password_hash=os.environ.get("PASSWORD_HASH")
)

history = get_month_history(network, 1, 2025)
create_top_report(history[0], history[1], history[2])