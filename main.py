from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

# Simulate a mobile phone screen ratio
Window.size = (400, 750)

class MessageBubble(MDBoxLayout):
    msg_text = StringProperty()
    sender = StringProperty()

class ChattopApp(MDApp):
    # Messenger-style theme colors (Blue, Coral, Purple, Green)
    theme_colors = [
        get_color_from_hex("#0084FF"), 
        get_color_from_hex("#FF5A5F"), 
        get_color_from_hex("#8A2BE2"), 
        get_color_from_hex("#05A32D"), 
    ]
    current_theme_index = 0
    current_accent = ListProperty(theme_colors[0])
    
    # Chatbot avatar options
    avatar_icons = ["robot-outline", "android", "brain", "message-bot"]
    current_avatar_index = 0
    current_avatar = StringProperty(avatar_icons[0])

    def build(self):
        self.theme_cls.theme_style = "Light" 
        return Builder.load_file("assets/chatbot.kv")

    def change_messenger_theme(self):
        """Cycles the accent color of user bubbles and icons."""
        self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_colors)
        self.current_accent = self.theme_colors[self.current_theme_index]
    
    def change_chatbot_avatar(self):
        """Cycles the chatbot avatar icon."""
        self.current_avatar_index = (self.current_avatar_index + 1) % len(self.avatar_icons)
        self.current_avatar = self.avatar_icons[self.current_avatar_index]

    def send_message(self):
        text_input = self.root.ids.text_input
        message = text_input.text.strip()

        if message:
            self.add_message_bubble(message, "user")
            text_input.text = ""

            # Simulate LLM thinking delay
            Clock.schedule_once(lambda dt: self.llm_response(message), 1.2)

    def llm_response(self, user_message):
        # Replace this string return with your actual LLM API / Chain invocation
        reply = f"I am a simulated AI. I received your message: '{user_message}'. How else can I assist you?"
        self.add_message_bubble(reply, "llm")

    def add_message_bubble(self, text, sender):
        chat_list = self.root.ids.chat_list
        bubble = MessageBubble(msg_text=text, sender=sender)
        chat_list.add_widget(bubble)
        
        # Scroll to the bottom slightly after the widget is added
        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)

    def _scroll_to_bottom(self):
        self.root.ids.scroll_view.scroll_y = 0

if __name__ == "__main__":
    ChattopApp().run()