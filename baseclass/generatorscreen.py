from kivymd.app import MDApp
import random
import string
import re
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen


class GeneratorScreen(MDScreen):
    def __init__(self, **kw):
        super(GeneratorScreen, self).__init__(**kw)
        # Clock.schedule_once(self.after_init)
        self.app = MDApp.get_running_app()

    def on_kv_post(self, base_widget):
        self.generate(2, 3)

    def on_pre_enter(self, *args):
        self.ids.regen_button.size_hint = .7, None
        self.ids.copy_button.size_hint = .7, None

    def on_enter(self, *args):
        self.configuration_check()
        self.app.check_visited_screens()

        # try:
        #     read_config.read("generator.ini")
        #     name = read_config.get("Example", "bool")
        # except configparser.NoOptionError:
        #     pass
        # except configparser.NoSectionError:
        #     pass

    def configuration_check(self):
        if self.app.config.get("Example", "saveoptions") == '1':
            if self.app.config.get("options", "digits") == '1':
                self.ids.digits_switch.active = True
            elif self.app.config.get("options", "digits") == '0':
                self.ids.digits_switch.active = False

            if self.app.config.get("options", "special") == '1':
                self.ids.special_switch.active = True
            elif self.app.config.get("options", "special") == '0':
                self.ids.special_switch.active = False
        else:
            self.ids.digits_switch.active = False
            self.ids.special_switch.active = False


    def set_digits_config(self):
        if self.ids.digits_switch.active:
            self.app.config.set("options", 'digits', '1')
            self.app.config.write()
        else:
            self.app.config.set("options", 'digits', '0')
            self.app.config.write()

    def set_special_config(self):
        if self.ids.digits_switch.active:
            self.app.config.set("options", 'special', '1')
            self.app.config.write()
        else:
            self.app.config.set("options", 'special', '0')
            self.app.config.write()

    def value_check(self):
        slider = self.ids.input_value
        if slider.value < 8:
            slider.value = 8
        self.generate()

    def generate(self, *args):
        # def generate(self, letters_count, digits_count, special_count):
        sp_char = '@!~$%^&*()_+#{}?/<>'
        # letters_count = args[0]

        if not args:
            # default arguments for digit and special
            args = (2, 3)
        my_list = list(args)
        if int(self.ids.input_value.value) > 52:
            digit_divide = int(int(self.ids.input_value.value) / 3)
            special_divide = int(int(self.ids.input_value.value) / 6)
            my_list[0] = 23 if digit_divide > 23 else digit_divide

            my_list[1] = 18 if special_divide > 18 else special_divide
        elif int(self.ids.input_value.value) > 12:
            digit_divide = int(int(self.ids.input_value.value) / 3)
            special_divide = int(int(self.ids.input_value.value) / 5)
            my_list[0] = 23 if digit_divide > 23 else digit_divide

            my_list[1] = 18 if special_divide > 18 else special_divide
        else:
            my_list[0] = 3
            my_list[1] = 4
        args = tuple(my_list)
        # print(my_list[0])
        letters_count = self.total(args)
        digits_count = my_list[0]
        special_count = my_list[1]
        # letters = ''.join((random.sample(string.ascii_letters, letters_count)))
        letters = ''.join((random.choice(string.ascii_letters) for i in range(letters_count)))
        digits = ''.join((random.choice(string.digits) for i in range(digits_count)))
        special = ''.join((random.choice(sp_char) for i in range(special_count)))
        # Convert resultant string to list and shuffle it to mix letters and digits
        sample_list = list(letters + digits
                           if (self.ids.digits_switch.active and not self.ids.special_switch.active)
                           else letters + special if (
                                self.ids.special_switch.active and not self.ids.digits_switch.active)
                           else letters + digits + special if (
                                self.ids.digits_switch.active and self.ids.special_switch.active) else letters)

        random.shuffle(sample_list)
        # convert list to string
        final_string = ''.join(sample_list)
        colored_string = ''
        for i in final_string:
            if i.isnumeric():
                colored_string += '[color=0073e5]' + i + '[/color]'
            elif i.isalpha():
                colored_string += i
            else:
                colored_string += '[color=bc4b4b]' + i + '[/color]'

        print('Random string with', letters_count, 'letters', 'and', digits_count, 'digits and', special_count,
              ' special characters is: \n', final_string, "and total password length is: -- ",
              int(self.ids.input_value.value))
        self.ids.result.text = colored_string
        return self.ids.result.text

    def clean_text(self):
        text_after = re.sub(r'\[(.*?)\]', '', self.ids.result.text)
        Clipboard.copy(text_after)
        toast('Password Copied')

    def total(self, args):
        if self.ids.digits_switch.active and not self.ids.special_switch.active:
            return int(self.ids.input_value.value) - args[0]
        elif self.ids.special_switch.active and not self.ids.digits_switch.active:
            return int(self.ids.input_value.value) - args[1]
        elif self.ids.digits_switch.active and self.ids.special_switch.active:
            return int(self.ids.input_value.value) - args[0] - args[1]
        else:
            return int(self.ids.input_value.value)
