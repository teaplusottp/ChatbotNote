from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivymd.uix.pickers import MDColorPicker
from plyer import filechooser

class MessageBubble(MDBoxLayout):
    msg_text = StringProperty()
    sender = StringProperty()

class ChattopApp(MDApp):
    current_accent = ListProperty(get_color_from_hex("#0084FF")) # Default Messenger Blue
    
    # Store the path to the custom avatar. We start with a default KivyMD icon name.
    current_avatar = StringProperty("robot-outline")
    is_avatar_image = StringProperty("icon") # "icon" or "image"

    def build(self):
        self.theme_cls.theme_style = "Light" 
        return Builder.load_file("assets/chatbot.kv")

    # --- CUSTOM MESSENGER THEME (COLOR PICKER) ---
    def open_color_picker(self):
        """Opens a dynamic color picker so the user can choose any theme color."""
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.bind(
            on_select_color=self.handle_theme_color,
            on_release=self.get_selected_color,
        )
        color_picker.open()

    def handle_theme_color(self, instance_color_picker, color):
        pass # Optional: update things in real-time as they drag

    def get_selected_color(self, instance_color_picker, type_color, selected_color):
        """Applies the chosen color to the chat."""
        self.current_accent = selected_color
        instance_color_picker.dismiss()

    # --- GALLERY AVATAR PICKER ---
    def open_gallery_for_avatar(self):
        """Opens the native device gallery to pick a chatbot avatar."""
        try:
            # Opens native file chooser looking for images
            filechooser.open_file(on_selection=self.handle_avatar_selection, filters=[("Image Files", "*.png", "*.jpg", "*.jpeg")])
        except Exception as e:
            print(f"Gallery not supported on this platform without proper permissions: {e}")

    def handle_avatar_selection(self, selection):
        if selection:
            # selection is a list of file paths. We take the first one.
            self.current_avatar = selection[0]
            self.is_avatar_image = "image" # Tell the UI to render an Image, not an Icon

    # --- MESSAGING LOGIC ---
    def send_message(self):
        text_input = self.root.ids.text_input
        message = text_input.text.strip()

        if message:
            self.add_message_bubble(message, "user")
            text_input.text = ""
            Clock.schedule_once(lambda dt: self.llm_response(message), 1.2)

    def llm_response(self, user_message):
        reply = f"I am a simulated AI. I received your message: '{user_message}'. How else can I assist you?"
        self.add_message_bubble(reply, "llm")

    def add_message_bubble(self, text, sender):
        chat_list = self.root.ids.chat_list
        bubble = MessageBubble(msg_text=text, sender=sender)
        chat_list.add_widget(bubble)
        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)

    def _scroll_to_bottom(self):
        self.root.ids.scroll_view.scroll_y = 0

if __name__ == "__main__":
    ChattopApp().run()