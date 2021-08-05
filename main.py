from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from kivy.lang import Builder

from kivymd.theming import ThemeManager
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from baseclass.generatorscreen import GeneratorScreen
from baseclass.introscreen import IntroScreen
from kivy.core.window import Window
from settings_json import setting_json


class GeneratorApp(MDApp):
    show = 0
    dialog = None

    def __init__(self, **kwargs):
        super(GeneratorApp, self).__init__(**kwargs)
        self.screens_visited_list = []
        self.rootscreen = Builder.load_file("main.kv")
        Window.bind(on_keyboard=self.on_back_button)
        self.title = "Password Generator"

        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "500"

        self.theme_cls.accent_palette = "DeepOrange"
        self.theme_cls.accent_hue = "500"

        self.theme_cls.theme_style = "Light"
        self.setting = 'self.config'
        self.sm = ScreenManager(transition=NoTransition())

    def build(self):
        self.theme_cls = ThemeManager()
        self.sm.add_widget(IntroScreen(name='intro_screen'))
        self.sm.add_widget(GeneratorScreen(name='generator_screen'))
        self.theme_cls.primary_palette = "DeepPurple"
        self.use_kivy_settings = False
        self.show = self.config.get('Example', 'bool')
        print("from build", self.show)
        return self.sm

    def on_start(self):
        print("from start ", self.show)
        self.toggle_intro_screen(self.config.get('Example', 'bool'))
        self.toggle_darkmode(self.config.get('Example', 'darkmode'))
        print(self.sm.__dict__)
        print(self.sm.screen_names)
        self.check_visited_screens()
        print(self.screens_visited_list)
        self.config = self.config

    '''
    {27: 'escape', 9: 'tab', 8: 'backspace', 13: 'enter', 127: 'del', 271: 'enter', 273: 'up', 274: 'down',
     275: 'right', 276: 'left', 278: 'home', 279: 'end', 280: 'pgup', 281: 'pgdown'}#
    '''
    def on_back_button(self, window, key, *args):
        # print("Keyboard button pressed", window.__dict__)
        if key == 27:
            # return self.close_settings()
            return self.pop_screen()
        if key == 9:
            print('tab clicked')

    def check_visited_screens(self):
        # print(self.screens_visited_list)
        if self.sm.current not in self.screens_visited_list:
            self.screens_visited_list.append(self.sm.current)
            print(self.screens_visited_list)

    def on_stop(self):
        pass

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Discard draft?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="DISCARD", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
        self.dialog.open()

    def pop_screen(self):
        if self.screens_visited_list:
            if not self.sm.current == "intro_screen":
                popped_item = self.screens_visited_list.pop()
                # self.sm.current = popped_item
                print("popping",popped_item)
                if len(self.screens_visited_list) == 0:
                    return self.stop()
                self.sm.current = self.screens_visited_list[len(self.screens_visited_list)-1]
                print(self.screens_visited_list)
                return True
        else:
            self.sm.current = "intro_screen"
            self.screens_visited_list.append(self.sm.current)
            # return True

    def build_settings(self, settings):
        settings.add_json_panel('Settings', self.config, data=setting_json)
        # settings.add_json_panel('two', self.config, data=setting_json2)

    def build_config(self, config):
        config.setdefaults('Example', {
            'bool': True,
            'darkmode': False,
            'saveoptions': False
        })
        config.setdefaults('Example2', {
            'bool': True
        })
        config.setdefaults('options', {
            'digits': False,
            'special': False
        })

    def on_config_change(self, config, section, key, value):
        print(config, section, key, value)
        if key == 'darkmode':
            self.toggle_darkmode(value)
        elif key == 'bool':
            self.toggle_intro_screen(value)
        elif key == 'saveoptions':
            pass

    def toggle_intro_screen(self, value):
        if value == '1':
            self.sm.current = 'intro_screen'
            self.close_settings()
        else:
            self.sm.current = 'intro_screen'
            self.close_settings()

    def toggle_darkmode(self, value):
        if value == '1':
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


if __name__ == '__main__':
    GeneratorApp().run()
