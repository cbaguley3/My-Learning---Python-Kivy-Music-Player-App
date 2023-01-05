import os
import random
import kivy
import time

from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton
from kivymd.app import MDApp
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.button import Button

# set app window size (x,y)
Window.size = (250,500)

class MyApp(MDApp):
    def build(self):
 
        layout = MDRelativeLayout(md_bg_color = [0/240,0/240,1/240,1])

        self.music_dir = "C:/Users/charl/projects/MusicPlayerApp"

        self.music_files = os.listdir(self.music_dir)

        print(self.music_files)

        self.song_list = [x for x in self.music_files if x.endswith(('mp3'))]

        self.song_count = len(self.song_list)

        print(self.song_list)

        # Track and Artist label positioning and font size
        self.songLabel = Label(pos_hint={'center_x':0.5, 'center_y':0.85},
                               size_hint = (1,1),
                               font_size = 18,
                               font_name = "Roboto")
       
        # Song Thumbnail positioning
        self.albumimage = Image(pos_hint={'center_x':0.5, 'center_y':0.55},
                               size_hint = (0.8,0.75))

        # Progress bar positioning
        self.currenttime = Label(text= "00:00",
                                 pos_hint={'center_x':.16,'center_y':.20},
                                 size_hint=(1,1),
                                 font_size=16)

        self.totaltime = Label(text= "00:00",
                                 pos_hint={'center_x':.84,'center_y':.20},
                                 size_hint=(1,1),
                                 font_size=16)


        self.progressbar = ProgressBar(max=100,
                                       value=0,
                                       pos_hint = {'center_x':0.5,'center_y':0.15},
                                       size_hint=(.8,.75))

        self.volumeslider = Slider(min=0,
                                   max=1,
                                   value=0.5,
                                   orientation='horizontal',
                                   pos_hint={'center_x':0.5, 'center_y':0.25},
                                   size_hint=(0.5,0.5))          


        # buttons functionality setup and layout positions

        self.playbutton = MDIconButton(pos_hint={'center_x':0.2, 'center_y':0.08},
                                       icon = 'play-button.png',
                                       on_press = self.playaudio)
        
        self.stopbutton = MDIconButton(pos_hint={'center_x':0.4, 'center_y':0.08},
                                       icon = 'stop-button.png',
                                       on_press = self.stopaudio, disabled =True)

        self.nextbutton = MDIconButton(pos_hint={'center_x':0.6, 'center_y':0.08},
                                       icon = 'fast-forward-button.png')

        self.backbutton = MDIconButton(pos_hint={'center_x':0.8, 'center_y':0.08},
                                       icon = 'fast-backward.png')

        layout.add_widget(self.playbutton)
        layout.add_widget(self.stopbutton)
        layout.add_widget(self.nextbutton)
        layout.add_widget(self.backbutton)
        layout.add_widget(self.songLabel)
        layout.add_widget(self.albumimage)
        layout.add_widget(self.progressbar)
        layout.add_widget(self.currenttime)
        layout.add_widget(self.totaltime)
        layout.add_widget(self.volumeslider)


        Clock.schedule_once(self.playaudio)


        # Sound level 
        def volume(instance,value):
            self.sound.volume = value
        self.volumeslider.bind(value = volume)

       
        return layout

    # play button
    def playaudio(self,obj):
        self.playbutton.disabled = True
        self.stopbutton.disabled = False
        self.song_title = self.song_list[random.randrange(0,self.song_count)]
        self.sound = SoundLoader.load('{}/{}'.format(self.music_dir,self.song_title))

        print()

        # match song title with song thumbnail
        self.songLabel.text = ""+ self.song_title[0:-4]+""
        self.albumimage.source = self.song_title[0:-4]+".jpg"

        self.sound.play()

        self.progressbarEvent = Clock.schedule_interval(self.updateprogressbar,self.sound.length/100)
        self.settimeEvent = Clock.schedule_interval(self.settime,1)
    
    # stop button
    def stopaudio(self,obj):
        self.playbutton.disabled = False
        self.stopbutton.disabled = True
        self.sound.stop()
        self.progressbarEvent.cancel()
        self.settimeEvent.cancel()
        self.progressbar.value = 0
        self.currenttime.text = "00:00"
        self.totaltime.text = "00:00"

    # song progress bar
    def updateprogressbar(self,value):
        if self.progressbar.value <100:
            self.progressbar.value +=1

    def settime(self,t):
        current_time = time.strftime('%M:%S',time.gmtime(self.progressbar.value*self.sound.length/100))
        total_time = time.strftime('%M:%S',time.gmtime(self.sound.length))

        self.currenttime.text = current_time
        self.totaltime.text = total_time

if __name__ ==  '__main__':
    MyApp().run()