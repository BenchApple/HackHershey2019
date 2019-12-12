# Ben Chappell

import sys
import spotipy
import spotipy.util as util
from random import randint
import math

def main():
    username = "bchapen"
    token = util.prompt_for_user_token(username,scope = 'user-top-read',client_id='407f7f8b0c314f42816264be391af790',client_secret='765d0a94dbec49e4b8a379ebe642404d',redirect_uri='https://example.com/callback')
    sp = spotipy.Spotify(auth=token)
    
    if token:
        #print("Cool we authenticated")

        # this is the final list of all genres to be used.
        genres = ['alt-rock', 'alternative', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'classical', 'country', 'death-metal', 'disco', 'dubstep', 'edm', 'electronic', 'emo', 'folk', 'funk', 'gospel', 'goth', 'grunge', 'hard-rock', 'heavy-metal', 'hip-hop', 'holidays', 'indian', 'indie', 'indie-pop', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'metal', 'metalcore', 'opera', 'piano', 'pop', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'reggae', 'rock', 'rock-n-roll', 'romance', 'salsa', 'samba', 'ska', 'soul', 'spanish', 'study', 'summer', 'synth-pop', 'tango', 'techno', 'turkish']
        print (len(genres))
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
        trackLimit = 2000
        
        for genre in genres:
            currentGenreSongs = list(generateSongsForAGenre(sp, genre, trackLimit))

            genreIDs = open("songIDs\\" + genre + "IDs.txt", 'w')
            for track in currentGenreSongs:
                genreIDs.write(track + "\n")





        #returnedSongs = list(generateSongsForAGenre(sp, genre, trackLimit))
        #print (returnedSongs)
        #checkingTrack = 9
        #trackChecked = sp.track(returnedSongs[checkingTrack])
        #print (trackChecked['name'])

        ## Find Mac Demarcos still together - example of searching for a specific song.
        #searchedSong = sp.search("Bohemian Rhapsody", limit=1, type='track')
        #print (stillTogether)
        #searchedSongID = searchedSong['tracks']['items'][0]['id']
        #print (searchedSongID)

        #getAudioFeaturesAndAnalysis(sp, searchedSongID)

        #dataCrunchingOnTracks(sp, returnedSongs)

        #classicalSongs = open('classicalIDs.txt', 'w')
        #for i in returnedSongs:
        #    classicalSongs.write(i + "\n")




# Ideas for data points (aside from the ones that the data presents immediately)
# Include confidence values in things
# Sections: Number of sections, something w their duration, loudness values (range, mean, median, etc)
# tempo(changes, avg, mean, amount of time on each), key (changes etc), mode (mainly the amount of switches),
# TS (changes and number of changes)

#Segments: Use stuff with the timbre of what's used, group the timbre's together somehow, since 
# similar timbre vectors will be similar instruments.
# Pitches used too, though harder

# Bars, Beats, Tatums: Harder to use but still interesting i guess.
# Other than all of that, use pretty much all of what the features give. 



# Get data on a large number of songs so that we can educate ourselves on what data points to use.
# This data includes time, # of (sections, segments, tatums, bars, beats)
def dataCrunchingOnTracks(sp, idList):
    # All of these just count the occurances of these events within each song.
    barCounts = []
    beatCounts = []
    secCounts = []
    segCounts = []
    tatumCount = []

    # get all of the data from each of the songs
    count = 0
    for id in idList:
        analysis = sp.audio_analysis(id)

        barCounts.append(len(analysis['bars']))
        beatCounts.append(len(analysis['beats']))
        secCounts.append(len(analysis['sections']))
        segCounts.append(len(analysis['segments']))
        tatumCount.append(len(analysis['tatums']))

        count += 1

        if count % 10 == 0:
            print (count)

    print("Bars:\nMin: %2i\nMax: %2i\nAverage: %2f\n\n" % (min(barCounts), max(barCounts), average(barCounts)))
    print("Beats:\nMin: %2i\nMax: %2i\nAverage: %2f\n\n" % (min(beatCounts), max(beatCounts), average(beatCounts)))
    print("Sections:\nMin: %2i\nMax: %2i\nAverage: %2f\n\n" % (min(secCounts), max(secCounts), average(secCounts)))
    print("Segments:\nMin: %2i\nMax: %2i\nAverage: %2f\n\n" % (min(segCounts), max(segCounts), average(segCounts)))
    print("Tatums:\nMin: %2i\nMax: %2i\nAverage: %2f\n\n" % (min(tatumCount), max(tatumCount), average(tatumCount)))


def average(list):
    s = sum(list)

    return s / len(list)

# Break down the data into what we actually want to use as data points. Remember that every song has to have the same number of data points no matter what.
def generateNeededDataPerTrack(sp, idList):
    pass


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

    bars = open("sampleBars.txt", 'w')
    for bar in anaBars:
        bars.write("Start: %2f, Duration: %2f, Confidence: %2f\n" % (bar['start'], bar['duration'], bar['confidence']))
    bars.close()

    beats = open("sampleBeats.txt", 'w')
    for beat in anaBeats:
        beats.write("Start: %2f, Duration: %2f, Confidence: %2f\n" % (beat['start'], beat['duration'], beat['confidence']))
    beats.close()

    secs = open("sampleSections.txt", 'w')
    for sec in anaSections:
        secs.write("Start: %2f, Duration: %2f, Confidence: %2f, Loudness: %2f, Tempo: %2f, Key: %1i, Mode: %1i, Time Signature: %1i\n" % 
                   (sec['start'], sec['duration'], sec['confidence'], sec['loudness'], sec['tempo'], sec['key'], sec['mode'], sec['time_signature'], ))
    secs.close()

    segs = open("sampleSegments.txt", 'w')
    for seg in anaSegments:
        segs.write("Start: %2f, Duration: %2f, Confidence: %2f, Loudness Start: %2f, Loudness Max Time: %2f, Loudness Max: %2f\nPitches: " % 
                  (seg['start'], seg['duration'], seg['confidence'], seg['loudness_start'], seg['loudness_max_time'], seg['loudness_max']))
        for i in seg['pitches']:
            segs.write(str(i) + ", ")
        segs.write("\nTimre: ")
        for i in seg['timbre']:
            segs.write(str(i) + ", ")
        segs.write("\n\n")        

    segs.close()

    tats = open("sampleTatums.txt", 'w')
    for tat in anaTatums:
        tats.write("Start: %2f, Duration: %2f, Confidence: %2f\n" % (tat['start'], tat['duration'], tat['confidence']))
    tats.close()

    

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
        print (len(generatedSongsFinalSet))

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