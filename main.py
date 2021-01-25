from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.progressbar import MDProgressBar


class CircularButton(Label):
    active = ObjectProperty(False)


class AnimatedProgressBar(MDProgressBar):
    """
    Animated ProgressBar
    animate: Boolean value, we set it to declare if we want the progressbar to be animated or not
    completed: Boolean value, we set it to declare if the progressbar will be 'full' or 'empty'
    """
    animate = ObjectProperty(False)
    completed = ObjectProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.progress_bar_increment, 1 / 25)

    def progress_bar_increment(self, dt):
        if not self.animate:
            self.value = 0
            if self.completed:
                self.value = 100
            return
        if self.value >= 100:
            self.value = 0
        self.value += 1


class ProgressComponent(MDBoxLayout):
    """
    Component made from 2 ProgressBars and 3 CircularButtons
    step: Integer, the current step we want to choose on the progress component to show as active
    """
    step = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # workaround
        Clock.schedule_once(self.render_by_step, 0)

    def render_by_step(self, dt):
        if self.step > 0:  # first dot ()
            self.ids.step_1.active = True
        if self.step > 1:  # first pb ===
            self.ids.step_2.animate = True
        if self.step > 2:  # second dot ()
            self.ids.step_3.active = True
            self.ids.step_2.animate = False
            self.ids.step_2.completed = True
        if self.step > 3:  # second pb ===
            self.ids.step_4.animate = True
        if self.step > 4:  # third dot ()
            self.ids.step_5.active = True
            self.ids.step_4.animate = False
            self.ids.step_4.completed = True


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


window_manager = ScreenManager()
window_manager.add_widget(NewEntityWindow(name='new_entity'))
window_manager.add_widget(AddAreaWindow(name='add_area'))
window_manager.add_widget(AddWhatsappWindow(name='add_whatsapp'))
window_manager.add_widget(ValidateWhatsappWindow(name='validate_whatsapp'))
window_manager.add_widget(ShareCodeWindow(name='share_code'))
window_manager.current = "new_entity"


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = 'GuazuApp'
        screen = Builder.load_file('content.kv')
        return screen


MainApp().run()
