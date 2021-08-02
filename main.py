from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivy.lang import Builder

from kivymd.theming import ThemeManager
from baseclass.generatorscreen import GeneratorScreen
from kivy.core.window import Window
from settings_json import setting_json

class GeneratorApp(MDApp):

    def __init__(self, **kwargs):
        super(GeneratorApp, self).__init__(**kwargs)
        self.rootscreen = Builder.load_file("main.kv")
        Window.bind(on_keyboard=self.onBackButton)
        self.title = "Password Generator"

        self.theme_cls.primary_palette = "DeepPurple"
        self.theme_cls.primary_hue = "500"

        self.theme_cls.accent_palette = "DeepOrange"
        self.theme_cls.accent_hue = "500"

        self.theme_cls.theme_style = "Light"


    def onBackButton(self, window, key, *args):
        print("Keyboard button pressed", )
        if key == 27:
            return self.close_settings()

    def build(self):
        self.theme_cls = ThemeManager()

        self.theme_cls.primary_palette = "DeepPurple"
        self.use_kivy_settings = False
        # self.config.get('Example','bool')
        return self.rootscreen


    def build_settings(self, settings):
        settings.add_json_panel('Settings', self.config, data=setting_json)
        # settings.add_json_panel('two', self.config, data=setting_json2)

    def build_config(self, config):
        config.setdefaults('Example', {
            'bool': True
        })
        config.setdefaults('Example2', {
            'bool': True
        })

    def on_config_change(self, config, section, key, value):
        print(config, section, key, value)


if __name__ == '__main__':
    GeneratorApp().run()
