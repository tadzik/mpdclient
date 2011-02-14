# -*- coding: utf-8 -*-
# <Copyright and license information goes here.>
from PyQt4.QtCore import *
from PyKDE4.plasma import Plasma
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4 import plasmascript
from socket import error as SocketError
import mpd

HOST = 'localhost'
PORT = 6600
 
class MPDClient(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)
 
    def init(self):
        self.setHasConfigurationInterface(False)
        self.setAspectRatioMode(Plasma.Square)
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)

        self.label = Plasma.Label(self.applet)
        self.layout.addItem(self.label)

        self.mpd = mpd.MPDClient()
        self.mpd.connect(HOST, PORT)
        
        self.timer = QTimer()
        self.timer.connect(self.timer, SIGNAL('timeout()'), self.timeout)
        self.timer.start(1000)
        self.timeout()

        self.resize(300, 100)

    def timeout(self):
        if self.mpd.status()['state'] != 'play':
            self.label.setText('Music stopped')
            return

        currentSong = self.mpd.currentsong()
        title = album = artist = ''

        try:
            title = currentSong['title']
        except:
            title = currentSong['file'].split("/")[-1]

        try:
            str = currentSong['artist'] + ' - ' + title
        except:
            str = title

        try:
            album = currentSong['album']
            str = str + "\n" + album
        except:
            pass
        
        self.label.setText(str)

def CreateApplet(parent):
    return MPDClient(parent)
