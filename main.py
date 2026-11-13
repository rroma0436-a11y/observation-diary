from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.metrics import dp
from kivy.utils import platform
import os
import datetime

# Безпечне підключення модуля розпізнавання мови (Speech-to-Text)
try:
    from plyer import stt
except ImportError:
    stt = None


# --- ЕКРАН 1: Авторизація та Вибір Ролі ---
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(15))
        
        layout.add_widget(Label(text='📋 Щоденник спостережень', font_size='22sp', bold=True, size_hint_y=None, height=dp(50)))
        layout.add_widget(Label(text='Авторизація користувача', font_size='16sp', color=(0.7, 0.7, 0.7, 1), size_hint_y=None, height=dp(30)))

        self.user_input = TextInput(hint_text='ПІБ або Логін', multiline=False, size_hint_y=None, height=dp(45))
        layout.add_widget(self.user_input)

        self.role_spinner = Spinner(
            text='Вихователь',
            values=('Директор садка', 'Вихователь', 'Асистент вихователя', 'Помічник вихователя'),
            size_hint_y=None, height=dp(45)
        )
        layout.add_widget(self.role_spinner)

        login_btn = Button(text='Увійти в систему', size_hint_y=None, height=dp(50), background_color=(0.2, 0.6, 0.8, 1))
        login_btn.bind(on_press=self.do_login)
        layout.add_widget(login_btn)

        self.add_widget(layout)

    def do_login(self, instance):
        role = self.role_spinner.text
        if role == 'Директор садка':
            self.manager.current = 'dashboard'
        else:
            self.manager.current = 'onboarding'


# --- ЕКРАН 2: Покроковий майстер (Onboarding) ---
class OnboardingScreen(Screen):
    def __init__(self, **kwargs):
        super(OnboardingScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))

        layout.add_widget(Label(text='⚙️ Налаштування групи та профілю', font_size='18sp', bold=True, size_hint_y=None, height=dp(40)))

        layout.add_widget(Label(text='Введіть номер та специфікацію групи:', size_hint_y=None, height=dp(30)))
        self.group_input = TextInput(hint_text='Наприклад: Молодша група "Сонечко"', multiline=False, size_hint_y=None, height=dp(45))
        layout.add_widget(self.group_input)

        layout.add_widget(Label(text='Список вихованців:', size_hint_y=None, height=dp(30)))
        self.kids_input = TextInput(hint_text='Іванко, Марійка, Оленка...', multiline=True, size_hint_y=0.4)
        layout.add_widget(self.kids_input)

        finish_btn = Button(text='Зберегти та перейти до роботи', size_hint_y=None, height=dp(50), background_color=(0.3, 0.7, 0.3, 1))
        finish_btn.bind(on_press=self.finish_onboarding)
        layout.add_widget(finish_btn)

        self.add_widget(layout)

    def finish_onboarding(self, instance):
        self.manager.current = 'dashboard'


# --- ЕКРАН 3: Головна робоча панель педагога (з голосовим введенням) ---
class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super(DashboardScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Верхня панель
        header = BoxLayout(size_hint_y=None, height=dp(50), padding=dp(10))
        header.add_widget(Label(text='📋 Щоденник спостережень (Робочий кабінет)', bold=True))
        layout.add_widget(header)

        tabs = TabbedPanel(do_default_tab=False)

        # 1. Вкладка: Записи та Голос
        tab_record = TabbedPanelItem(text='✍️ Запис')
        rec_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        self.note_input = TextInput(
            hint_text='Введіть нотатку або скористайтеся мікрофоном...',
            multiline=True,
            size_hint_y=0.5
        )
        rec_layout.add_widget(self.note_input)

        # Кнопка голосового введення
        voice_btn = Button(
            text='🎙️ Надиктувати голосом (UA)',
            size_hint_y=None,
            height=dp(45),
            background_color=(0.8, 0.5, 0.2, 1)
        )
        voice_btn.bind(on_press=self.start_voice_input)
        rec_layout.add_widget(voice_btn)

        save_btn = Button(
            text='💾 Зберегти у щоденний файл',
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.6, 0.8, 1)
        )
        save_btn.bind(on_press=self.save_note)
        rec_layout.add_widget(save_btn)

        tab_record.add_widget(rec_layout)
        tabs.add_widget(tab_record)

        # 2. Вкладка: Швидкі Чек-листи
        tab_checks = TabbedPanelItem(text='📊 Чек-листи')
        check_layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        check_layout.add_widget(Label(text='Швидкі критерії розвитку:', bold=True, size_hint_y=None, height=dp(30)))
        
        self.chk_speech = CheckBox(size_hint_x=None, width=dp(40))
        r1 = BoxLayout(size_hint_y=None, height=dp(40))
        r1.add_widget(self.chk_speech)
        r1.add_widget(Label(text='Мовлення та комунікація'))
        check_layout.add_widget(r1)

        self.chk_motor = CheckBox(size_hint_x=None, width=dp(40))
        r2 = BoxLayout(size_hint_y=None, height=dp(40))
        r2.add_widget(self.chk_motor)
        r2.add_widget(Label(text='Дрібна моторика та творчість'))
        check_layout.add_widget(r2)

        save_chk_btn = Button(text='Зберегти чек-лист дня', size_hint_y=None, height=dp(45), background_color=(0.3, 0.7, 0.3, 1))
        save_chk_btn.bind(on_press=self.save_checklist)
        check_layout.add_widget(save_chk_btn)

        tab_checks.add_widget(check_layout)
        tabs.add_widget(tab_checks)

        # 3. Вкладка: Архів
        tab_archive = TabbedPanelItem(text='📂 Архів')
        arch_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        self.archive_view = Label(text='Архів записів порожній.', valign='top', halign='left')
        self.archive_view.bind(size=lambda s, w: setattr(s, 'text_size', w))
        arch_layout.add_widget(self.archive_view)

        refresh_btn = Button(text='Оновити архів', size_hint_y=None, height=dp(45))
        refresh_btn.bind(on_press=self.load_archive)
        arch_layout.add_widget(refresh_btn)
        
        tab_archive.add_widget(arch_layout)
        tabs.add_widget(tab_archive)

        layout.add_widget(tabs)
        self.add_widget(layout)

    def start_voice_input(self, instance):
        if platform == 'android':
            if stt:
                try:
                    stt.start(language='uk-UA', callback=self.on_speech_result)
                    self.note_input.hint_text = "Слухаю вас... Говоріть..."
                except Exception as e:
                    self.note_input.hint_text = f"Помилка мікрофона: {e}"
            else:
                self.note_input.hint_text = "Модуль stt не завантажено у збірці."
        else:
            # Симуляція для перевірки на ПК
            current = self.note_input.text
            self.note_input.text = (current + " [Тестовий голосовий надиктовувач українською]").strip()

    def on_speech_result(self, text):
        if text:
            current_text = self.note_input.text
            self.note_input.text = (current_text + " " + text).strip()
        self.note_input.hint_text = "Введіть нотатку або скористайтеся мікрофоном..."

    def save_note(self, instance):
        text = self.note_input.text.strip()
        if text:
            today_str = datetime.date.today().strftime('%Y-%m-%d')
            filename = f"schodennik_{today_str}.txt"
            try:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.datetime.now().strftime('%H:%M')}] {text}\n---\n")
                self.note_input.text = ""
                self.archive_view.text = "✅ Запис успішно збережено у щоденний файл!"
            except Exception as e:
                self.archive_view.text = f"Помилка: {e}"

    def save_checklist(self, instance):
        status = f"Мовлення: {'Виконано' if self.chk_speech.active else 'Ні'}, Моторика: {'Виконано' if self.chk_motor.active else 'Ні'}"
        today_str = datetime.date.today().strftime('%Y-%m-%d')
        filename = f"schodennik_{today_str}.txt"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(f"[ЧЕК-ЛИСТ {datetime.datetime.now().strftime('%H:%M')}] {status}\n---\n")
        self.archive_view.text = "✅ Чек-лист успішно додано до звітів дня!"

    def load_archive(self, instance):
        today_str = datetime.date.today().strftime('%Y-%m-%d')
        filename = f"schodennik_{today_str}.txt"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                self.archive_view.text = f.read()
        else:
            self.archive_view.text = "Записів за сьогодні ще немає."


# --- ГОЛОВНИЙ КЛАС ДОДАТКУ ---
class ObservationApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(OnboardingScreen(name='onboarding'))
        sm.add_widget(DashboardScreen(name='dashboard'))
        return sm


if __name__ == '__main__':
    ObservationApp().run()
