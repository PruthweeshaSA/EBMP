import librosa as lr;
import os;

with open('metaverage.txt', 'r') as f:
    metaverage = f.read() # Read whole file in the file_content string
print(metaverage);
properties=[];
lines=metaverage.split('\n');
for line in lines:
    #print(line);
    values=line.split();
    floatValues=[];
    #print(values);
    for element in values:
        #print(element);
        element1=float(element);
        floatValues.append(element1);
    properties.append(values);


def reclassify():

    DirectoryNames=["WAV_Angry_Songs_1","WAV_Fear_Songs_1","WAV_Happy_Songs_1","WAV_Sad_Songs_1","WAV_Surprise_Songs_1"];
    
    AngrySongs=os.listdir("WAV_Angry_Songs_1");
    FearSongs=os.listdir("WAV_Fear_Songs_1");
    HappySongs=os.listdir("WAV_Happy_Songs_1");
    SadSongs=os.listdir("WAV_Sad_Songs_1");
    SurpriseSongs=os.listdir("WAV_Surprise_Songs_1");

    AllSongs=[AngrySongs,FearSongs,HappySongs,SadSongs,SurpriseSongs];

    for i in range(0,len(AllSongs)):
        directory=AllSongs[i];
        directoryName=DirectoryNames[i];
        for song in directory:
            verdict=analyze(directoryName,song);
            if(not verdict in directoryName):
                print("reclassify "+directoryName+"\\"+song+" to WAV_"+verdict+"_Songs_1");
            
    
    


def analyze(directory,song):
    filename=directory+'\\'+song;
    y, sr = lr.load(filename);
    stream=lr.stream(filename,block_length=256,frame_length=256,hop_length=256);
    duration=lr.get_duration(y=y,sr=sr);
    rolloffs=[];
    bandwidths=[];
    contrasts=[];
    centroids=[];
    rmss=[];
    
    SumRolloff=0;
    SumBandwidth=0;
    SumContrast=0;
    SumCentroid=0;
    SumRms=0;
    for segment in stream:
        rolloff=lr.feature.spectral_rolloff(y=segment,sr=sr);
        rolloffs.append(rolloff);
        #rolloff=rolloff.tolist();
        for arr in rolloff:
            for integer in arr:
                SumRolloff+=integer;

        #bandwidth=lr.feature.spectral_bandwidth(y=segment,sr=sr);
        #bandwidths.append(bandwidth);
        #bandwidth=bandwidth.tolist();
        #for arr in bandwidth:
        #    for integer in arr:
        #        SumBandwidth+=integer;
        #contrast=lr.feature.spectral_contrast(y=segment,sr=sr);
        #contrasts.append(contrast);
        ##contrast=contrast.tolist();
        #for arr in contrast:
        #    for integer in arr:
        #        SumContrast+=integer;
        #centroid=lr.feature.spectral_centroid(y=segment,sr=sr);
        #centroids.append(centroid);
        ##centroid=centroid.tolist();
        #for arr in centroid:
        #    for integer in arr:
        #        SumCentroid+=integer;
        #rms = lr.feature.rms(y=segment);
        #rmss.append(rms);
        ##rms=rms.tolist();
        #for arr in rms:
        #    for integer in arr:
        #        SumRms+=integer;
    
    SongRolloff=SumRolloff/duration;

    #SongBandwidth=SumBandwidth/duration;
    #SongContrast=SumContrast/duration;
    #SongCentroid=SumCentroid/duration;
    #SongRms=SumRms/duration;

    #verdict=analyze_properties(SongRolloff,SongBandwidth,SongContrast,SongCentroid,SongRms);
    verdict=rank_analyze_properties(SongRolloff);
    return verdict;


def analyze_properties(rolloff,bandwidth,contrast,centroid,rms):
    global properties;
    #rolloff=float(input('rolloff'));
    #bandwidth=float(input('bandwidth'));
    #contrast=float(input('contrast'));
    #centroid=float(input('centroid'));
    #rms=float(input('rms'));

    rolloffDelta=[];
    for element in properties[0]:
        element1=float(element);
        diff=rolloff-element1;
        if(diff<0):
            diff=-diff;
        rolloffDelta.append(diff);

    verdict=0;
    for i in range(1,5):
        if(rolloffDelta[i]<rolloffDelta[verdict]):
            verdict=i;

    if(verdict==0 or verdict==2):
        rmsDelta=[];
        angry_happy=[properties[4][0],properties[4][2]]
        for element in angry_happy:
            element1=float(element);
            diff=rms-element1;
            if(diff<0):
                diff=-diff;
            rmsDelta.append(diff);

        verdict2=0;
        if(rmsDelta[1]<rmsDelta[verdict2]):
            verdict2=2;

        if(not verdict==verdict2):
            verdict=verdict2;

    emotionList=['Angry','Fear','Happy','Sad','Surprise','Neutral'];
    print(emotionList[verdict]);
    return emotionList[verdict];

def rank_analyze_properties(rolloff):
    with open('rank.txt', 'r') as f:
        ranks = f.read() # Read whole file in the file_content string
    #print(ranks);
    lines=ranks.split('\n');
    rankedEmotions=lines[0].split();
    rankedRolloffs=lines[1].split();
    floatRankedRolloffs=[];
    for rank in rankedRolloffs:
        floatRankedRolloffs.append(float(rank));
    verdict=0;
    for rank in floatRankedRolloffs:
        if(rolloff>rank):
            verdict+=1;
        else:
            return rankedEmotions[verdict];
    return rankedEmotions[verdict];

def main():
    reclassify();
    directory=input('directory');
    song=input('song');
    analyze(directory,song);

if __name__ == "__main__":
    main();
        
    
    
    
