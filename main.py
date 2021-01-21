from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.toolbar import MDToolbar


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
        return Builder.load_file('content.kv')


MainApp().run()
