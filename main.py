from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
import webbrowser
import random

# App Config
APP_VERSION = "1.2"
Window.clearcolor = (0.05, 0.05, 0.1, 1)

class TradingApp(App):
    def build(self):
        self.title = "Rahul Singh Trading Pro"
        self.store = JsonStore('app_data.json')
        self.my_number = "918787269197"
        
        # Load Data
        if self.store.exists('user_data'):
            data = self.store.get('user_data')
            self.balance = data.get('balance', 0)
            self.my_referral_code = data.get('referral_code', f"REF-{random.randint(1000, 9999)}")
        else:
            self.balance = 0; self.my_referral_code = f"REF-{random.randint(1000, 9999)}"; self.save_data()

        # All Stocks and Indices Data
        self.indices = {
            "NIFTY 50": 24500, "BANK NIFTY": 52000, "SENSEX": 80200,
            "MIDCAP NIFTY": 12500, "BANKEX": 58000, "DOW JONES": 39500
        }
        self.stocks = {"RELIANCE": 2980, "TATA MOTORS": 985, "ZOMATO": 265, "HDFC BANK": 1650}

        # --- MAIN HOME PAGE LAYOUT ---
        self.layout = BoxLayout(orientation='vertical', spacing=5)

        # 1. TOP HEADER (Menu + Search)
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.08), padding=5, spacing=10)
        menu_btn = Button(text="☰", size_hint=(0.15, 1), background_color=(0.1, 0.5, 0.8, 1), font_size=25, bold=True)
        menu_btn.bind(on_press=self.open_sidebar)
        
        self.search_bar = TextInput(hint_text="Search Stocks, F&O...", multiline=False, size_hint=(0.85, 1))
        self.search_bar.bind(on_text_validate=self.search_action)
        
        header.add_widget(menu_btn)
        header.add_widget(self.search_bar)
        self.layout.add_widget(header)

        # 2. INDICES GRID (Nifty, BankNifty, etc.)
        indices_grid = GridLayout(cols=3, size_hint=(1, 0.2), spacing=5, padding=5)
        for name, price in self.indices.items():
            box = BoxLayout(orientation='vertical', padding=5)
            box.add_widget(Label(text=name, font_size=12, color=(0.7, 0.7, 0.7, 1)))
            box.add_widget(Label(text=f"₹{price}", bold=True, font_size=14, color=(0, 1, 0, 1)))
            indices_grid.add_widget(box)
        self.layout.add_widget(indices_grid)

        # 3. WATCHLIST LABEL
        self.layout.add_widget(Label(text="WATCHLIST", bold=True, color=(1, 0.8, 0, 1), size_hint=(1, 0.05)))

        # 4. LIVE MARKET LIST (Stocks)
        scroll = ScrollView()
        self.stock_list_box = BoxLayout(orientation='vertical', spacing=8, size_hint_y=None, padding=10)
        self.stock_list_box.bind(minimum_height=self.stock_list_box.setter('height'))
        
        self.refresh_watchlist()
        
        scroll.add_widget(self.stock_list_box)
        self.layout.add_widget(scroll)
        
        return self.layout

    def refresh_watchlist(self, filter_text=""):
        self.stock_list_box.clear_widgets()
        for name, price in self.stocks.items():
            if filter_text.upper() in name.upper():
                btn = Button(text=f"{name}      ₹{price}", size_hint_y=None, height=70, background_color=(0.1, 0.1, 0.15, 1))
                btn.bind(on_press=lambda x, n=name, p=price: self.show_trade_panel(n, p))
                self.stock_list_box.add_widget(btn)

    def search_action(self, instance):
        self.refresh_watchlist(self.search_bar.text)

    # --- SIDEBAR MENU ---
    def open_sidebar(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text="RAHUL SINGH TRADING PRO", bold=True, color=(1, 0.8, 0, 1), size_hint_y=None, height=40))
        content.add_widget(Label(text=f"Wallet: ₹{self.balance}", color=(0, 1, 0, 1), bold=True))
        
        btns = [("👤 Profile", self.show_profile), ("💰 Buy Coins", self.show_store), ("🎁 Claim Bonus", self.show_refer_popup), ("📞 Contact Rahul", self.show_contact), ("🤖 Chandel Helpline", self.show_helpline)]
        for t, f in btns:
            b = Button(text=t, size_hint_y=None, height=50, background_color=(0.2, 0.2, 0.3, 1))
            b.bind(on_press=f); content.add_widget(b)
        
        content.add_widget(Label(size_hint_y=1))
        content.add_widget(Label(text=f"App Version: {APP_VERSION}", color=(0.5, 0.5, 0.5, 1), size_hint_y=None, height=30))
        self.sidebar = Popup(title="Menu", content=content, size_hint=(0.75, 0.9), pos_hint={'x': 0, 'y': 0.05}); self.sidebar.open()

    # --- TRADE & INDICATORS ---
    def show_trade_panel(self, n, p):
        content = BoxLayout(orientation='vertical', spacing=10, padding=15)
        content.add_widget(Label(text=f"[b]{n}[/b]", markup=True, font_size=20))
        content.add_widget(Label(text=f"RSI: {random.randint(30,70)} | EMA: ₹{p-10}"))
        
        trade_btns = BoxLayout(spacing=10, size_hint_y=0.4)
        buy_btn = Button(text="BUY", background_color=(0,1,0,1)); buy_btn.bind(on_press=lambda x: self.open_whatsapp(n))
        sell_btn = Button(text="SELL", background_color=(1,0,0,1)); sell_btn.bind(on_press=lambda x: self.open_whatsapp(n))
        
        trade_btns.add_widget(buy_btn); trade_btns.add_widget(sell_btn)
        content.add_widget(trade_btns)
        Popup(title="Trading Terminal", content=content, size_hint=(0.9, 0.6)).open()

    # Helper Functions
    def open_whatsapp(self, n): webbrowser.open(f"https://wa.me/918787269197?text=Rahul Sir, mujhe {n} buy/sell karna hai.")
    def save_data(self): self.store.put('user_data', balance=self.balance, referral_code=self.my_referral_code)
    def show_popup(self, t, m): Popup(title=t, content=Label(text=m, halign='center'), size_hint=(0.8, 0.4)).open()
    def show_profile(self, x): self.show_popup("Profile", f"Balance: ₹{self.balance}\nCode: {self.my_referral_code}")
    def show_contact(self, x): self.show_popup("Contact", "Rahul Singh: 8787269197")
    def show_helpline(self, x): self.show_popup("Chandel Helpline", "Chandel Helpline active hai!")
    def show_store(self, x): self.show_popup("Store", "Recharge ke liye Rahul Sir ko\n8787269197 par WhatsApp karein.")
    def show_refer_popup(self, x): self.show_popup("Bonus", "Referral code sidebar ke 'Claim Bonus'\nsection mein enter karein.")

if __name__ == '__main__':
    TradingApp().run()
