from kivymd.app import MDApp
import random
import string
import re
from kivy.core.clipboard import Clipboard
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen
from kivymd.uix.selectioncontrol import MDSwitch


class GeneratorScreen(MDScreen):
    def __init__(self, **kw):
        super(GeneratorScreen, self).__init__(**kw)
        # Clock.schedule_once(self.after_init)
        self.app = MDApp.get_running_app()

    def on_kv_post(self, base_widget):
        self.generate()

    def on_pre_enter(self, *args):
        self.ids.regen_button.size_hint = .9, None
        self.ids.copy_button.size_hint = .9, None

    def on_enter(self, *args):
        self.configuration_check()
        self.app.check_visited_screens()
        self.app.platform_check_for_statusbar('#e67a70')

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

            if self.app.config.get("options", "uppercase") == '1':
                self.ids.upper_switch.active = True
            elif self.app.config.get("options", "uppercase") == '0':
                self.ids.upper_switch.active = False
        else:
            # self.ids.digits_switch.active = False
            # self.ids.special_switch.active = False
            self.app.config.set("options", 'digits', '0')
            self.app.config.set("options", 'special', '0')
            self.app.config.write()

    def value_check(self):
        slider = self.ids.input_value
        if slider.value < 8:
            slider.value = 8
        self.generate()

    def get_password(self, key, digits, special, uppercase, lowercase):
        switcher = {
            1: lowercase + uppercase,
            2: lowercase + digits,
            3: lowercase + uppercase + digits,
            10: lowercase + special,
            12: lowercase + digits + special,
            11: lowercase + uppercase + special,
            13: lowercase + uppercase + digits + special,
        }
        return switcher.get(key, lowercase)

    def get_switch_key(self, dig, sp, upper):
        if dig:
            digit = 2
        else:
            digit = 0
        if sp:
            sp = 10
        else:
            sp = 0
        if upper:
            upper = 1
        else:
            upper = 0
        print(digit + upper + sp)
        return digit + sp + upper

    def generate(self, *args):
        # def generate(self, uppercase_count, digits_count, special_count):
        sp_char = '@!~$%^&*()_+#{}?/<>'
        digits_active_status = self.ids.digits_switch.active
        special_active_status = self.ids.special_switch.active
        upper_active_status = self.ids.upper_switch.active
        switch_key = self.get_switch_key(
            digits_active_status,
            special_active_status,
            upper_active_status
        )

        if not args:
            # default arguments for digit and special
            args = (2, 2, 2)
        my_list = list(args)
        if int(self.ids.input_value.value) > 52:
            digit_divide = int(int(self.ids.input_value.value) / 3)
            special_divide = int(int(self.ids.input_value.value) / 6)
            upper_divide = int(int(self.ids.input_value.value) / 4)

            my_list[0] = 23 if digit_divide > 23 else digit_divide
            my_list[1] = 18 if special_divide > 18 else special_divide
            my_list[2] = 20 if upper_divide > 20 else upper_divide

        elif int(self.ids.input_value.value) > 12:
            digit_divide = int(int(self.ids.input_value.value) / 3)
            special_divide = int(int(self.ids.input_value.value) / 5)
            upper_divide = int(int(self.ids.input_value.value) / 4)

            my_list[0] = 23 if digit_divide > 23 else digit_divide
            my_list[1] = 18 if special_divide > 18 else special_divide
            my_list[2] = 20 if upper_divide > 20 else upper_divide
        else:
            my_list[0] = 2
            my_list[1] = 2
            my_list[2] = 2
        lowercase_count = self.lowercase_total_count(tuple(my_list))
        digits_count = my_list[0]
        special_count = my_list[1]
        uppercase_count = my_list[2]
        lowercase = ''.join((random.choice(string.ascii_lowercase) for i in range(lowercase_count)))
        digits = ''.join((random.choice(string.digits) for i in range(digits_count)))
        special = ''.join((random.choice(sp_char) for i in range(special_count)))
        uppercase = ''.join((random.choice(string.ascii_uppercase) for i in range(uppercase_count)))

        # Convert resultant string to list and shuffle it to mix uppercase and digits
        # self.get_password(switch_key, digits, special, uppercase, lowercase)

        # sample_list = list(uppercase + digits
        #                    if (self.ids.digits_switch.active and not self.ids.special_switch.active)
        #                    else uppercase + special if (
        #         self.ids.special_switch.active and not self.ids.digits_switch.active)
        # else uppercase + digits + special if (
        #         self.ids.digits_switch.active and self.ids.special_switch.active) else uppercase)
        # print("skjsld-----------",self.get_password(switch_key, digits, special, uppercase, lowercase))
        sample_list = list(self.get_password(switch_key, digits, special, uppercase, lowercase))
        random.shuffle(sample_list)
        # convert list to string
        final_string = ''.join(sample_list)
        colored_string = ''
        for i in final_string:
            if i.isnumeric():
                colored_string += '[color=0073e5]' + i + '[/color]'
            elif i.islower():
                colored_string += i
            elif i.isupper():
                colored_string += '[color=1a936f]' + i + '[/color]'
            else:
                colored_string += '[color=bc4b4b]' + i + '[/color]'
        print('Random string with', uppercase_count, 'uppercase', 'and',
              digits_count, 'digits and', special_count,
              'special characters,', "total password length is: -- ",
              int(self.ids.input_value.value)
              )
        self.ids.result.text = colored_string
        return self.ids.result.text

    def cleaned_text(self):
        text_after = re.sub(r'\[(.*?)\]', '', self.ids.result.text)
        Clipboard.copy(text_after)
        toast('Password Copied')

    def active_switches(self):
        lst = []
        for child in self.ids.float_layout.children:
            if isinstance(child, MDSwitch):
                # child.disabled = not child.disabled
                if child.active:
                    print(child.name)
                    lst.append(child.name)
        return lst

    def lowercase_total_count(self, args):
        total_characters_count = int(self.ids.input_value.value)
        for switch in self.active_switches():
            if 'digits' in switch:
                total_characters_count -= args[0]
            if 'special' in switch:
                total_characters_count -= args[1]
            if 'upper' in switch:
                total_characters_count -= args[2]
        return total_characters_count
