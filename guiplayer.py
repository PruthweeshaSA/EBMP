import vlc;
import easygui;
import sys;
import os;

choice='';
player=None;

def setPlayer(player1):
    global player;
    player=player1;

def display(song):
    global choice;
    global player;
    player=vlc.MediaPlayer(song);
    player.play();
    while(True and not choice=='destruct'):
        choice = easygui.buttonbox(choices=['Play','Pause','Stop','New']);
        if(choice=='Play'):
            player.play();
        elif(choice=='Pause'):
            player.pause();
        elif(choice=='Stop'):
            player.stop();
        elif(choice=='New'):
            song=easygui.fileopenbox();
            player=vlc.MediaPlayer(song);
        else:
            break;

def stop(player):
    player.stop();

def pause(player):
    player.pause();

def play(player):
    player.play();


if(__name__=='__main__'):
    f=open('pid.txt','w');
    pid=os.getpid();
    f.write(str(pid));
    f.close();
    display(sys.argv[1]);
        
