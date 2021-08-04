from kaki.app import App
from kivy import Config
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.factory import Factory
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
        # os.path.join(os.getcwd(), "main.kv"),
        os.path.join(os.getcwd(), "kv/introscreen.kv"),
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
        self.theme_cls.primary_palette = "DeepPurple"
        self.use_kivy_settings = False
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(IntroScreen(name='intro_screen'))
        self.sm.add_widget(GeneratorScreen(name='generator_screen'))
        # return Factory.GeneratorScreen()
        return self.sm
        # return Factory.ScreenUI()

    def on_start(self):
        print(self.sm.current)
        # Clock.schedule_once(self.gen_scren, 1000)
    # def on
    def gen_scren(self):
        self.sm.current = 'generator_screen'

    def _rebuild(self, *args):
        if args[1] == 32:
            self.rebuild()

    def build_settings(self, settings):
        settings.add_json_panel('Settings', self.config, data=setting_json)

    def build_config(self, config):
        config.setdefaults('Example', {
            'bool': True
        })
        config.setdefaults('Example2', {
            'bool': True
        })

    def on_config_change(self, config, section, key, value):
        print(config.get('Example', 'bool'))
        if config.get('Example', 'bool') == '1':
            self.sm.current = 'intro_screen'
            self.close_settings()


LiveApp().run()
