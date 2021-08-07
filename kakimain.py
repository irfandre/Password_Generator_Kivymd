from kaki.app import App
from kivy import Config
from kivy.clock import Clock

from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, WipeTransition, SwapTransition, CardTransition, FadeTransition, \
    FallOutTransition, RiseInTransition, NoTransition
from kivymd.app import MDApp
import os

from baseclass.generatorscreen import GeneratorScreen
from baseclass.introscreen import IntroScreen
from settings_json import setting_json

Config.set('graphics', 'position', 'custom')
Window.size = (300, 700)


class LiveApp(App, MDApp):
    KV_FILES = {
        os.path.join(os.getcwd(), "kv/generatorscreen.kv"),
        os.path.join(os.getcwd(), "kv/introscreen.kv"),
        os.path.join(os.getcwd(), "main.kv"),
    }

    CLASSES = {
        "GeneratorScreen": "baseclass.generatorscreen",
        "IntroScreen": "baseclass.introscreen"
    }

    AUTORELOADER_PATHS = [
        (".", {"recursive": True})
    ]

    def build_app(self, *args):
        Window.bind(on_keyboard=self._rebuild)
        print("from kaki app")
        self.screens_visited_list = []
        self.theme_cls.primary_palette = "DeepPurple"
        self.use_kivy_settings = False
        self.screen = ScreenManager(transition=NoTransition())
        self.screen.add_widget(IntroScreen(name='intro_screen'))
        self.screen.add_widget(GeneratorScreen(name='generator_screen'))
        return Factory.GeneratorScreen()
        # self.screen = Builder.load_file('main.kv')
        # return self.screen
        # return Factory.ScreenUI()

    def on_start(self):
        # print(se.current)
        self.check_visited_screens()
        Clock.schedule_once(self.gen_scren, 1000)

    # def on
    def gen_scren(self):
        self.screen.current = 'generator_screen'

    def _rebuild(self, *args):
        if args[1] == 32:
            self.rebuild()

    '''
        {27: 'escape', 9: 'tab', 8: 'backspace', 13: 'enter', 127: 'del', 271: 'enter', 273: 'up', 274: 'down',
         275: 'right', 276: 'left', 278: 'home', 279: 'end', 280: 'pgup', 281: 'pgdown'}#
        '''

    def on_back_button(self, window, key, *args):
        print("Keyboard button pressed", window, key, args)
        if key == 27:
            # return self.close_settings()
            return self.pop_screen()
        if key == 9:
            print('tab clicked')

    def check_visited_screens(self):
        # print(self.screens_visited_list)
        if self.screen.current not in self.screens_visited_list:
            self.screens_visited_list.append(self.screen.current)
            print(self.screens_visited_list)

    def pop_screen(self):
        if self.screens_visited_list:
            if not self.screen.current == "intro_screen":
                popped_item = self.screens_visited_list.pop()
                # self.screen.current = popped_item
                print("popping", popped_item)
                if len(self.screens_visited_list) == 0:
                    return self.stop()
                self.screen.current = self.screens_visited_list[len(self.screens_visited_list) - 1]
                print(self.screens_visited_list)
                return True
        else:
            self.screen.current = "intro_screen"
            self.screens_visited_list.append(self.screen.current)
            # return True

    def build_settings(self, settings):
        settings.add_json_panel('Settings', self.config, data=setting_json)

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
            self.screen.current = 'intro_screen'
            self.close_settings()
        else:
            self.screen.current = 'intro_screen'
            self.close_settings()

    def toggle_darkmode(self, value):
        if value == '1':
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


LiveApp().run()
