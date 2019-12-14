# Ben Chappell

import spotipy
import spotipyInit
import math
import random
import os
import gc
import spotipy.util as util

token = spotipyInit.token
sp = spotipy.Spotify(auth=token)

genres = ['alt-rock', 'alternative', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'classical', 'country', 'death-metal', 'disco', 'dubstep', 'edm', 'electronic', 'emo', 'folk', 'funk', 'gospel', 'goth', 'grunge', 'hard-rock', 'heavy-metal', 'hip-hop', 'holidays', 'indian', 'indie', 'indie-pop', 'jazz', 'k-pop', 'kids', 'latin', 'latino', 'metal', 'metalcore', 'opera', 'piano', 'pop', 'psych-rock', 'punk', 'punk-rock', 'r-n-b', 'reggae', 'rock', 'rock-n-roll', 'romance', 'salsa', 'samba', 'ska', 'soul', 'spanish', 'study', 'summer', 'synth-pop', 'tango', 'techno', 'turkish']


### all of the data that i want to collect from each track ###

'''
# of tatums, beats, bars, sections, segments
# avg confidence of tatums, beats, bars, sections, segments

From Sections
min loudness, max loudness, avg loudness
volume swell factor - is there a distinct swell in the volume? - use the volume in tandem with the loudness to create a "graphic" 
representation and use the derivative and calc stuff to determine this
min tempo, max tempo, avg tempo
tempo swell factor - same as volume
# of distinct keys - # of key changes, average key, longest run, shortest run
# of mode switches, longest run in a single mode, shortest, avg mode (kinda touches on happiness)
Prodominant TS, TS switches, longest TS run (seconds), average TS

From Segments (this is likely to become much more complicated and I'm kinda worried about time when it comes to running all of this on 100000 songs)
I honestly don't know how we want to crunch the data presented by pitches
I don't know if there's anything useful to be gained from that
What is cool is that it'd be possible to sheet music it from this

Timbre - 
See if any patterns in the most frequent timbres can be found, i don't know
if this will be all that useful either without some serious crunching that i don't 
know that we can do within the time limit.
including all of this stuff might have to be a personal project
What I'm thinking is that all of the timbres might need to be mapped into 12
dimensions and then clustered in some way, but that brings up its own problems
Overall using timbre and pitch would be incredibly difficult, so I need to think
on it
The upside is that they could be incredibly useful in all of this.
pretty much all that applies here kinda applies to pitch too, but not as much
pitch could be used to recreate a melodic line, which would be another really really cool project


From Song Features --
length
key, key vs keys from sections
mode, mode vs mode from sections
time signature, TS vs TS from sections
acousticness, danceability, energy, instrumentalness, liveness
Loudness, loudness vs loudness from sections and segments
speechiness
valence
tempo, tempo vs tempo from sectionss

'''

def loudnessSections(sections):
    pass

def barsAnalysis(bars):
    barCount = len(bars)

    barConfSum = 0
    for bar in bars:
        barConfSum += bar['confidence']

    return [barConfSum / barCount, barCount]

def beatAnalyis(beats):
    beatCount = len(beats)

    beatConfSum = 0
    for beat in beats:
        beatConfSum += beat['confidence']

    return [beatConfSum / beatCount, beatCount]

def tatumAnalysis(tatums):
    tatumCount = len(tatums)

    tatumConfSum = 0
    for tatum in tatums:
        tatumConfSum += tatum['confidence']

    return [tatumConfSum / tatumCount, tatumCount]


# I'm pretty sure that this section is done, need to know soon if there are any other ideas for data from here.
# This is all of the analyisis and data collection for the sections
def sectionAnalysis(sections):
    sectionCount = len(sections)

    sectionConfSum = 0
    loudnessSum = 0
    tempoSum = 0
    keySum = 0
    keyConfSum = 0
    modeSum = 0
    modeConfSum = 0
    tsSum = 0
    tsConfSum = 0

    # TODO somehting to measure the swell in the volume

    minLoud = sections[0]['loudness']
    maxLoud = sections[0]['loudness']
    minTemp = sections[0]['tempo']
    maxTemp = sections[0]['tempo']

    keys = {'ph'}
    timeSigs = {'ph'}

    keys.remove('ph')
    timeSigs.remove('ph')

    shortestKeyRun = sectionCount
    longestKeyRun = 0
    shortestModeRun = sectionCount
    longestModeRun = 0
    shortestTSRun = sectionCount
    longestTSRun = 0

    currentKeyRun = 0
    currentModeRun = 0
    currentTSRun = 0

    loudness = []
    tempo = []
    times = []

    prevKey = sections[0]['key']
    keySwitches = 0
    prevMode = sections[0]['mode']
    modeSwitches = 0
    prevTS = sections[0]['time_signature']
    tsSwitches = 0

    for section in sections:
        conf = section['confidence']
        l = section['loudness']
        t = section['tempo']
        k = section['key']
        kConf = section['key_confidence']
        m = section['mode']
        mConf = section['mode_confidence']
        ts = section['time_signature']
        tsConf = section['time_signature_confidence']

        sectionConfSum += conf
        loudnessSum += l
        tempoSum += t
        keySum += k
        keyConfSum += kConf
        modeSum += m
        modeConfSum += mConf
        tsSum += ts
        tsConfSum += tsConf

        if l < minLoud:
            minLoud = l
        if l > maxLoud:
            maxLoud = l
        if t < minTemp:
            minTemp = t
        if 1 > maxTemp:
            maxTemp = t

        keys.add(k)
        timeSigs.add(ts)

        if k == prevKey:
            currentKeyRun += 1
        if m == prevMode:
            currentModeRun += 1
        if ts == prevTS:
            currentTSRun += 1

        if currentKeyRun > longestKeyRun:
            longestKeyRun = currentKeyRun
        if currentModeRun > longestModeRun:
            longestKeyRun = currentModeRun
        if currentTSRun > longestTSRun:
            longestTSRun = currentTSRun
        

        loudness.append(l)
        tempo.append(t)
        times.append(section['start'])

        # All of these deal with the key switches and key runs
        if k != prevKey:
            keySwitches += 1
            prevKey = k
            if currentKeyRun < shortestKeyRun:
                shortestKeyRun = currentKeyRun
            currentKeyRun = 0
        if m != prevMode:
            modeSwitches += 1
            prevMode = m
            if currentModeRun < shortestModeRun:
                shortestModeRun = currentModeRun
            currentModeRun = 0
        if ts != prevTS:
            tsSwitches += 1
            prevTS = ts
            if currentTSRun < shortestTSRun:
                shortestTSRun = currentTSRun
            currentTSRun = 0

    # Return all of the data that was created.
    toRet = [sectionCount, sectionConfSum, loudnessSum, tempoSum, keySum, keyConfSum, modeSum, modeConfSum,
            tsSum, tsConfSum, sectionConfSum/sectionCount, loudnessSum/sectionCount, tempoSum/sectionCount,
            keySum/sectionCount, keySum/sectionCount, keyConfSum/sectionCount, modeSum/sectionCount,
            modeConfSum/sectionCount, tsSum/sectionCount, tsConfSum/sectionCount, minLoud, maxLoud, 
            minTemp, maxTemp, len(keys), len(timeSigs), shortestKeyRun, longestKeyRun, shortestModeRun,
            longestModeRun, shortestTSRun, longestTSRun, keySwitches, modeSwitches, tsSwitches]

    return toRet


def segmentAnalysis(segments):
    segmentCount = len(segments)

    segmentConfSum = 0
    for segment in segments:
        segmentConfSum += segment['confidence']

    # Get 100 random pitch vectors and 100 random timbre vectors
    pitches = []
    timbres = []
    datasetsToCollect = 100
    step = int(segmentCount / datasetsToCollect) - 1
    for i in range(0, datasetsToCollect):
        pitchToCollect = random.randint(step*i, (step+1)*i)
        timbreToCollect = random.randint(step*i, (step+1)*i)

        # Stores the pitches and timbres associated with this specific boy.
        try:
            pitch = segments[pitchToCollect]['pitches']
            timbre = segments[timbreToCollect]['timbre']
        except:
            pitch = [0,0,0,0,0,0,0,0,0,0,0,0]
            timre = [0,0,0,0,0,0,0,0,0,0,0,0]

        for i in range(0, 12):
            pitches.append(pitch[i])
            timbres.append(timbre[i])


    # Return everything here.
    toRet = [segmentConfSum / segmentCount, segmentCount]
    for i in pitches:
        toRet.append(i)
    for i in timbres:
        toRet.append(i)

    return toRet


# the ordering here is really quite important
def analyzeTrack(sp, trackID):
    analysis = sp.audio_analysis(trackID)
    features = sp.audio_features(trackID)

    bars = analysis['bars']
    beats = analysis['beats']
    sections = analysis['sections']
    segments = analysis['segments']
    tatums = analysis['tatums']

    finalAnalysis = []

    for i in barsAnalysis(bars):
        finalAnalysis.append(i)

    for i in beatAnalyis(beats):
        finalAnalysis.append(i)

    for i in sectionAnalysis(sections):
        finalAnalysis.append(i)

    for i in segmentAnalysis(segments):
        finalAnalysis.append(i)

    for i in tatumAnalysis(tatums):
        finalAnalysis.append(i)

    return finalAnalysis

# Returns all of the features of a track as stated by the spotify api
def featuresTrack(sp, trackID):
    features = sp.audio_features(trackID)[0]

    feat = [features['duration_ms'], features['key'], features['mode'], features['time_signature'], 
            features['acousticness'], features['danceability'], features['energy'], 
            features['instrumentalness'], features['liveness'], features['loudness'], 
            features['speechiness'], features['valence'], features['tempo']]

    return feat

def combineData(sp, trackID):
    features = featuresTrack(sp, trackID)
    analyis = analyzeTrack(sp, trackID)

    final = []

    for i in features:
        final.append(i)
    for i in analyis:
        final.append(i)

    return final

def main():
    
    # place the analytics in a text document, in the order of how they appear in the genres array and the txt files
    data = open("allData.txt", 'w')
    for genre in genres:
        if genre in ['alt-rock', 'alternative', 'anime', 'black-metal', 'bluegrass', 'blues', 'bossanova', 'classical', 'country', 'death-metal', 'disco', 'dubstep', 'edm', 'electronic', 'emo', 'folk', 'funk', 'gospel', 'goth', 'grunge', 'hard-rock', 'heavy-metal']:
            continue

        username = "bchapen"
        token = util.prompt_for_user_token(username,scope = 'user-top-read',client_id='407f7f8b0c314f42816264be391af790',client_secret='765d0a94dbec49e4b8a379ebe642404d',redirect_uri='https://example.com/callback')

        sp = spotipy.Spotify(auth=token)


        cur = open("songIDs/" + genre + "IDs.txt", 'r')
        lines = cur.readlines()
        count = 0

        for line in lines:
            line = line.rstrip("\n")
            
            dataForThisTrack = combineData(sp, line)
        
            for i in dataForThisTrack:
                data.write(str(i) + " ")
            data.write("\n")

            del dataForThisTrack
            gc.collect()

            count += 1
            print (genre + " " + str(count))
            if count == 500:
                print ("on to the next genre")
                print 
                break

            
        
        



if __name__ == "__main__":
    main()