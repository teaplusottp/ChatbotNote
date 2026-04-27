from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDRectangleFlatButton
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivymd.uix.pickers import MDColorPicker
from kivymd.uix.dialog import MDDialog
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.behaviors import ButtonBehavior
from kivy.utils import platform

# Import plugin giao diện cài đặt (ChatInfoScreen)
from plugin.chat_info import ChatInfoScreen

# Class để cho phép nhấn vào khu vực Avatar + Tên
class ClickableInfoArea(ButtonBehavior, MDBoxLayout):
    pass

class MessageBubble(MDBoxLayout):
    msg_text = StringProperty()
    sender = StringProperty()

class ChatScreen(Screen):
    pass

class ChattopApp(MDApp):
    current_accent = ListProperty(get_color_from_hex("#0084FF"))  
    current_avatar = StringProperty("robot-outline")
    is_avatar_image = StringProperty("icon")
    chat_partner_name = StringProperty("Chattop AI") # Biến lưu Tên đối tác
    
    characters = {
        "Hoa nữ": {"icon": "flower", "color": "#FF69B4"},
        "Trà sữa trân châu": {"icon": "tea", "color": "#A0522D"},
        "Bông ơi": {"icon": "cloud", "color": "#87CEEB"},
        "Chuyên giới": {"icon": "briefcase", "color": "#4169E1"},
        "Taylor Swift": {"icon": "music-note", "color": "#FFD700"},
        "Cyberpunk 2077": {"icon": "robot", "color": "#FFFF00"},
    }

    def build(self):
        self.theme_cls.theme_style = "Light" 
        
        # Khởi tạo Quản lý màn hình (ScreenManager)
        self.sm = ScreenManager(transition=SlideTransition())
        
        Builder.load_file("assets/chatbot.kv")
        
        # Gắn các màn hình vào
        self.chat_screen = ChatScreen(name="chat")
        self.info_screen = ChatInfoScreen(name="info")
        
        self.sm.add_widget(self.chat_screen)
        self.sm.add_widget(self.info_screen)
        
        return self.sm

    # --- ĐIỀU HƯỚNG ---
    def open_chat_info(self):
        self.sm.transition.direction = "left"
        self.sm.current = "info"

    def go_back_to_chat(self):
        self.sm.transition.direction = "right"
        self.sm.current = "chat"

    # --- CHARACTER SELECTION ---
    def open_character_picker(self):
        dialog_content = MDBoxLayout(
            orientation="vertical", spacing="12dp", padding="16dp",
            size_hint_y=None, height="500dp"
        )
        
        from kivymd.uix.label import MDLabel
        title = MDLabel(
            text="Chọn đối tác chat", font_size="18sp", bold=True,
            size_hint_y=None, height="40dp", theme_text_color="Primary"
        )
        dialog_content.add_widget(title)
        
        grid = MDGridLayout(cols=2, spacing="12dp", size_hint_y=None, height="420dp", padding="0dp")
        
        # Thêm lựa chọn mở Gallery ở đầu list
        gallery_btn = MDRectangleFlatButton(
            text="[Mở Thư Viện Ảnh]", size_hint_y=None, height="60dp",
            line_color=get_color_from_hex("#000000"), line_width="2dp",
            text_color=get_color_from_hex("#000000"), theme_text_color="Custom"
        )
        gallery_btn.bind(on_release=lambda x: [self.open_gallery_for_avatar(), dialog.dismiss()])
        grid.add_widget(gallery_btn)

        for char_name, char_data in self.characters.items():
            char_button = MDRectangleFlatButton(
                text=char_name, size_hint_y=None, height="60dp",
                line_color=get_color_from_hex(char_data["color"]), line_width="2dp",
                text_color=get_color_from_hex(char_data["color"]), theme_text_color="Custom"
            )
            char_button.bind(on_release=lambda btn, name=char_name, data=char_data: self.select_character(name, data, dialog))
            grid.add_widget(char_button)
        
        dialog_content.add_widget(grid)
        
        # Sửa lỗi con trỏ UnboundLocalError bằng cách định nghĩa dialog trước
        global dialog
        dialog = MDDialog(content_cls=dialog_content, size_hint=(0.9, None), height="600dp")
        dialog.open()

    def select_character(self, name, char_data, dialog_instance):
        self.chat_partner_name = name
        self.current_avatar = char_data.get("icon", "robot-outline")
        self.is_avatar_image = "icon"
        color_hex = char_data.get("color", "#0084FF")
        self.current_accent = get_color_from_hex(color_hex)
        dialog_instance.dismiss()

    # --- CUSTOM MESSENGER THEME ---
    def open_color_picker(self):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.bind(on_select_color=self.handle_theme_color, on_release=self.get_selected_color)
        color_picker.open()

    def handle_theme_color(self, instance_color_picker, color):
        pass

    def get_selected_color(self, instance_color_picker, type_color, selected_color):
        self.current_accent = selected_color
        instance_color_picker.dismiss()

    # --- THƯ VIỆN ẢNH (ANDROID FIX) ---
    def open_gallery_for_avatar(self):
        # Yêu cầu quyền trên Android trước khi gọi thư viện
        if platform == "android":
            try:
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.READ_MEDIA_IMAGES])
            except Exception as e:
                print("Không thể xin quyền Android:", e)
                
        try:
            from plyer import filechooser
            filechooser.open_file(
                on_selection=self.handle_avatar_selection, 
                filters=[("Image Files", "*.png", "*.jpg", "*.jpeg")]
            )
        except Exception as e:
            print(f"Lỗi hệ thống khi mở thư viện ảnh: {e}")

    def handle_avatar_selection(self, selection):
        if selection:
            self.chat_partner_name = "Custom Avatar"
            self.current_avatar = selection[0]
            self.is_avatar_image = "image"

    # --- MESSAGING LOGIC ---
    def send_message(self):
        # Cập nhật ID trỏ tới chat_screen thay vì self.root
        text_input = self.chat_screen.ids.text_input
        message = text_input.text.strip()

        if message:
            self.add_message_bubble(message, "user")
            text_input.text = ""
            Clock.schedule_once(lambda dt: self.llm_response(message), 1.2)

    def llm_response(self, user_message):
        reply = f"I am a simulated AI. I received your message: '{user_message}'"
        self.add_message_bubble(reply, "llm")

    def add_message_bubble(self, text, sender):
        chat_list = self.chat_screen.ids.chat_list
        bubble = MessageBubble(msg_text=text, sender=sender)
        chat_list.add_widget(bubble)
        Clock.schedule_once(lambda dt: self._scroll_to_bottom(), 0.1)

    def _scroll_to_bottom(self):
        self.chat_screen.ids.scroll_view.scroll_y = 0

if __name__ == "__main__":
    ChattopApp().run()