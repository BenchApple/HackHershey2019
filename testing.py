import spotipy
spotify = spotipy.Spotify()
name = 'Mac DeMarco'
results = spotify.search(q='artist:' + name, type='artist')
print (results)