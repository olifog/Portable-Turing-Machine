import kivy, sys, os
kivy.require('1.9.1')

from kivy.uix.slider import Slider
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.button import Button
from LabelB import LabelB
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.uix.togglebutton import ToggleButton
from kivy.config import Config
from functools import partial
from knob import Knob
from kivy.core.window import Window
from kivy.clock import Clock

from otm import Otm

Window.clearcolor = (1, 1, 1, 1)

def txtformat(text):
    ret = []
    for line in text:
        if line == '\n' or line[0] == ';':
            ret.append(line)
        else:
            linelis = line.split(" ")
            ret.append("")
            for obj in linelis:
                if len(obj) == 1 and not obj == "0":
                    ret[len(ret) - 1] += obj
                else:
                    ret[len(ret) - 1] += "{:5}".format(obj)
                ret[len(ret) - 1] += " "
            ret[len(ret) - 1] = ret[len(ret) - 1][:len(ret[len(ret) - 1]) - 1].rstrip() + "\n"
    return ret

class OtmgSlider(Slider):
    def speed(self):
        return ((100 - self.value) / 100.0) * .1

    def on_touch_move(self, touch):
        super(OtmgSlider, self).on_touch_move(touch)
        amount = self.speed()
        if self.parent.parent.state == "Run":
            self.parent.parent.row2.gear_left.anim_delay = amount
            self.parent.parent.row2.gear_right.anim_delay = amount

    def on_touch_down(self, touch):
        super(OtmgSlider, self).on_touch_down(touch)
        amount = self.speed()
        if self.parent.parent.state == "Run":
            self.parent.parent.row2.gear_left.anim_delay = amount
            self.parent.parent.row2.gear_right.anim_delay = amount

class Otmg(BoxLayout):

    gear_dir = 'cw'
    state = "Stop"
    

    def __init__(self, **kwargs):
        super(Otmg, self).__init__(**kwargs)

        self.progs = os.listdir("../../otmp")
        self.prog = "Roman_Numeral_Square_Root"
        
        self.otm = Otm(" ")
        self.otm.load(self.prog)
        self.alph = self.otm.findchars()

        self.lastloc = 0
        self.movedloc = False
        self.lastleftknob = 0
        self.lastrightknob = 0
        self.lastinput = [" "]
        self.setlast = False

        self.orientation = 'vertical'
        self.padding = 20

        self.row0 = BoxLayout(size_hint=(1,0.1))
        self.row0.prev = Button(text="Previous", size_hint=(0.25,1))
        self.row0.prev.bind(on_press=self.prev)
        self.row0.add_widget(self.row0.prev)
        self.row0.title = LabelB(text=self.prog.replace("_", " "),
                size_hint=(0.5, 1),
                halign='center', 
                valign='top',
                color=(0, 0, 0, 1),
                font_size=25,
                bcolor=(1, 1, 1, 1))
        self.row0.add_widget(self.row0.title)
        self.row0.nex = Button(text="Next", size_hint=(0.25,1))
        self.row0.nex.bind(on_press=self.nex)
        self.row0.add_widget(self.row0.nex)
        self.add_widget(self.row0)

        self.row1 = BoxLayout(size_hint=(1,0.2))
        self.row1.tape = LabelB(text=self.otm.croptape(25), 
            size_hint=(1, 1),
            halign='center', 
            valign='top',
            color=(0, 0, 0, 1),
            font_size=25,
            bcolor=(210/255.0,105/255.0,30/255.0,1),
            font_name='Courier New Bold')
        self.row1.add_widget(self.row1.tape)
        self.add_widget(self.row1)

        self.row15 = BoxLayout(size_hint=(1, 0.01))
        self.row15.pointer = LabelB(text='^',
                halign='center',
                color=(0, 0, 0 ,1),
                bcolor=(210/255.0,105/255.0,30/255.0, 1),
                valign = 'top')
        self.row15.add_widget(self.row15.pointer)
        self.add_widget(self.row15)

        self.row2 = BoxLayout(orientation='horizontal')
        self.row2.it1 = BoxLayout(orientation='vertical')
        self.row2.it2 = BoxLayout(orientation='horizontal')
        self.row2.it3 = BoxLayout(orientation='vertical')
        
        self.row2.gear_left = Image(source='cw.zip', anim_delay=-1, size_hint=(1, 1))
        self.row2.it1.add_widget(self.row2.gear_left)
        self.row2.desc1 = BoxLayout(orientation='horizontal')
        self.row2.actdesc1 = Button(text=" ",
                font_size=25,
                color=(0, 0, 0, 1),
                background_color=(32/255.0,178/255.0,170/255.0, 1),
                size_hint=(1, 1),
                background_normal='')
        self.row2.actdesc1.bind(on_press=self.write_char)
        self.row2.knob_left = Knob(size=(125,125),
                step=100/len(self.alph),
                knobimg_source="knob/img/knob_metal.png", 
                marker_img="knob/img/bline.png",
                markeroff_color=(0.3, 0.3, 0.3, 1))
        self.row2.knob_left.bind(on_touch_move=self.change_char)
        self.row2.desc1.add_widget(self.row2.knob_left)
        self.row2.desc1.add_widget(self.row2.actdesc1)
        self.row2.it1.add_widget(self.row2.desc1)
        
        self.row2.it2.program = LabelB(text=''.join(txtformat(self.otm.cropprog(3))),
                color=(0, 0, 0, 1),
                halign='left',
                valign='top',
                bcolor=(218/255.0,165/255.0,32/255.0, 1),
                size_hint=(0.9, 1),
                font_size=20,
                font_name="Courier New Bold",
                text_size=(200, None))
        self.row2.it2.pointer = LabelB(text='->',
                color=(0, 0, 0, 1),
                halign='right',
                valign='middle',
                size_hint=(0.1, 1),
                bcolor=(218/255.0,165/255.0,32/255.0, 1))
        self.row2.it2.add_widget(self.row2.it2.pointer)
        self.row2.it2.add_widget(self.row2.it2.program)

        
        self.row2.gear_right = Image(source='cw.zip', anim_delay=-1, size_hint=(1, 1))
        self.row2.it3.add_widget(self.row2.gear_right)
        self.row2.desc2 = BoxLayout(orientation='horizontal')
        self.row2.actdesc2 = LabelB(text='Location -->', color=(0, 0, 0, 1), bcolor=(32/255.0,178/255.0,170/255.0, 1))
        self.row2.knob_right = Knob(size=(125,125), 
                knobimg_source="knob/img/knob_metal.png", 
                marker_img="knob/img/bline.png",
                markeroff_color=(0.3, 0.3, 0.3, 1))
        self.row2.knob_right.bind(on_touch_move=self.set_location)
        self.row2.desc2.add_widget(self.row2.actdesc2)
        self.row2.desc2.add_widget(self.row2.knob_right)
        self.row2.it3.add_widget(self.row2.desc2)

        self.row2.add_widget(self.row2.it1)
        self.row2.add_widget(self.row2.it2)
        self.row2.add_widget(self.row2.it3)
        self.add_widget(self.row2)
        
        self.row3 = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))
        self.row3.slider = OtmgSlider(min=0, max=100, value=0)
        self.row3.add_widget(self.row3.slider)
        self.add_widget(self.row3)

        self.row4 = BoxLayout(orientation='horizontal', size_hint=(1, 0.2))
        self.row4.btn1 = ToggleButton(text='Start/Stop')
        self.row4.btn1.bind(on_press=self.do_startstop)
        self.row4.add_widget(self.row4.btn1)
        self.row4.btn2 = Button(text='Step')
        self.row4.btn2.bind(on_press=self.do_step_request)
        self.row4.add_widget(self.row4.btn2)
        self.row4.btn3 = Button(text='Restart')
        self.row4.btn3.bind(on_press=self.restart)
        self.row4.add_widget(self.row4.btn3)
        self.row4.btn4 = Button(text='Clear')
        self.row4.btn4.bind(on_press=self.do_clear)
        self.row4.add_widget(self.row4.btn4)
        self.row4.btn5 = Button(text='EXIT')
        self.row4.btn5.bind(on_press=self.exit)
        self.row4.add_widget(self.row4.btn5)

        self.add_widget(self.row4)

    def exit(self, value):
        sys.exit()
    
    def write_char(self, value):
        self.otm.tape[self.otm.index] = self.row2.actdesc1.text
        self.otm.moveright()
        self.row1.tape.text=self.otm.croptape(25)

    def change_char(self, val, val2):
        if self.lastleftknob != self.row2.knob_left.value:
            self.row2.actdesc1.text = self.alph[int(round(self.row2.knob_left.value / (100 / len(self.alph))) - 1)]
            self.lastleftknob = self.row2.knob_left.value

    def restart(self, val):
        self.otm.tape = self.lastinput
        self.otm.index = 0
        self.otm.state = "0"
        self.row1.tape.text=self.otm.croptape(25)
        self.row2.it2.program.text=''.join(txtformat(self.otm.cropprog(3)))
        self.setlast = False

    def nex(self, value):
        try:
            self.prog = self.progs[self.progs.index(self.prog) + 1]
        except:
            self.prog = self.progs[0]
        self.do_clear(None)
        self.row0.title.text = self.prog.split(".")[0].replace("_", " ")
        self.otm.load(self.prog.split(".")[0])
        self.alph = self.otm.findchars()
        self.row1.tape.text=self.otm.croptape(25)
        self.row2.it2.program.text=''.join(txtformat(self.otm.cropprog(3)))

    def prev(self, value):
        try:
            self.prog = self.progs[self.progs.index(self.prog) - 1]
        except:
            self.prog = self.progs[len(self.progs) - 1]
        
        self.do_clear(None)
        self.row0.title.text = self.prog.split(".")[0].replace("_", " ")
        self.otm.load(self.prog.split(".")[0])
        self.alph = self.otm.findchars()
        self.row1.tape.text=self.otm.croptape(25)
        self.row2.it2.program.text=''.join(txtformat(self.otm.cropprog(3)))

    def set_location(self, touch, value):
        if self.lastrightknob != self.row2.knob_right.value:
            self.lastrightknob = self.row2.knob_right.value
            if self.state == "Stop":
                self.movedloc = True
                prev = self.otm.index
                self.otm.index = int(round((len(self.otm.tape) / 100) * self.row2.knob_right.value))
                self.row1.tape.text=self.otm.croptape(25)
                if self.otm.index > prev:
                    self.row2.gear_left.source = 'cw.zip'
                    self.row2.gear_right.source = 'cw.zip'
                elif self.otm.index < prev:
                    self.row2.gear_right.source = 'ccw.zip'
                    self.row2.gear_left.source = 'ccw.zip'
                else:
                    return
                self.row2.gear_left.anim_loop=1
                self.row2.gear_right.anim_loop=1
                self.row2.gear_left.anim_delay= self.row3.slider.speed()
                self.row2.gear_right.anim_delay= self.row3.slider.speed()
                self.row2.gear_left.anim_delay=0.01
                self.row2.gear_right.anim_delay=0.01

    def do_clear(self, value):
        self.otm.__init__()
        self.row1.tape.text=" "
        self.row2.it2.program.text=""
        self.row2.knob_left.value=0
        self.row2.knob_right.value=0
        self.row0.title.text = ""
        self.state = "Stop"
        self.setlast = False
        self.lastinput = [" "]
        self.row2.gear_left.anim_delay=-1
        self.row2.gear_right.anim_delay=-1
        self.row3.slider.value = 0
        self.row4.btn1.state='normal'

    def do_step(self, value):
        if not self.setlast:
            self.lastinput = self.otm.tape
            self.setlast = True
        
        if self.row2.it2.program.text == "Finished!":
            self.state = "Stop"
            self.row2.gear_right.anim_loop=-1
            self.row2.gear_left.anim_loop=-1
            return
        if self.movedloc:
            self.otm.index = self.lastloc
            self.movedloc = False
        self.otm.tick()
        self.row1.tape.text=self.otm.croptape(25)
        self.row2.it2.program.text=''.join(txtformat(self.otm.cropprog(3)))
        self.lastloc = self.otm.index
        if self.otm.lastdir == 'r':
            self.row2.gear_right.source = 'ccw.zip'
            self.row2.gear_left.source = 'ccw.zip'
        elif self.otm.lastdir == 'l':
            self.row2.gear_left.source = 'cw.zip'
            self.row2.gear_right.source = 'cw.zip'

    def do_step_request(self, value):
        if self.row2.it2.program.text == "Finished!":
            self.state = "Stop"
            self.row2.gear_right.anim_loop=-1
            self.row2.gear_left.anim_loop=-1
            return
        if self.state != "Run":
            self.do_step(None)
            self.row2.gear_left.anim_loop=1
            self.row2.gear_right.anim_loop=1
            self.row2.gear_left.anim_delay= self.row3.slider.speed()
            self.row2.gear_right.anim_delay= self.row3.slider.speed()
            self.row2.gear_left.anim_delay=0.01
            self.row2.gear_right.anim_delay=0.01
        
    def do_startstop(self, value):
        self.row2.gear_left.anim_loop=0
        self.row2.gear_right.anim_loop=0
        if self.state == "Run":
            self.state = "Stop"
            self.row2.gear_left.anim_delay=-1
            self.row2.gear_right.anim_delay=-1
        elif not self.row2.it2.program.text == "Finished!":
            self.state = "Run"
            Clock.schedule_once(self.runstep_callback, 0.5)
            self.row2.gear_left.anim_delay= self.row3.slider.speed()
            self.row2.gear_right.anim_delay= self.row3.slider.speed()

    def runstep_callback(self, dt):
        if self.state == "Run":
            self.do_step(None)
            Clock.schedule_once(self.runstep_callback, self.row3.slider.speed() * 5)
            self.row2.gear_left.anim_loop=0
            self.row2.gear_right.anim_loop=0
            self.row2.gear_left.anim_delay= self.row3.slider.speed()
            self.row2.gear_right.anim_delay= self.row3.slider.speed()

class OtmgApp(App):
    def build(self):
        return Otmg()

if __name__ == '__main__':
    Config.set('graphics','resizable',0)
    Window.size = (800, 480)
    OtmgApp().run()
