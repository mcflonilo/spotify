import json
from datetime import datetime, timedelta
from collections import Counter
import matplotlib.pyplot as plt

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def calculateTopTracks(week, amount):
    tracks = []
    for i in range(0, len(week)):
        tracks.append(week[i]['trackName'])
    return Counter(tracks).most_common(amount)

def getweeks(data):
    startdate = datetime.strptime(data[0]['endTime'], '%Y-%m-%d %H:%M')
    enddate = datetime.strptime(data[-1]['endTime'], '%Y-%m-%d %H:%M')
    allweeks = []

    while startdate < enddate:
        week = []
        next_week = startdate + timedelta(days=7)
        for entry in data:
            entry_date = datetime.strptime(entry['endTime'], '%Y-%m-%d %H:%M')
            if startdate <= entry_date < next_week:
                week.append(entry)
        most_played_songs = calculateTopTracks(week, 10)
        allweeks.append(most_played_songs)
        startdate = next_week

    return allweeks

if __name__ == "__main__":
    data = load_json('spotify/egenwrapped/SpotifyAccountData/StreamingHistory_music_0.json')
    data.extend(load_json('spotify/egenwrapped/SpotifyAccountData/StreamingHistory_music_1.json'))
    data.extend(load_json('spotify/egenwrapped/SpotifyAccountData/StreamingHistory_music_2.json'))

    weeks = getweeks(data)

    # Prepare data for visualization
    song_totals = Counter()
    for week in weeks:
        for song, count in week:
            song_totals[song] += count

    # Filter to top 20 songs over the year
    top_songs = song_totals.most_common(20)

    # Plot the data
    songs, counts = zip(*top_songs)
    plt.figure(figsize=(14, 7))
    plt.barh(songs, counts)
    plt.xlabel('Total Play Count')
    plt.ylabel('Song')
    plt.title('Top 20 Songs Over the Year')
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest count on top
    plt.show()