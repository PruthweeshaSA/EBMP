import numpy as np;
import librosa as lr;
import os;


class Neuron:
    def __init__(self, weights, bias):
        self.weights=weights;
        self.bias=bias;
            
    def feedForward(self,inputs):
        total=np.dot(self.weights,inputs)+self.bias;
        return 1/(1+np.exp(-total));


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
        bandwidth=lr.feature.spectral_bandwidth(y=segment,sr=sr);
        bandwidths.append(bandwidth);
        #bandwidth=bandwidth.tolist();
        for arr in bandwidth:
            for integer in arr:
                SumBandwidth+=integer;
        contrast=lr.feature.spectral_contrast(y=segment,sr=sr);
        contrasts.append(contrast);
        #contrast=contrast.tolist();
        for arr in contrast:
            for integer in arr:
                SumContrast+=integer;
        centroid=lr.feature.spectral_centroid(y=segment,sr=sr);
        centroids.append(centroid);
        #centroid=centroid.tolist();
        for arr in centroid:
            for integer in arr:
                SumCentroid+=integer;
        rms = lr.feature.rms(y=segment);
        rmss.append(rms);
        #rms=rms.tolist();
        for arr in rms:
            for integer in arr:
                SumRms+=integer;
    
    SongRolloff=SumRolloff/duration;
    SongBandwidth=SumBandwidth/duration;
    SongContrast=SumContrast/duration;
    SongCentroid=SumCentroid/duration;
    SongRms=SumRms/duration;

def printlist(list_a):
    a='';
    for i in list_a:
        a+=(str(i)+" ");
    return a;

def main():
    emotionNames=["Angry","Fear","Happy","Sad","Surprise"];
    rankedEmotions=["Angry","Fear","Happy","Sad","Surprise"];
    directoryNames=["WAV_Angry_Songs_1","WAV_Fear_Songs_1","WAV_Happy_Songs_1","WAV_Sad_Songs_1","WAV_Surprise_Songs_1"];
    directorySize=24;
    
    AngrySongs=os.listdir("WAV_Angry_Songs_1");
    FearSongs=os.listdir("WAV_Fear_Songs_1");
    HappySongs=os.listdir("WAV_Happy_Songs_1");
    SadSongs=os.listdir("WAV_Sad_Songs_1");
    SurpriseSongs=os.listdir("WAV_Surprise_Songs_1");

    emotionList=[AngrySongs,FearSongs,HappySongs,SadSongs,SurpriseSongs];
    SumRolloff=0;
    SumBandwidth=0;
    SumContrast=0;
    SumCentroid=0;
    SumRms=0;

    metaRolloff=[];
    metaBandwidth=[];
    metaContrast=[];
    metaCentroid=[];
    metaRms=[];

    allSongRolloff=[];
    allSongBandwidth=[];
    allSongContrast=[];
    allSongCentroid=[];
    allSongRms=[];

    outfile="averages.txt";
    metafile="metaverage.txt";
    rankfile="rank.txt";
    outwriter=open(outfile,'w+');
    metawriter=open(metafile,'w+');

    for i in range(0,len(emotionList)):
        emotion=emotionList[i]
        emotionName=emotionNames[i];
        directory=directoryNames[i];
        outwriter.write(emotionName + ':\n');
        #metawriter.write(emotionName + ':\n');
        
        metaRolloff.append(0);
        metaBandwidth.append(0);
        metaContrast.append(0);
        metaCentroid.append(0);
        metaRms.append(0);
        for song in emotion:
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
                bandwidth=lr.feature.spectral_bandwidth(y=segment,sr=sr);
                bandwidths.append(bandwidth);
                #bandwidth=bandwidth.tolist();
                for arr in bandwidth:
                    for integer in arr:
                        SumBandwidth+=integer;
                contrast=lr.feature.spectral_contrast(y=segment,sr=sr);
                contrasts.append(contrast);
                #contrast=contrast.tolist();
                for arr in contrast:
                    for integer in arr:
                        SumContrast+=integer;
                centroid=lr.feature.spectral_centroid(y=segment,sr=sr);
                centroids.append(centroid);
                #centroid=centroid.tolist();
                for arr in centroid:
                    for integer in arr:
                        SumCentroid+=integer;
                rms = lr.feature.rms(y=segment);
                rmss.append(rms);
                #rms=rms.tolist();
                for arr in rms:
                    for integer in arr:
                        SumRms+=integer;
            
            SongRolloff=SumRolloff/duration;
            SongBandwidth=SumBandwidth/duration;
            SongContrast=SumContrast/duration;
            SongCentroid=SumCentroid/duration;
            SongRms=SumRms/duration;

            metaRolloff[-1]+=SongRolloff;
            metaBandwidth[-1]+=SongBandwidth;
            metaContrast[-1]+=SongContrast;
            metaCentroid[-1]+=SongCentroid;
            metaRms[-1]+=SongRms;

            allSongRolloff.append(SongRolloff);
            
            outwriter.write('Song Rolloff = ' + str(SongRolloff) + '\n');
            outwriter.write('Song Bandwidth = ' + str(SongBandwidth) + '\n');
            outwriter.write('Song Contrast = ' + str(SongContrast) + '\n');
            outwriter.write('Song Centroid = ' + str(SongCentroid) + '\n');
            outwriter.write('Song RMS = ' + str(SongRms) + '\n\n');
        outwriter.write('\n');
        
        metaRolloff[-1]/=directorySize;
        metaBandwidth[-1]/=directorySize;
        metaContrast[-1]/=directorySize;
        metaCentroid[-1]/=directorySize;
        metaRms[-1]/=directorySize;
        
    outwriter.close();
    
    metawriter.write(printlist(metaRolloff)+'\n');
    metawriter.write(printlist(metaBandwidth)+'\n');
    metawriter.write(printlist(metaContrast)+'\n');
    metawriter.write(printlist(metaCentroid)+'\n');
    metawriter.write(printlist(metaRms)+'\n');

    metawriter.close();

    sortedMetaRolloff=[];

    for element in metaRolloff:
        sortedMetaRolloff.append(element);

    length=len(metaRolloff);
    for i in range(0,length):
        for j in range(i+1,length):
            if(sortedMetaRolloff[i]>sortedMetaRolloff[j]):
                temp=sortedMetaRolloff[i];
                sortedMetaRolloff[i]=sortedMetaRolloff[j];
                sortedMetaRolloff[j]=temp;
                temp2=rankedEmotions[i];
                rankedEmotions[i]=rankedEmotions[j];
                rankedEmotions[j]=temp2;

    sortedRolloffs=sorted(allSongRolloff);
    rankRolloffs=[sortedRolloffs[directorySize-1],sortedRolloffs[2*directorySize-1],sortedRolloffs[3*directorySize-1]];
    rankRolloffs.append(sortedRolloffs[4*directorySize-1]);
    rankwriter=open(rankfile,'w+');
    rankwriter.write(printlist(rankedEmotions)+'\n');
    rankwriter.write(printlist(rankRolloffs)+'\n');
    rankwriter.close();


if(__name__=='__main__'):
    main();


