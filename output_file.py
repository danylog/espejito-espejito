import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QScrollArea, QLabel, QFrame
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPoint
from PyQt5.QtGui import QFontDatabase, QFont  # Add these imports

class HorizontalScroller(QWidget):
    def __init__(self):
        super().__init__()
        
        # Load custom font
        font_id = QFontDatabase.addApplicationFont("Jost-Regular.ttf")  # Replace with your font path
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            self.custom_font = QFont(font_family)
        else:
            print("Error: Could not load custom font")
            self.custom_font = QFont()  # Fallback to default font
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.resize(800, 400)
        self.setStyleSheet("background-color: black;")

        self.scroll_area = QScrollArea()
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: black; }")

        # Container widget
        self.container = QWidget()
        self.container.setStyleSheet("background-color: black;")
        self.hbox = QHBoxLayout(self.container)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.hbox.setSpacing(0)

        # Button style with custom font
        self.button_style = f"""
            QPushButton {{
                color: white;
                background-color: black;
                border: 2px solid white;
                font-family: {self.custom_font.family()};
                font-size: 20px;
                min-width: 40px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: #333;
            }}
            QPushButton:pressed {{
                background-color: #444;
            }}
        """

        # Create multiple "screens"
        self.screens = []
        for i in range(5):
            screen = QFrame()
            screen_layout = QVBoxLayout(screen)
            
            # Content container to hold label and buttons
            content_container = QWidget()
            content_layout = QVBoxLayout(content_container)
            
            # Add label with custom font
            label = QLabel(f"Screen {i+1}")
            label.setAlignment(Qt.AlignCenter)
            label.setFont(self.custom_font)  # Set custom font directly
            label.setStyleSheet("font-size: 32px; color: white;")
            content_layout.addWidget(label)
            
            # Add navigation buttons
            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            
            prev_btn = QPushButton("←")
            next_btn = QPushButton("→")
            
            # Set custom font for buttons
            prev_btn.setFont(self.custom_font)
            next_btn.setFont(self.custom_font)
            
            prev_btn.setStyleSheet(self.button_style)
            next_btn.setStyleSheet(self.button_style)
            
            btn_layout.addWidget(prev_btn)
            btn_layout.addWidget(next_btn)
            btn_layout.setContentsMargins(10, 10, 10, 10)
            btn_layout.setSpacing(10)
            
            content_layout.addWidget(btn_container)
            content_layout.setAlignment(Qt.AlignCenter)
            
            # Center the content in the screen
            screen_layout.addWidget(content_container)
            screen_layout.setAlignment(Qt.AlignCenter)
            
            # Set up the screen
            screen.setStyleSheet("background-color: black;")
            screen.setFixedSize(800, 400)
            
            self.hbox.addWidget(screen)
            self.screens.append(screen)
            
            # Connect buttons
            prev_btn.clicked.connect(self.scroll_left)
            next_btn.clicked.connect(self.scroll_right)

        self.scroll_area.setWidget(self.container)

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.scroll_area)

        self.current_index = 0

    def scroll_to_index(self, index):
        if 0 <= index < len(self.screens):
            self.current_index = index
            target_x = index * self.screens[0].width()
            anim = QPropertyAnimation(self.scroll_area.horizontalScrollBar(), b"value")
            anim.setDuration(400)
            anim.setStartValue(self.scroll_area.horizontalScrollBar().value())
            anim.setEndValue(target_x)
            anim.setEasingCurve(QEasingCurve.InOutQuad)
            anim.start()
            self.anim = anim

    def scroll_left(self):
        self.scroll_to_index(self.current_index - 1)

    def scroll_right(self):
        self.scroll_to_index(self.current_index + 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HorizontalScroller()
    window.show()
    sys.exit(app.exec_())