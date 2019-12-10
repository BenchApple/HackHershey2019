# Ben Chappell

import sys
import spotipy
import spotipy.util as util

def main():
    username = "bchapen"
    token = util.prompt_for_user_token(username,scope = 'user-top-read',client_id='407f7f8b0c314f42816264be391af790',client_secret='765d0a94dbec49e4b8a379ebe642404d',redirect_uri='https://example.com/callback')
    sp = spotipy.Spotify(auth=token)
    
    if token:
        print("Cool we authenticated")

        genres = sp.recommendation_genre_seeds()['genres']
        genreWanted = genres[4]
        print (genreWanted)
        
        returnedSongs = list(generateSongsForAGenre(sp, genreWanted, 10))
        print (returnedSongs)
        checkingTrack = 9
        trackChecked = sp.track(returnedSongs[checkingTrack])
        print (trackChecked['name'])

        
# TODO add some sort of limiter on the loop if the limit is less than 100? idk exactly how this will work. I might honestly just instead have the limit be the 
# limit for the amount of times that the collection loop runs
def generateSongsForAGenre(sp, genre, upperLimit):
    #Will hold the all of the songs that are to be returned. The values will be the IDs of the songs as per spotify, as lists cannot be placed in sets.
    # A set is used to guarentee the uniqueness of each element.
    generatedSongsFinalSet = {'placeholder'}
    # keeps track of whether the placeholder has been removed or not.
    placeholderTracker = True

    #convert to a list since the recommendations only takes it as a list.
    genre=[genre]

    # if limit is set too high this loop might take a long time to run, I don't know yet.
    while len(generatedSongsFinalSet) < upperLimit:
        # the raw track data returned by spotify
        rawTracks = sp.recommendations(seed_genres=genre, limit=100)['tracks']

        # Iterate through the raw track data and extract the IDs of each of the tracks, adding them to the set.
        for i in range(0, len(rawTracks)):
            #Navigate these JSON structures using the spotify api docs, makes it easier than self analyzing.
            generatedSongsFinalSet.add(rawTracks[i]['id'])

        # Remove the placeholder Tracker for simplicity.
        if placeholderTracker:
            generatedSongsFinalSet.remove('placeholder')
            placeholderTracker = False

    return generatedSongsFinalSet


    #track = sp.recommendations(seed_genres=genres, limit=1)['tracks'][0]
    #recommended.append([genres[0], track['name'], track['id']])

    #generatedSongsFinalSet.add(['this', 'is', 'a', 'test'])
    #print (generatedSongsFinalSet)


# Gets the top artist of the user currently logged in, shouldn't be needed.
def getMyTopArtist(sp):
    myTopArtist = sp.current_user_top_artists(1, 0, 'short_term')

    ## Returns the url of the current artist's url
    topArtistUrl = myTopArtist['items'][0]['external_urls']['spotify']
       
    topArtistAlbums = sp.artist_albums(topArtistUrl)
    #topArtistTracks = sp.artist_top_tracks(topArtistUrl)

    #print (topArtistTracks)

    topArtistGenres = myTopArtist['items'][0]['genres']

    return [topArtistAlbums, topArtistGenres]


#Gets one recommendation from the spotify api for every genre spotify uses for their recommendation seedings. 
def oneRecommendationPerGenre(sp):
    #Get all of the genre seeds
    seeds = sp.recommendation_genre_seeds()['genres']

    recommended = []
    #Iterate through the genres, getting one recommendation per genre
    for i in range(0, len(seeds)):
        genres = [seeds[i]]
        print (genres)
        #print (sp.recommendations(seed_genres=genres, limit=1))
        track = sp.recommendations(seed_genres=genres, limit=1)['tracks'][0]

        recommended.append([genres[0], track['name'], track['id']])

    print (recommended)

# Can find a list of tracks per a specific genre using the recommendations function. 
# Can use this in tandem with getting genres from artists to generate large amounts of tracks per genre that I want.
# Can get an audio analysis for tracks using the API, need to find this function in spotipy.


if __name__ == '__main__':
    main()