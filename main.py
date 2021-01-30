import re

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField


class CircularButton(Label):
    active = ObjectProperty(False)


class NumericField(MDTextField):
    pat = re.compile('[^0-9]')
    limit = 13

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        if len(self.text) < self.limit:
            return super(NumericField, self).insert_text(s, from_undo=from_undo)
        return


class ProgressComponent(MDBoxLayout):
    """
    Component made from 2 ProgressBars and 3 CircularButtons
    step: Integer, the current step we want to choose on the progress component to show as active
    """
    step = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.render_by_step, 0)

    def render_by_step(self, dt):
        if self.step == 1:  # first dot ()
            self.ids.step_1.active = True
        if self.step == 2:  # first pb ===
            self.ids.step_1.active = True
            self.ids.step_2.start()
        if self.step == 3:  # second dot ()
            self.ids.step_1.active = True
            self.ids.step_2.value = 100.0
            self.ids.step_3.active = True
        if self.step == 4:  # second pb ===
            self.ids.step_1.active = True
            self.ids.step_2.value = 100.0
            self.ids.step_3.active = True
            self.ids.step_4.start()
        if self.step == 5:  # third dot ()
            self.ids.step_1.active = True
            self.ids.step_2.value = 100.0
            self.ids.step_3.active = True
            self.ids.step_4.value = 100.0
            self.ids.step_5.active = True


class NewEntityWindow(Screen):
    pass


class AddAreaWindow(Screen):
    pass


class AddWhatsappWindow(Screen):
    pass


class ValidateWhatsappWindow(Screen):
    pass


class ShareCodeWindow(Screen):
    pass


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = 'GuazuApp'
        Window.size = (360, 640)
        screen = Builder.load_file('content.kv')
        return screen

    def close_app(self):
        self.get_running_app().stop()


MainApp().run()
