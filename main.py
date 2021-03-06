import re
import uuid

from kivy import platform
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField


class CardItem(MDGridLayout):
    label_text = StringProperty(None)


class ShareCard(MDGridLayout):
    item_name = StringProperty(None)
    code = StringProperty(None)

    def show_entity_areas(self, touch, code):
        if not self.collide_point(*touch.pos):
            return
        share_code_screen = self.parent.parent.parent.parent.parent.parent
        areas_container = share_code_screen.ids.share_card2_container
        entities = share_code_screen.entities
        #
        selected_entity = None
        for entity in entities:
            if entity.get('code') == code:
                selected_entity = entity
                break
        if not selected_entity:
            return
        entity_name = selected_entity.get('entity_name')
        share_code_screen.selected_entity = entity_name
        share_code_screen.ids.areas_label.text = "Areas of {}".format(entity_name)
        #
        areas = selected_entity.get('areas')
        areas_container.clear_widgets()
        areas_container.bind(minimum_width=areas_container.setter('width'))
        for area in areas:
            area_name = area.get('endpoint')
            area_code = area.get('code')
            share_item = ShareCard(item_name=area_name, code=area_code)
            areas_container.add_widget(share_item)


class CircularButton(Label):
    active = ObjectProperty(False)


class CommonTextField(MDTextField):
    pass


class NumericField(MDTextField):
    pat = re.compile('[^0-9]')
    limit = 13

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        if len(self.text) < self.limit:
            return super(NumericField, self).insert_text(s, from_undo=from_undo)
        return


class ReplicableTextField(CommonTextField):
    """
    Textfield Class that can copy its text to another TextField while typing with a filter
    """
    pat = re.compile('[^0-9A-Za-z& ]')
    pat2 = re.compile('[^0-9A-Za-z ]')
    limit = 25
    copy_to = ObjectProperty(None)

    def on_text(self, instance, text):
        text = re.sub(self.pat2, '', text)
        new_value = ""
        for i, t in enumerate(text, start=0):
            t = t.lower()
            if text[i-1] == " " and t == " " and i > 1:
                t = ""
            if t == " ":
                t = "-"
            new_value = new_value + t
        self.copy_to.text = new_value

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        if len(self.text) < self.limit:
            if self.text == '' and s == ' ':
                return
            if len(self.text) > 2 and self.text[-1] == " " and s == " ":
                return
            return super(ReplicableTextField, self).insert_text(s, from_undo=from_undo)
        return


class OnlyAlphaNumericTextField(CommonTextField):
    pat = re.compile('[^0-9A-Za-z ]')
    limit = 25
    only_lowercase = True

    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        if self.only_lowercase:
            s = s.lower()
        if len(self.text) < self.limit:
            if s == " ":
                s = "-"
            return super(OnlyAlphaNumericTextField, self).insert_text(s, from_undo=from_undo)
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
    # pass
    def on_enter(self, *args):
        Clock.schedule_once(self.set_layout_bind)

    def set_layout_bind(self, dt):
        scroll_layout = self.ids.get("new_entity_scroll_layout")
        if scroll_layout:
            scroll_layout.bind(minimum_height=scroll_layout.setter('height'))


class AddAreaWindow(Screen):
    pass


class AddWhatsappWindow(Screen):
    pass


class ValidateWhatsappWindow(Screen):
    pass


class ShareCodeWindow(Screen):
    entities = [{'entity_name': '@cyberlink', 'code': 'enti1',
                 'areas': [{'endpoint': '#ventas', 'code': 'yt43h'},
                           {'endpoint': '#servicio', 'code': 'g56h'},
                           {'endpoint': '#servicio3', 'code': '1333'}]
                 }, {'entity_name': '@cyberlink2', 'code': 'enti2',
                     'areas': [{'endpoint': '#ventas2', 'code': 'yt43h'},
                               {'endpoint': '#servicio2', 'code': 'g56h'},
                               {'endpoint': '#servicio3', 'code': '2333'}]
                     }]
    selected_entity = ''

    def on_enter(self, *args):
        entities_container = self.ids.share_card1_container
        areas_container = self.ids.share_card2_container
        entities_container.bind(minimum_width=entities_container.setter('width'))
        areas_container.bind(minimum_width=areas_container.setter('width'))
        #
        entities = self.entities
        if not len(entities):
            return
        first_entity = self.entities[0]
        entity_name = first_entity.get('entity_name')
        self.ids.areas_label.text = "Areas of {}".format(entity_name)
        #
        areas = first_entity.get('areas')
        for area in areas:
            area_name = area.get('endpoint')
            area_code = area.get('code')
            share_item = ShareCard(item_name=area_name, code=area_code)
            areas_container.add_widget(share_item)
        #
        for entity in entities:
            entity_name = entity.get('entity_name')
            self.ids.areas_label.text = "Areas of {}".format(entity_name)
            entity_code = entity.get('code')
            share_item = ShareCard(item_name=entity_name, code=entity_code)
            entities_container.add_widget(share_item)


def show_dialog(msg="Please fill all the required fields"):
    dialog = MDDialog(
        text=msg,
        buttons=[
            MDFlatButton(
                text="OK", on_release=lambda x: dialog.dismiss()
            ),
        ],
    )

    dialog.open()


# Loading all the kv files
Builder.load_file('screens/styles.kv')
Builder.load_file('screens/components.kv')
Builder.load_file('screens/new_entity.kv')
Builder.load_file('screens/add_area.kv')
Builder.load_file('screens/add_whatsapp.kv')
Builder.load_file('screens/validate_whatsapp.kv')
Builder.load_file('screens/share_code.kv')


class MainApp(MDApp):
    entity = {}
    areas = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=True,
        )

    def build(self):
        self.title = 'GuazuApp'
        Window.size = (360, 640)  # more common dimensions for mobiles, delete this for building
        screen = Builder.load_file('content.kv')
        # screen.current = "add_area"
        return screen

    def set_entity(self):
        entity_name = self.root.screens[0].ids.entity_name.text
        id_name = self.root.screens[0].ids.id_name.text
        if entity_name and id_name:
            self.entity['entity_name'] = entity_name
            self.entity['id_name'] = id_name
            self.root.current = "add_area"
            return
        show_dialog()

    def set_areas(self):
        add_area_screen = self.root.screens[1]
        area_name = add_area_screen.ids.area_name.text
        area_container_layout = add_area_screen.ids.area_container_layout
        area_container = add_area_screen.ids.area_container
        card_cointainer = add_area_screen.ids.card_area_cointainer
        card_cointainer.bind(minimum_width=card_cointainer.setter('width'))

        if area_name:
            self.areas.append(area_name)
            add_area_screen.ids.area_name.text = ''
            area_container_layout.size_hint = [1, .2]
            area_container.size_hint_y = .9
            area_item = CardItem(label_text=area_name)
            area_item.id = uuid.uuid1()
            card_cointainer.add_widget(area_item)
            return
        show_dialog(msg='Please insert a name')

    def edit_area(self, area_id):
        print('Edited area was #'+str(area_id))

    def delete_area(self, area_id):
        add_area_screen = self.root.screens[1]
        area_container = add_area_screen.ids.area_container
        card_cointainer = add_area_screen.ids.card_area_cointainer
        area_name = None
        #
        for child in card_cointainer.children:
            if child.id == area_id:
                area_name = child.label_text
                card_cointainer.remove_widget(child)
        if area_name:
            self.areas.remove(area_name)
        if len(self.areas) < 1:
            area_container.size_hint = [0, .2]

    def validate_areas(self):
        areas = self.areas
        if len(areas) < 1:
            show_dialog(msg='Please add at least one Area')
            return
        self.root.current = "add_whatsapp"

    def validate_phone(self):
        add_whatsapp_screen = self.root.screens[2]
        country_code = add_whatsapp_screen.ids.country_code.text
        whatsapp_number = add_whatsapp_screen.ids.whatsapp_number.text
        if country_code and whatsapp_number:
            self.root.current = "validate_whatsapp"
            return
        show_dialog()

    def show_more_options(self):
        new_entity_screen = self.root.screens[0]
        more_options_button = new_entity_screen.ids.more_options_button
        #
        more_options_container = new_entity_screen.ids.more_options_container
        publish_button = new_entity_screen.ids.publish_button
        create_group_button = new_entity_screen.ids.create_group_button
        add_areas_button = new_entity_screen.ids.add_areas_button
        #
        create_entity_button = new_entity_screen.ids.create_entity_button
        # new_entity_float_layout = new_entity_screen.ids.new_entity_float_layout
        #
        more_options_container.size_hint_y = 1
        more_options_container.opacity = 1
        more_options_button.size_hint_y = 0
        more_options_button.text = ""
        publish_button.disabled = False
        create_group_button.disabled = False
        add_areas_button.disabled = False
        # new_entity_float_layout.height += 400
        create_entity_button.pos_hint = {'center_x': 0.5, 'center_y': .23}

    # #### FileManager #### #
    def upload_image(self, touch, image):
        """
        Be careful! To use the / path on Android devices, you need special permissions.
        Therefore, you are likely to get an error.
        """
        if not image.collide_point(*touch.pos):
            return
        path = ""
        operative_system = platform
        if operative_system == "win":
            path = 'C:/Users/PC/Downloads/'
        if operative_system == "linux":
            path = '/'
        if operative_system == "android":
            path = '/'
        self.file_manager.show(path)  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        """It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        """
        new_entity_screen = self.root.screens[0]
        image_thumbnail = new_entity_screen.ids.image_thumbnail
        image_thumbnail.source = path
        self.exit_manager()
        self.manager_open = False
        toast(path)

    def exit_manager(self, *args):
        """Called when the user reaches the root of the directory tree."""

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        """Called when buttons are pressed on the mobile device."""

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    def close_app(self):
        self.get_running_app().stop()


MainApp().run()
