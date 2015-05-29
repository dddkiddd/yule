#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

Y.tube Ü.rl L.ist É.xtrapolator
//Y.Ü.L.É//
by dddkiddd;

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import Tkinter as tk 
from Tkinter import Tk, BOTH
from ttk import Frame, Button, Style
import random, string
from bs4 import BeautifulSoup
from mechanize import Browser
import cPickle as pickle
from urllib2 import HTTPError 

urlList = []
urlBList = []

try:
    aList = pickle.load(open('goodlist.txt', 'rb'))
    BList = pickle.load(open('badlist.txt', 'rb'))
    for line in aList:
        urlList.append(line),
    for line in BList:
        urlBList.append(line),
except EOFError:
    pass
FIRE = False
root = Tk()
Stats = tk.StringVar()
Whatsup = tk.StringVar()
whatsup = "Go"
cdown = 0


def KILLMODE():
    global FIRE, cdown
    if (FIRE):
        cdown = cdown + 1
        global urlList, urlBList, Stats, stats
        # generate random ytube link
        x = ''.join([random.choice(string.ascii_letters + string.digits + "_-") for n in xrange(11)])
        while x in urlList or x in urlBList:
            print "Generated Duplicate Link; Re-generating"
            x = ''.join([random.choice(string.ascii_letters + string.digits + "_-") for n in xrange(11)])
        br = Browser()
        try:
            res = br.open("http://www.youtube.com/watch?v=" + x)
            data = res.get_data() 
            soup = BeautifulSoup(data)
            title = soup.find('title')
            # bad links are titled 'Youtube'
            if title.renderContents() != "YouTube":
                urlList.append("http://www.youtube.com/watch?v=" + x)
            # good links have other titles
            else:
                urlBList.append("http://www.youtube.com/watch?v="+ x)

        except HTTPError, e:
            print "Error ", e.code
            print "ERROR at:: http://www.youtube.com/watch?v=" + x

        Stats.set("TRIES THIS ATTEMPT: " + str(cdown) + "\nSUCCESS: " + str(len(urlList)) + "\nFAIL: " + str(len(urlBList)))
    root.after(15000, KILLMODE)

class mainWindow(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self)   
        self.parent = parent
        self.initUI()

    def goPher(self):
        global FIRE
        global Whatsup
        global whatsup
        if FIRE:
            print "stopping"
            whatsup = "Go"
            FIRE = False
        else:
            print "going"
            whatsup = "Stop"
            FIRE = True
        Whatsup.set(whatsup)

    def saveQuit(self):
        print "savequit"
        global urlList, urlBList
        pickle.dump( urlList, open( 'goodlist.txt', 'wb' ))
        pickle.dump( urlBList, open( 'badlist.txt', 'wb' ))
        root.quit()

        
    def initUI(self):
        self.parent.title("Y.tube Ü.rl L.ist É.xtrapolator")
        self.style = Style()
        self.style.theme_use("default")

        self.pack(fill=BOTH, expand=1)

        global urlList, Stats, Whatsup, whatsup
        Whatsup.set(whatsup)
        stats = "SUCCESS: " + str(len(urlList)) + "\nFAIL: " + str(len(urlBList))
        Stats.set(stats)
        mainLabel = tk.Label(self, textvariable = Stats)
        mainLabel.pack()
        quitButton = Button(self, text="Save & Quit",
            command=self.saveQuit)
        quitButton.place(x=85, y=80)
        goButton = Button(self, command=self.goPher, textvariable = Whatsup)
        goButton.place(x=5, y=80)
        goButton.pack()


def main():
    global root
    root.geometry("250x150+300+300")
    app = mainWindow(root)
    KILLMODE()
    root.mainloop()

if __name__ == '__main__':
    main()  
