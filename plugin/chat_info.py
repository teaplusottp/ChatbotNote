from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

# Khởi tạo giao diện trang Cài đặt chung bằng KV string
Builder.load_string('''
#:import ButtonBehavior kivy.uix.behaviors.ButtonBehavior

<ChatActionItem@ButtonBehavior+MDBoxLayout>:
    orientation: "vertical"
    icon: ""
    text: ""
    spacing: "8dp"
    MDIconButton:
        icon: root.icon
        theme_text_color: "Custom"
        text_color: [1, 1, 1, 1]
        md_bg_color: [0.15, 0.15, 0.15, 1]
        pos_hint: {"center_x": 0.5}
        # Truyền sự kiện click của Icon lên cho class cha
        on_release: root.dispatch('on_release')
    MDLabel:
        text: root.text
        halign: "center"
        theme_text_color: "Custom"
        text_color: [1, 1, 1, 1]
        font_size: "13sp"

<ChatInfoListItem@MDBoxLayout>:
    size_hint_y: None
    height: "60dp"
    icon: ""
    text: ""
    secondary_text: ""
    spacing: "16dp"
    
    MDIcon:
        icon: root.icon
        theme_text_color: "Custom"
        text_color: [1, 1, 1, 1]
        size_hint_x: None
        width: "24dp"
        pos_hint: {"center_y": 0.5}
        
    MDBoxLayout:
        orientation: "vertical"
        pos_hint: {"center_y": 0.5}
        adaptive_height: True
        MDLabel:
            text: root.text
            theme_text_color: "Custom"
            text_color: [1, 1, 1, 1]
            font_size: "16sp"
            adaptive_height: True
        MDLabel:
            text: root.secondary_text
            theme_text_color: "Custom"
            text_color: [0.6, 0.6, 0.6, 1]
            font_size: "13sp"
            adaptive_height: True
            opacity: 1 if root.secondary_text else 0
            height: self.texture_size[1] if root.secondary_text else 0

<ChatInfoScreen>:
    md_bg_color: [0.03, 0.03, 0.03, 1] # Dark theme base

    MDBoxLayout:
        orientation: "vertical"

        # --- TOP BAR ---
        MDBoxLayout:
            size_hint_y: None
            height: "56dp"
            padding: "8dp"
            MDIconButton:
                icon: "arrow-left"
                theme_text_color: "Custom"
                text_color: [1, 1, 1, 1]
                on_release: app.go_back_to_chat()
            Widget:
            MDIconButton:
                icon: "dots-vertical"
                theme_text_color: "Custom"
                text_color: [1, 1, 1, 1]

        # --- SCROLLABLE CONTENT ---
        ScrollView:
            do_scroll_x: False
            
            MDBoxLayout:
                orientation: "vertical"
                adaptive_height: True
                padding: "0dp", "10dp", "0dp", "40dp"
                spacing: "20dp"

                # Avatar
                MDFloatLayout:
                    size_hint_y: None
                    height: "100dp"
                    
                    MDBoxLayout:
                        size_hint: None, None
                        size: "100dp", "100dp"
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        canvas.before:
                            Color:
                                rgba: app.current_accent
                            Ellipse:
                                pos: self.pos
                                size: self.size
                        opacity: 1 if app.is_avatar_image == "icon" else 0
                        
                    MDIcon:
                        icon: app.current_avatar if app.is_avatar_image == "icon" else ""
                        font_size: "50dp"
                        halign: "center"
                        theme_text_color: "Custom"
                        text_color: [1, 1, 1, 1]
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        opacity: 1 if app.is_avatar_image == "icon" else 0

                    FitImage:
                        source: app.current_avatar if app.is_avatar_image == "image" else ""
                        size_hint: None, None
                        size: "100dp", "100dp"
                        radius: [50,]
                        pos_hint: {"center_x": 0.5, "center_y": 0.5}
                        opacity: 1 if app.is_avatar_image == "image" else 0

                # Name
                MDLabel:
                    text: app.chat_partner_name
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: [1, 1, 1, 1]
                    font_size: "24sp"
                    bold: True
                    size_hint_y: None
                    height: self.texture_size[1]

                # 4 Action Buttons
                MDBoxLayout:
                    size_hint_y: None
                    height: "80dp"
                    padding: "20dp", "0dp"
                    spacing: "15dp"
                    
                    ChatActionItem:
                        icon: "facebook"
                        text: "Trang cá nhân"
                    ChatActionItem:
                        icon: "format-text-variant"
                        text: "Biệt danh"
                    ChatActionItem:
                        icon: "magnify"
                        text: "Tìm kiếm"
                    ChatActionItem:
                        icon: "palette"
                        text: "Tùy chỉnh"
                        # Đã xóa "lambda:" ở đây để fix lỗi
                        on_release: app.open_color_picker()

                # Settings List
                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    padding: "16dp", "20dp"
                    
                    MDLabel:
                        text: "Hành động"
                        theme_text_color: "Custom"
                        text_color: [0.6, 0.6, 0.6, 1]
                        font_size: "14sp"
                        size_hint_y: None
                        height: "40dp"
                        
                    ChatInfoListItem:
                        icon: "bell-outline"
                        text: f"Tắt thông báo về {app.chat_partner_name}"
                    ChatInfoListItem:
                        icon: "volume-high"
                        text: "Thông báo và âm thanh"
                        secondary_text: "Bật"
                    ChatInfoListItem:
                        icon: "account-group"
                        text: f"Tạo nhóm chat với {app.chat_partner_name}"
                    ChatInfoListItem:
                        icon: "download"
                        text: "Tự động lưu ảnh"
                    ChatInfoListItem:
                        icon: "share-variant"
                        text: "Chia sẻ thông tin liên hệ"

                    Widget:
                        size_hint_y: None
                        height: "20dp"

                    MDLabel:
                        text: "Quyền riêng tư và hỗ trợ"
                        theme_text_color: "Custom"
                        text_color: [0.6, 0.6, 0.6, 1]
                        font_size: "14sp"
                        size_hint_y: None
                        height: "40dp"
                        
                    ChatInfoListItem:
                        icon: "eye-outline"
                        text: "Thông báo đã đọc"
                        secondary_text: "Bật"
                    ChatInfoListItem:
                        icon: "clock-outline"
                        text: "Tin nhắn tự hủy"
                        secondary_text: "Tắt"
                    ChatInfoListItem:
                        icon: "lock-outline"
                        text: "Mã hóa đầu cuối"
                        secondary_text: "Đoạn chat này được mã hóa đầu cuối"
                    ChatInfoListItem:
                        icon: "minus-circle-outline"
                        text: "Chặn"
                    ChatInfoListItem:
                        icon: "cancel"
                        text: "Hạn chế"
                    ChatInfoListItem:
                        icon: "alert-outline"
                        text: "Báo cáo"
                        secondary_text: "Góp ý và báo cáo cuộc trò chuyện"
                    
                    MDBoxLayout:
                        size_hint_y: None
                        height: "60dp"
                        spacing: "16dp"
                        MDIcon:
                            icon: "trash-can-outline"
                            theme_text_color: "Custom"
                            text_color: [1, 0.3, 0.3, 1]
                            size_hint_x: None
                            width: "24dp"
                            pos_hint: {"center_y": 0.5}
                        MDLabel:
                            text: "Xóa đoạn chat"
                            theme_text_color: "Custom"
                            text_color: [1, 0.3, 0.3, 1]
                            font_size: "16sp"
                            pos_hint: {"center_y": 0.5}
''')

class ChatInfoScreen(MDScreen):
    pass