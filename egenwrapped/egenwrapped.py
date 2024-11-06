import json
from collections import defaultdict
from datetime import datetime, timedelta
from collections import Counter
import copy
import re
import os
import matplotlib.pyplot as plt

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def find_all_json_files(directory):
        json_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.json'):
                    if file.startswith(jsonformat['fileName']):
                        json_files.append(os.path.join(root, file))

        if jsonformat['fileName'] == 'Streaming_History_Audio':
            json_files.sort(key=lambda x: (re.search(r'(\d{4})', x).group(), re.search(r'(\d+)', x.split('_')[-1]).group()))
        else:
            pass
        return json_files

def load_all_json_files(directory, regex_pattern):
    json_data = []
    json_files = find_all_json_files(directory)
    pattern = re.compile(regex_pattern)
    for filename in json_files:
        file_path = os.path.join(filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            json_data.extend(data)
            print(f"Loaded {filename}")
    return json_data

def calculateWeek(endDate, data):
    week = []
    i = 0
    while datetime.strptime(data[i][jsonformat['endtime']], jsonformat['timeformat']) < endDate:
        week.append(data[i])
        i += 1
    for i in range(0, week.__len__()):
        data.remove(week[i])
    return week

def calculateRest():
    week = []
    for i in range(0, data.__len__()):
        week.append(data[i])
    return week

def calculateTotalTimeByArtist(data):
    artist_time = defaultdict(timedelta)
    for entry in data:
        artist = entry.get(jsonformat['artistName'], None)
        if artist:
            ms_played = entry.get(jsonformat['msplayed'], 0)
            artist_time[artist] += timedelta(milliseconds=ms_played)
    most_listened_artist = max(artist_time, key=artist_time.get)
    top_10_artists = sorted(artist_time.items(), key=lambda x: x[1], reverse=True)[:10]
    for artist, time in top_10_artists:
        hours = time.total_seconds() / 3600
    return top_10_artists

def calculateartists(data):
    artists = set()
    for entry in data:
        artists.add(entry[jsonformat['artistName']])
    return artists

def calculateTopTracks(week, amount):
    tracks = []
    for i in range(0, week.__len__()):
        tracks.append(f"{week[i][jsonformat['trackname']]} - {week[i][jsonformat['artistName']]}")
    return Counter(tracks).most_common(amount)

def getweeks():
    allweeks = []
    startdate = datetime.strptime(data[0][jsonformat['endtime']], jsonformat['timeformat'])
    enddate = datetime.strptime(data[data.__len__()-1][jsonformat['endtime']], jsonformat['timeformat'])
    while startdate < enddate:
        if startdate + timedelta(days=7) > enddate:
            allweeks.append(calculateRest())
            break
        else:
            startdate = startdate + timedelta(days=7)
            allweeks.append(calculateWeek(startdate, data))
    return allweeks

def moving_average(data, window_size):
    return [sum(data[i:i+window_size]) / window_size for i in range(len(data) - window_size + 1)]

def plotTopArtistsPlaytime(data):
    top_artists = calculateTotalTimeByArtist(data)
    weeks = getweeks()
    top_artists = [artist for artist, _ in top_artists]
    print(top_artists)

    weekbyweek = []
    week_dates = []

    cumulative_time = defaultdict(int)
    for week in weeks:
        currentWeek = []
        for artist in top_artists:
            artist_time = sum(entry.get(jsonformat['msplayed'], 0) for entry in week if entry[jsonformat['artistName']] == artist)
            cumulative_time[artist] += artist_time
            currentWeek.append((artist, cumulative_time[artist]))
        weekbyweek.append(currentWeek)
        if week:
            week_dates.append(datetime.strptime(week[-1][jsonformat['endtime']], jsonformat['timeformat']))

    for artist in top_artists:
        artist_weekly_playtime = [dict(week)[artist] / 3600000 for week in weekbyweek]
        plt.plot(week_dates, artist_weekly_playtime, label=artist)

    plt.xlabel('Date')
    plt.ylabel('Playtime (hours)')
    plt.title('Top Artists Playtime Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()
    

                


def plotArtistPlaytimeOverTime(data):
    artist_time = defaultdict(list)
    for entry in data:
        artist = entry.get(jsonformat['artistName'], None)
        if artist:
            artist = artist.replace('$', '\$')
            end_time = datetime.strptime(entry[jsonformat['endtime']], jsonformat['timeformat'])
            ms_played = entry.get(jsonformat['msplayed'], 0)
            ms_played = int(ms_played)  # Convert ms_played to integer
            artist_time[artist].append((end_time, ms_played / 3600000))  # Convert ms to hours

    plt.figure(figsize=(12, 8))
    for artist, times in artist_time.items():
        times.sort()
        x, y = zip(*times)
        # Get the top 15 artists by total playtime
        total_playtime = {artist: sum(playtime for _, playtime in times) for artist, times in artist_time.items()}
        top_15_artists = sorted(total_playtime, key=total_playtime.get, reverse=True)[:15]

        for artist in top_15_artists:
            times = artist_time[artist]
            times.sort()
            x, y = zip(*times)
            plt.plot(x, y, label=artist)

    plt.xlabel('Time')
    plt.ylabel('Playtime (hours)')
    plt.title('Artist Playtime Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    global jsonformat
    global data

    #user_input = input("press y for extended or n for last year").strip().lower()
    user_input = 'y'
    if user_input == 'y':
        jsonformat = {'artistName':'master_metadata_album_artist_name','trackname':'master_metadata_track_name','msplayed':'ms_played','endtime':'ts','timeformat':'%Y-%m-%dT%H:%M:%SZ','fileName':'Streaming_History_Audio'}
        regex_pattern = r'(Streaming_History_Audio).+(\.json)'
        data = load_all_json_files('egenwrapped/SpotifyAccountData/lars/extended', regex_pattern)
    elif user_input == 'n':
        jsonformat = {'artistName':'artistName','trackname':' trackName','msplayed':'msPlayed','endtime':'endTime','timeformat':'%Y-%m-%d %H:%M','fileName':'StreamingHistory_music'}
        regex_pattern = r'(StreamingHistory_music_).+(\.json)'
        data = load_all_json_files('egenwrapped/SpotifyAccountData/pi/last year', regex_pattern)
    else:
        print("Invalid input. Please enter 'plot' or 'exit'.")

    week = list()
    
    
    #allweeks = getweeks()
    #plotTopArtistsPlaytime(data)
    plotTopArtistsPlaytime(data)
    #print(calculateTopTracks(data,10))
    
        
    
#for i in range(0, allweeks.__len__()):
    #calculateTopTracks(allweeks[i],1)
