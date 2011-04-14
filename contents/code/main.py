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
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.layout = QGraphicsLinearLayout(Qt.Vertical, self.applet)

        self.label = Plasma.Label(self.applet)
        self.label.setWordWrap(False)
        self.layout.addItem(self.label)

        self.mpd = mpd.MPDClient()
        try:
            self.mpd.connect(HOST, PORT)
        except:
            pass
        
        self.timer = QTimer()
        self.timer.connect(self.timer, SIGNAL('timeout()'), self.timeout)
        self.timer.start(1000)
        self.timeout()

    def timeout(self):
        status = ''
        try:
            status = self.mpd.status()['state']
        except:
            try:
                self.mpd.connect(HOST, PORT)
            except:
                pass
        if status != 'play':
            self.label.setText('Music stopped')
            return

        currentSong = self.mpd.currentsong()
        title = album = artist = ''
        longstr = '<b>'
        str = ''

        try:
            title = currentSong['title']
        except:
            title = currentSong['file'].split("/")[-1]

        try:
            str = str + currentSong['artist'] + ' - ' + title
        except:
            str = str + title

        try:
            album = currentSong['album']
        except:
            pass
        
        self.label.setText(str.decode('utf-8')[0:50])

def CreateApplet(parent):
    return MPDClient(parent)
