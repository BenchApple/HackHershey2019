# Ben Chappell

import sys
import spotipy
import spotipy.util as util
from random import randint

def main():
    username = "bchapen"
    token = util.prompt_for_user_token(username,scope = 'user-top-read',client_id='407f7f8b0c314f42816264be391af790',client_secret='765d0a94dbec49e4b8a379ebe642404d',redirect_uri='https://example.com/callback')
    sp = spotipy.Spotify(auth=token)
    
    if token:
        #print("Cool we authenticated")

        #genres = sp.recommendation_genre_seeds()['genres']
        #print (genres)
        #print (len(genres))
        #genreWanted = 'pop'
        #print (genreWanted)
        
        #For more popular genres, 5k shouldn't be too much of a problem, takes probably about a minute. Even 10k is feasible. Using multiple computers, could be very short 
        # data collection for a lot of genres. Sweet spot is probably around 5k songs per category.
        # For less popular genres, can run into problems around 1.5K, so have to be careful
        # Country took around 2 minutes for 5000 examples
        # Pop took around 2 minutes for 7k examples

        # I don't know if 10k examples per final genre is the best of ideas, but it could be fruitful to create final genres for the training using k-means clustering
        # Basic idea would be to gather as many samples of data as possible for each genre, then get all of their data and then cluster all of it with the 
        # final count of genres we want being the amount of clusters. If the data is truly unique then there should be no issue with this, and it will put like genres 
        # in the same clusters.
        # If we're going to do this, we will likely need to reduce the size of the data using SVD, otherwise it'll take ages to run properly

        # TODO check if the current method detracts from the uniqueness of the songs returned.
        returnedSongs = list(generateSongsForAGenre(sp, 'pop', 100))
        #print (returnedSongs)
        checkingTrack = 9
        trackChecked = sp.track(returnedSongs[checkingTrack])
        #print (trackChecked['name'])

        ## Find Mac Demarcos still together - example of searching for a specific song.
        searchedSong = sp.search("Still Together", limit=1, type='track')
        #print (stillTogether)
        searchedSongID = searchedSong['tracks']['items'][0]['id']
        print (searchedSongID)

        getAudioFeaturesAndAnalysis(sp, searchedSongID)


# Mostly just for human consumption of songs.
def getAudioFeaturesAndAnalysis(sp, trackID):
    analysis = sp.audio_analysis(trackID)
    features = sp.audio_features(trackID)

    del analysis['track']['codestring']
    del analysis['track']['echoprintstring']
    del analysis['track']['synchstring']
    del analysis['track']['rhythmstring']

    anaBars = analysis['bars']
    anaBeats = analysis['beats']
    anaSections = analysis['sections']
    anaSegments = analysis['segments']
    anaTatums = analysis['tatums']

    for bar in anaBars:
        print ("Start: %5f, Duration: %5f, Confidence: %5f" % (bar['start'], bar['duration'], bar['confidence']))

    #print (analysis)
    #print ("\n\n\n")
    #print (features)

        
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
    counter = 0
    while len(generatedSongsFinalSet) < upperLimit:
        # the raw track data returned by spotify
        if counter > 0:
            # Removes and returns a random element from the set, to be used as the track seed for the next iteration.
            trackSeed = [generatedSongsFinalSet.pop()]
            rawTracks = sp.recommendations(seed_genres=genre, seed_tracks=trackSeed, limit=100)['tracks']
        else:
            rawTracks = sp.recommendations(seed_genres=genre, limit=100)['tracks']

        # Iterate through the raw track data and extract the IDs of each of the tracks, adding them to the set.
        for i in range(0, len(rawTracks)):
            #Navigate these JSON structures using the spotify api docs, makes it easier than self analyzing.
            generatedSongsFinalSet.add(rawTracks[i]['id'])

        # Remove the placeholder Tracker for simplicity.
        if placeholderTracker:
            generatedSongsFinalSet.remove('placeholder')
            placeholderTracker = False
            

        counter += 1
        #print (len(generatedSongsFinalSet))

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
# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/ - audio analysis page - lots of good shit here
# https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/ - audio features page, even more amazing shit here
# I legit thought the hardest part of this would be the data colleciton, 


if __name__ == '__main__':
    main()