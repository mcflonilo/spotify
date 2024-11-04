import json
from datetime import datetime, timedelta
from collections import Counter
import copy
import plotly.graph_objs as go
import plotly.offline as pyo

def load_json(filepath):
    with open(filepath, 'r' encoding) as file:
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

def find_all_artists(data):
    artists = set()
    for entry in data:
        artists.add(entry['artistName'])
    return artists

def moving_average(data, window_size):
    return [sum(data[i:i+window_size]) / window_size for i in range(len(data) - window_size + 1)]

if __name__ == "__main__":
    global data
    week = list()
    data = load_json('spotify/egenwrapped/SpotifyAccountData/StreamingHistory_music_0.json')
    data.extend(load_json('spotify/egenwrapped/SpotifyAccountData/StreamingHistory_music_1.json'))
    data.extend(load_json('spotify/egenwrapped/SpotifyAccountData/StreamingHistory_music_2.json'))

    weekByWeek = []
    topArtists = Counter()
    for entry in data:
        topArtists[entry['artistName']] += entry['msPlayed']
    topArtists = topArtists.most_common(10)

    for week in getweeks(data):
        toptentimes = [0] * 10
        topartistWeekData = [("", 0)] * 10
        for element in week:
            if element['artistName'] in dict(topArtists):
                index = list(dict(topArtists).keys()).index(element['artistName'])
                toptentimes[index] += element['msPlayed']

        for i in range(10):
            topartistWeekData[i] = (list(dict(topArtists).keys())[i], toptentimes[i])
        weekByWeek.append(copy.deepcopy(topartistWeekData))

    # Prepare data for plotting
    weeks_count = len(weekByWeek)
    x = list(range(weeks_count))
    artist_playtimes = {artist: [] for artist, _ in topArtists}

    for week_data in weekByWeek:
        total_playtime = sum(playtime for _, playtime in week_data)
        for artist, playtime in week_data:
            normalized_playtime = (playtime / total_playtime) if total_playtime > 0 else 0
            artist_playtimes[artist].append(normalized_playtime)

    # Apply moving average
    window_size = 3  # Adjust the window size as needed
    smoothed_artist_playtimes = {artist: moving_average(playtimes, window_size) for artist, playtimes in artist_playtimes.items()}

    # Adjust x-axis for smoothed data
    smoothed_x = list(range(len(x) - window_size + 1))

    # Plotting with Plotly
    traces = []
    for artist, playtimes in smoothed_artist_playtimes.items():
        trace = go.Scatter(
            x=smoothed_x,
            y=playtimes,
            mode='lines',
            name=artist
        )
        traces.append(trace)

    layout = go.Layout(
        title='Top 10 Artists Normalized Playtime Over Weeks (Smoothed)',
        xaxis=dict(title='Week'),
        yaxis=dict(title='Normalized Playtime'),
        hovermode='closest'
    )

    fig = go.Figure(data=traces, layout=layout)
    pyo.plot(fig, filename='top_artists_playtime.html')