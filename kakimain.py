from kaki.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivymd.app import MDApp
import os

class LiveApp(App, MDApp):
    KV_FILES = {
        os.path.join(os.getcwd(), "kv/generatorscreen.kv")
    }

    CLASSES = {
        "GeneratorScreen": "baseclass.generatorscreen"
    }

    AUTORELOADER_PATHS = [
        (".", {"recursive": True})
    ]

    def build_app(self, *args):
        Window.bind(on_keyboard=self._rebuild)
        print("from kaki app")
        return Factory.GeneratorScreen()

    def _rebuild(self, *args):
        if args[1] == 32:
            self.rebuild()
            


LiveApp().run()
