from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class RahulSinghGuard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        self.pnl = 0.0  
        self.balance = 100000.0
        self.loss_limit = -2000.0
        self.add_widget(Label(text="Rahul Singh (AI Assistant)", font_size=24, color=(0, 0.8, 1, 1)))
        self.status = Label(text="Rahul Singh: Market active. Practice well!", font_size=16)
        self.add_widget(self.status)
        self.pnl_display = Label(text=f"P&L: ₹{self.pnl} | Balance: ₹{self.balance}", font_size=18)
        self.add_widget(self.pnl_display)
        self.trade_btn = Button(text="Execute Practice Trade", background_color=(0, 0.7, 0, 1), size_hint=(1, 0.2))
        self.trade_btn.bind(on_press=self.process_trade)
        self.add_widget(self.trade_btn)

    def process_trade(self, instance):
        self.pnl -= 1000.0 
        self.balance -= 1000.0
        self.pnl_display.text = f"P&L: ₹{self.pnl} | Balance: ₹{self.balance}"
        if self.pnl <= self.loss_limit:
            self.status.text = "Rahul Singh: STOP! Loss limit reached. Trading locked."
            self.status.color = (1, 0, 0, 1)
            self.trade_btn.disabled = True
        else:
            self.status.text = "Rahul Singh: Trade done. Watch your risk!"

class MainApp(App):
    def build(self):
        return RahulSinghGuard()

if __name__ == "__main__":
    MainApp().run()
