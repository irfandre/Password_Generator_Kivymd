from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen


class IntroScreen(MDScreen):
    # def __init__(self,**kwargs):
    #     super( ).__init__(**kwargs)
    def __init__(self,**kw):
        super(IntroScreen, self).__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_enter(self, *args):
        print(self.ids.bu)
        self.ids.bu.size_hint = 0.7, None

    def goto_gen(self):
        print("hello")
        print(self.app.sm)
        self.app.sm.current = 'generator_screen'
