import paramiko
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

class MyApp(App):

    title = 'PiarService'

    def build(self):

        self.layout = BoxLayout(orientation='vertical')

        self.scroll_view = ScrollView(size_hint=(1, None), size=(400, 200))
        self.text_input = TextInput(hint_text='Введите логин', size_hint=(1, None), height=50)
        self.scroll_view.add_widget(self.text_input)
        self.layout.add_widget(self.scroll_view)

        self.info_text = TextInput(readonly=True, size_hint=(1, 1), multiline=True, background_color=(0.8, 0.8, 0.8, 1))
        self.layout.add_widget(self.info_text)

        self.button = Button(text='Авторизоваться', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5})
        self.button.bind(on_press=self.check_login)
        self.layout.add_widget(self.button)

        return self.layout

    def on_button_click(self, instance):
        self.layout.remove_widget(self.scroll_view)
        self.layout.remove_widget(self.button)

        new_button1 = Button(text='Мои боты', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5})
        new_button1.bind(on_press=self.show_bots)
        self.layout.add_widget(new_button1)

        new_button2 = Button(text='Логи', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5})
        new_button1.bind(on_press=self.show_logs)
        self.layout.add_widget(new_button2)

    def check_login(self, instance):
        username = self.text_input.text.strip()

        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect('185.63.191.71', username='root', password='230906Jg')

            command = f'sqlite3 /root/bot_database.db "SELECT * FROM accounts WHERE key=\'{username}\';"'
            stdin, stdout, stderr = ssh_client.exec_command(command)

            for line in stderr:
                print(line.strip())

            output = stdout.read().decode().strip()
            if output:
                self.on_button_click(instance)
                self.info_text.text = "Заебись, подключились!\n"
            else:
                self.info_text.text += "Хуёва: Пользователь не найден\n"

            ssh_client.close()
        except Exception as e:
            self.info_text.text += f"Ошибка: {str(e)}\n"

    def show_logs(self, instance):
        self.info_text.text = "Хуёва: я тут ещё нихуя не сделал...\n"

    def show_bots(self, instance):
        username = self.text_input.text.strip()
        self.layout.remove_widget(instance)
        self.layout.remove_widget(self.layout.children[-2])

        sel1 = Button(text='1', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5})
        self.layout.add_widget(sel1)

        sel2 = Button(text='2', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5})
        self.layout.add_widget(sel2)

        sel3 = Button(text='3', size_hint=(None, None), size=(150, 50), pos_hint={'center_x': 0.5})
        self.layout.add_widget(sel3)

        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect('185.63.191.71', username='root', password='230906Jg')

            command = f'sqlite3 /root/bot_database.db "SELECT * FROM accounts WHERE key=\'{username}\';"'
            stdin, stdout, stderr = ssh_client.exec_command(command)

            for line in stderr:
                print(line.strip())

            output = stdout.read().decode().strip()
            if output:
                self.info_text.text = f"Список твоих работяг:\n"
                bots_info = output.split("|")[2:5]
                for bot_info in bots_info:
                    self.info_text.text += f"Bot: {bot_info}\n"
            else:
                self.info_text.text += "Хуёва: Не удалось получить информацию о ботах\n"

            ssh_client.close()
        except Exception as e:
            self.info_text.text += f"Ошибка: {str(e)}\n"

if __name__ == '__main__':
    MyApp().run()
