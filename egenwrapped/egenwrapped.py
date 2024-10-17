import json
from collections import defaultdict
from datetime import datetime, timedelta
from collections import Counter
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
def calculateWeek(endDate, data):
    week = []
    i = 0
    while datetime.strptime(data[i]['endTime'], '%Y-%m-%d %H:%M') < endDate:
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

def calculateTopArtistsByPlays(week, amount):
    artists = []
    for i in range(0, week.__len__()):
        artists.append(week[i]['artistName'])
    return Counter(artists).most_common(amount)

def calculateartists(week):
    artists = set()
    for i in range(0, week.__len__()):
        artists.add(week[i]['artistName'])

def calculateTopTracks(week, amount):
    tracks = []
    for i in range(0, week.__len__()):
        tracks.append(week[i]['trackName'])
    return Counter(tracks).most_common(amount)

def getweeks():
    allweeks = []
    startdate = datetime.strptime(data[0]['endTime'], '%Y-%m-%d %H:%M')
    enddate = datetime.strptime(data[data.__len__()-1]['endTime'], '%Y-%m-%d %H:%M')
    while startdate < enddate:
        if startdate + timedelta(days=7) > enddate:
            allweeks.append(calculateRest())
            break
        else:
            startdate = startdate + timedelta(days=7)
            allweeks.append(calculateWeek(startdate, data))
    return allweeks

if __name__ == "__main__":
    global data
    week = list()
    data = load_json('spotify/egenwrapped/SpotifyAccountData/StreamingHistory_music_0.json')
    data.extend(load_json('spotify/egenwrapped/SpotifyAccountData/StreamingHistory_music_1.json'))
    data.extend(load_json('spotify/egenwrapped/SpotifyAccountData/StreamingHistory_music_2.json'))
    
    allweeks = getweeks()
    artists = calculateartists(allweeks[0])
    print(artists)
    #alltimetracks = calculateTopTracks(data,100)
    #weeks = getweeks()
        
    
#for i in range(0, allweeks.__len__()):
    #calculateTopTracks(allweeks[i],1)
