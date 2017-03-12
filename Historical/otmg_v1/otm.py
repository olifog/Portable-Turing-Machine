import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
from kivy.core.window import Window
from knob import Knob


class OtmKnob(Knob):

    def on_touch_move(self, touch):
        super(OtmKnob, self).on_touch_move(touch)
        self.parent.parent.row1.gear_left.anim_delay = (self.value / 100.0) * .1
        self.parent.parent.row1.gear_right.anim_delay = (self.value / 100.0) * .1

    def on_touch_down(self, touch):
        super(OtmKnob, self).on_touch_down(touch)
        self.parent.parent.row1.gear_left.anim_delay = (self.value / 100.0) * .1
        self.parent.parent.row1.gear_right.anim_delay = (self.value / 100.0) * .1

class Otm(BoxLayout):

    gear_dir = 'cw'

    def __init__(self, **kwargs):
        super(Otm, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.row1 = BoxLayout()
        self.row1.gear_left = Image(source='lcw.zip', anim_delay=.01)
        self.row1.add_widget(self.row1.gear_left)
        self.row1.btn1 = Button(text='Reverse Gears')
        self.row1.btn1.bind(on_press=self.do_reverse)
        self.row1.add_widget(self.row1.btn1)
        self.row1.gear_right = Image(source='rcw.zip', anim_delay=.01)
        self.row1.add_widget(self.row1.gear_right)
        self.add_widget(self.row1)

        self.row2 = BoxLayout()
        self.row2.knob_left = Builder.load_string('''
OtmKnob:
    size: 100, 100
    value: 0
    show_marker: True
    knobimg_source: "knob/img/knob_metal.png"
    marker_img: "knob/img/bline.png"
    markeroff_color: 0.3, 0.3, .3, 1
''')
        self.row2.add_widget(self.row2.knob_left)
        self.row2.btn2 = Button(text='Lower Button')
        self.row2.btn2.bind(on_press=self.do_action)
        self.row2.add_widget(self.row2.btn2)
        self.row2.add_widget(Label(text='Label before button press'))
        self.add_widget(self.row2)

    def do_reverse(self, value):
        if self.gear_dir is 'cw':
            self.row1.gear_right.source = 'rccw.zip'
            self.row1.gear_left.source = 'lccw.zip'
            self.gear_dir = 'ccw'
        else:
            self.row1.gear_right.source = 'rcw.zip'
            self.row1.gear_left.source = 'lcw.zip'
            self.gear_dir = 'cw'

    def do_action(self, value):
        print('The lower button <%s> is being pressed' % value.text)


class OtmApp(App):
    def build(self):
        return Otm()

if __name__ == '__main__':
    Config.set('graphics','resizable',0)
    Window.size = (800, 480)
    OtmApp().run()
