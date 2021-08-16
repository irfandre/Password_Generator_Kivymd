from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from baseclass.generatorscreen import GeneratorScreen
from baseclass.introscreen import IntroScreen
from kivy.core.window import Window
from settings_json import setting_json
from kivy.utils import platform, get_color_from_hex
from kivy.uix.settings import SettingsWithNoMenu


class ScreenManager(ScreenManager):
    pass


# if platform in ('linux', 'linux2', 'macos', 'win'):
if platform != 'android':
    Window.size = (350, 760)

try:
    from android.runnable import run_on_ui_thread
    from jnius import autoclass

    Color = autoclass("android.graphics.Color")
    WindowManager = autoclass('android.view.WindowManager$LayoutParams')
    activity = autoclass('org.kivy.android.PythonActivity').mActivity
except ModuleNotFoundError:
    pass
except NotImplementedError:
    pass


class GeneratorApp(MDApp):
    show = 0
    dialog = None
    label = get_color_from_hex('2F3259')

    def __init__(self, **kwargs):
        super(GeneratorApp, self).__init__(**kwargs)
        self.screens_visited_list = []
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "A100"
        self.screen = Builder.load_file("main.kv")
        self.title = "Password Generator"
        Window.bind(on_keyboard=self.on_back_button)
        Window.bind(on_request_close=self.show_alert_dialog)

    try:
        @run_on_ui_thread
        def statusbar(self, color):
            window = activity.getWindow()
            window.clearFlags(WindowManager.FLAG_TRANSLUCENT_STATUS)
            window.addFlags(WindowManager.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS)
            window.setStatusBarColor(Color.parseColor(color))
            self.navigation_bar_color(window)
    except NameError:
        pass
    except Exception as e:
        print(e)

    def navigation_bar_color(self, window):
        if self.theme_cls.theme_style == 'Light':
            window.setNavigationBarColor(Color.parseColor('#fafafa'))
        else:
            window.setNavigationBarColor(Color.parseColor('#121212'))

    def build(self):
        self.use_kivy_settings = False
        self.settings_cls = SettingsWithNoMenu
        self.platform_check_for_statusbar('#F59C8A')
        self.show = self.config.get('Example', 'bool')
        return self.screen

    def platform_check_for_statusbar(self, color):
        if platform == 'android':
            self.statusbar(color)

    def on_start(self):
        print("from start ", self.show)
        self.toggle_intro_screen(self.config.get('Example', 'bool'))
        self.toggle_darkmode(self.config.get('Example', 'darkmode'))
        self.check_visited_screens()
        print(self.screens_visited_list)
        print("root", self.screen.ids.intro_screen.ids)
        print("root", self.screen.ids)

    '''
    {27: 'escape', 9: 'tab', 8: 'backspace', 13: 'enter', 127: 'del', 271: 'enter', 273: 'up', 274: 'down',
     275: 'right', 276: 'left', 278: 'home', 279: 'end', 280: 'pgup', 281: 'pgdown'}#
    '''

    def on_back_button(self, window, key, *args):
        print("Keyboard button pressed", key)
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
        elif key == 'saveoptions' and value == '1':
            self.set_digits_config()
            self.set_special_config()
        elif key == 'saveoptions' and value == '0':
            config.set("options", 'digits', '0')
            config.set("options", 'special', '0')
            config.write()

    def set_digits_config(self):
        if self.screen.ids.generator_screen.ids.digits_switch.active:
            self.config.set("options", 'digits', '1')
            self.config.write()
        else:
            self.config.set("options", 'digits', '0')
            self.config.write()

    def set_special_config(self):
        if self.screen.ids.generator_screen.ids.special_switch.active:
            self.config.set("options", 'special', '1')
            self.config.write()
        else:
            self.config.set("options", 'special', '0')
            self.config.write()

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
        self.platform_check_for_statusbar(self.check_screen())

    def check_screen(self):
        if self.screen.current == 'intro_screen':
            return '#F59C8A'
        else:
            return '#e67a70'

    def show_alert_dialog(self, *largs, **kwargs):
        if not self.dialog:
            exit_button = MDFlatButton(
                text="Exit", text_color=self.theme_cls.primary_color
            )
            cancel_button = MDFlatButton(
                text="Cancel", text_color=self.theme_cls.primary_color
            )
            exit_button.bind(on_release=self.stop)
            cancel_button.bind(on_release=self.dialog_close)
            self.dialog = MDDialog(
                title="Exit",
                text="Are you sure you want to exit?",
                buttons=[
                    cancel_button,
                    exit_button,
                ],
            )
        self.dialog.open()
        return True

    def dialog_close(self, *args):
        print('closing dialog')
        self.dialog.dismiss(force=True)


if __name__ == '__main__':
    GeneratorApp().run()
