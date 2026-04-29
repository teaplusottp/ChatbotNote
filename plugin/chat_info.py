import os
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import (
    MDDialog, MDDialogButtonContainer, MDDialogContentContainer, 
    MDDialogHeadlineText, MDDialogSupportingText
)
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarSupportingText
from kivy.app import App
from kivy.uix.widget import Widget

kv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'chat_info.kv')
Builder.load_file(kv_path)

class ChatInfoScreen(MDScreen):
    nickname_dialog = None
    clear_dialog = None
    search_dialog = None
    profile_dialog = None
    group_dialog = None

    def show_toast(self, message):
        MDSnackbar(
            MDSnackbarSupportingText(text=message),
            y="24dp", orientation="horizontal", pos_hint={"center_x": 0.5}, size_hint_x=0.9,
        ).open()

    # --- TÌM KIẾM ---
    def show_search_dialog(self):
        self.search_input = MDTextField(
            MDTextFieldHintText(text="Nhập từ khóa cần tìm..."),
            mode="outlined",
        )
        content = MDBoxLayout(orientation="vertical", adaptive_height=True, padding="10dp")
        content.add_widget(self.search_input)

        self.search_dialog = MDDialog(
            MDDialogHeadlineText(text="Tìm kiếm trong chat"),
            MDDialogContentContainer(content, orientation="vertical"),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Hủy lọc"), style="text", on_release=self.reset_search),
                MDButton(MDButtonText(text="Tìm"), style="text", on_release=self.execute_search),
                spacing="8dp",
            ),
        )
        self.search_dialog.open()

    def execute_search(self, *args):
        keyword = self.search_input.text.strip()
        if keyword:
            count = App.get_running_app().filter_chat(keyword)
            self.show_toast(f"Tìm thấy {count} tin nhắn khớp từ khóa")
            self.search_dialog.dismiss()
            App.get_running_app().go_back_to_chat()

    def reset_search(self, *args):
        App.get_running_app().filter_chat("") # Trả lại toàn bộ tin nhắn
        self.search_dialog.dismiss()
        App.get_running_app().go_back_to_chat()

    # --- TRANG CÁ NHÂN ---
    def show_profile_dialog(self):
        app = App.get_running_app()
        self.profile_dialog = MDDialog(
            MDDialogHeadlineText(text=f"Profile: {app.chat_partner_name}"),
            MDDialogSupportingText(text="Trạng thái: Đang hoạt động\nTham gia từ: 2026\nSở thích: Hỗ trợ code và fix bug dạo."),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Đóng"), style="text", on_release=lambda x: self.profile_dialog.dismiss()),
            ),
        )
        self.profile_dialog.open()

    # --- TẠO NHÓM ---
    def show_create_group_dialog(self):
        app = App.get_running_app()
        self.group_input = MDTextField(
            MDTextFieldHintText(text="Tên nhóm mới"),
            text=f"Nhóm của tôi & {app.chat_partner_name}",
            mode="outlined",
        )
        content = MDBoxLayout(orientation="vertical", adaptive_height=True, padding="10dp")
        content.add_widget(self.group_input)

        self.group_dialog = MDDialog(
            MDDialogHeadlineText(text="Tạo nhóm chat mới"),
            MDDialogContentContainer(content, orientation="vertical"),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Hủy"), style="text", on_release=lambda x: self.group_dialog.dismiss()),
                MDButton(MDButtonText(text="Tạo"), style="text", on_release=self.execute_create_group),
                spacing="8dp",
            ),
        )
        self.group_dialog.open()

    def execute_create_group(self, *args):
        group_name = self.group_input.text.strip()
        self.group_dialog.dismiss()
        self.show_toast(f"Đã tạo nhóm: {group_name}")

    # ... (Giữ nguyên các hàm show_nickname_dialog, apply_nickname, show_clear_chat_dialog, confirm_clear cũ của bạn) ...

    def show_nickname_dialog(self):
        app = App.get_running_app()
        
        # Luôn tạo mới nội dung để cập nhật giá trị Tên hiện tại
        self.nick_input = MDTextField(
            MDTextFieldHintText(text="Biệt danh"),
            text=app.chat_partner_name,
            mode="outlined",
        )
        
        content = MDBoxLayout(orientation="vertical", adaptive_height=True, padding="10dp")
        content.add_widget(self.nick_input)

        self.nickname_dialog = MDDialog(
            MDDialogHeadlineText(text="Đặt biệt danh"),
            MDDialogContentContainer(content, orientation="vertical"),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Hủy"), style="text", on_release=lambda x: self.nickname_dialog.dismiss()),
                MDButton(MDButtonText(text="Lưu"), style="text", on_release=self.apply_nickname),
                spacing="8dp",
            ),
        )
        self.nickname_dialog.open()

    def apply_nickname(self, *args):
        new_name = self.nick_input.text.strip()
        if new_name:
            App.get_running_app().chat_partner_name = new_name
        self.nickname_dialog.dismiss()

    def show_clear_chat_dialog(self):
        self.clear_dialog = MDDialog(
            MDDialogHeadlineText(text="Xóa đoạn chat?"),
            MDDialogSupportingText(text="Hành động này sẽ xóa vĩnh viễn tin nhắn của bạn."),
            MDDialogButtonContainer(
                Widget(),
                MDButton(MDButtonText(text="Hủy"), style="text", on_release=lambda x: self.clear_dialog.dismiss()),
                MDButton(MDButtonText(text="Xóa"), style="text", on_release=self.confirm_clear),
                spacing="8dp",
            ),
        )
        self.clear_dialog.open()

    def confirm_clear(self, *args):
        App.get_running_app().clear_chat_history()
        self.clear_dialog.dismiss()
        App.get_running_app().go_back_to_chat()