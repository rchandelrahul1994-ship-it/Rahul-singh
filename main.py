from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
import webbrowser
import random

# --- APP CONFIGURATION ---
APP_VERSION = "1.2"  # Jab update dena ho, ise "1.3" kar dena
UPDATE_URL = "https://github.com/RAHULSINGH-8787/Rahul-singh-trading/raw/main/bin/trading_app.apk"

Window.clearcolor = (0.05, 0.05, 0.1, 1)

class TradingApp(App):
    def build(self):
        self.title = "Rahul Singh Trading Pro"
        self.store = JsonStore('app_data.json')
        self.my_number = "918787269197"
        
        # Check for Update first
        self.check_for_update()
        
        # Load user data
        if self.store.exists('user_data'):
            data = self.store.get('user_data')
            self.balance = data.get('balance', 0)
        else:
            self.balance = 0; self.save_data()

        self.stocks = {"NIFTY 50": 24500, "BANK NIFTY": 52000, "RELIANCE": 2980, "TATA MOTORS": 985}
        self.main_layout = BoxLayout(orientation='vertical')
        
        # UI Setup
        nav = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=10)
        nav.add_widget(Label(text=f"V{APP_VERSION}", size_hint=(0.2, 1), color=(0.5, 0.5, 0.5, 1)))
        nav.add_widget(Label(text="RAHUL SINGH TRADING PRO", bold=True, color=(1,0.8,0,1)))
        self.main_layout.add_widget(nav)

        self.content = BoxLayout(orientation='vertical', padding=10)
        self.show_market_ui()
        self.main_layout.add_widget(self.content)
        
        return self.main_layout

    # --- FORCE UPDATE SYSTEM ---
    def check_for_update(self):
        # Yahan hum simulate kar rahe hain. 
        # Real app mein ye server se version check karta hai.
        latest_version = "1.2" # Agar aap ise 1.3 kar denge code mein toh sabko update dikhega
        
        if APP_VERSION != latest_version:
            self.show_force_update_popup()

    def show_force_update_popup(self):
        content = BoxLayout(orientation='vertical', spacing=15, padding=20)
        msg = Label(text="[b]Naya Update Available Hai![/b]\n\nPurana version ab kaam nahi karega.\nKripya naya APK download karein.", 
                    markup=True, halign='center')
        
        upd_btn = Button(text="UPDATE NOW", background_color=(0, 1, 0, 1), size_hint=(1, 0.3))
        upd_btn.bind(on_press=self.go_to_update)
        
        content.add_widget(msg)
        content.add_widget(upd_btn)
        
        # auto_dismiss=False se customer ise hata nahi payega
        self.upd_popup = Popup(title="Update Compulsory!", content=content, 
                               size_hint=(0.9, 0.6), auto_dismiss=False)
        self.upd_popup.open()

    def go_to_update(self, instance):
        webbrowser.open(UPDATE_URL)

    # --- MARKET & INDICATORS ---
    def show_market_ui(self):
        self.content.clear_widgets()
        self.content.add_widget(Label(text=f"Balance: ₹{self.balance}", color=(0,1,0,1), size_hint=(1,0.1)))
        for name, price in self.stocks.items():
            btn = Button(text=f"{name} | ₹{price}", size_hint_y=None, height=70)
            btn.bind(on_press=lambda x, n=name, p=price: self.show_technicals(n, p))
            self.content.add_widget(btn)

    def show_technicals(self, name, price):
        rsi = random.randint(20, 80)
        content = BoxLayout(orientation='vertical', padding=15)
        content.add_widget(Label(text=f"Indicator Analysis for {name}", bold=True))
        content.add_widget(Label(text=f"RSI: {rsi}"))
        content.add_widget(Label(text=f"MACD: Bullish"))
        
        btn = Button(text="Close", size_hint=(1, 0.3))
        popup = Popup(title="Technicals", content=content, size_hint=(0.8, 0.5))
        btn.bind(on_press=popup.dismiss)
        content.add_widget(btn)
        popup.open()

    def save_data(self):
        self.store.put('user_data', balance=self.balance)

if __name__ == '__main__':
    TradingApp().run()
