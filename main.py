
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp
from kivy.lang import Builder

from kivymd.theming import ThemeManager
from baseclass.generatorscreen import GeneratorScreen
from baseclass.introscreen import IntroScreen
from kivy.core.window import Window
from settings_json import setting_json

class GeneratorApp(MDApp):
    show = 0
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
        self.setting = 'self.config'

    def onBackButton(self, window, key, *args):
        print("Keyboard button pressed", )
        if key == 27:
            return self.close_settings()

    def build(self):
        self.theme_cls = ThemeManager()
        self.sm = ScreenManager(transition=NoTransition())
        self.sm.add_widget(IntroScreen(name='intro_screen'))

        self.sm.add_widget(GeneratorScreen(name='generator_screen'))
        self.theme_cls.primary_palette = "DeepPurple"
        # self.use_kivy_settings = False
        self.show = self.config.get('Example', 'bool')
        print("from build",self.show)
        return self.sm

    def on_start(self):
        print("from start " , self.show)
        self.toggle_screen(self.config.get('Example', 'bool'))
        self.toggle_darkmode(self.config.get('Example', 'darkmode'))

    def set_special(self, config):
        if config.get('Example', 'bool'):
            print('1')

    def check(self):
        # Config = ConfigParser(name='kivy')
        print("from check", "Config")

    def build_settings(self, settings):
        settings.add_json_panel('Settings', self.config, data=setting_json)
        # settings.add_json_panel('two', self.config, data=setting_json2)

    def build_config(self, config):
        config.setdefaults('Example', {
            'bool': True,
            'darkmode': False
        })
        config.setdefaults('Example2', {
            'bool': True
        })

    def on_config_change(self, config, section, key, value):
        print(config, section, key, value)
        # if config.get('Example', 'bool') == '1':
        #     self.sm.current = 'intro_screen'
        #     self.close_settings()
        if key == 'darkmode':
            self.toggle_darkmode(value)

        elif key == 'bool':
            self.toggle_screen(value)

    def config_checker(self, config):
        pass

    def toggle_screen(self, value):
        if value == '1':
            self.sm.current = 'intro_screen'
            self.close_settings()
        else:
            pass
    def toggle_darkmode(self, value):
        if value == '1':
            self.theme_cls.theme_style = "Dark"
        else:
            self.theme_cls.theme_style = "Light"


if __name__ == '__main__':
    GeneratorApp().run()
