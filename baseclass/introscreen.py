from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class IntroScreen(MDScreen):

    def __init__(self, **kw):
        super(IntroScreen, self).__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_kv_post(self, base_widget):
        print("ids ---------", self.ids)
        self.ids.start_button.size_hint = 0.7, None
        # print(self.parent.current)
        # print(self.parent.ids.generator_screen.generate(2,3))

    def on_enter(self, *args):
        print("intro screen entered")
        # COMMENT OUT BELOW LINE DURING DEVELOPMENT/ AND UNCOMMENT WHILE BUILDING
        # self.app.statusbar('#F59C8A')
