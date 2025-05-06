import sys
import os
from PyQt5.QtCore import QPropertyAnimation, pyqtProperty, QEasingCurve, Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QStackedLayout,
    QGraphicsOpacityEffect,
    QLabel,
    QPushButton,
    QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QFontDatabase, QFont




class FadeWidget(QWidget):
    def __init__(self, child_widget):
        super().__init__()
        self._opacity = 1.0
        self.effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.effect)
        self.setAutoFillBackground(True)
        self.setStyleSheet("background-color: #000000;")
        

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(child_widget)

    def get_opacity(self):
        return self._opacity

    def set_opacity(self, value):
        self._opacity = value
        self.effect.setOpacity(value)

    opacity = pyqtProperty(float, get_opacity, set_opacity)

# ...existing imports...

# ...existing imports...

# ...existing imports...

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Decentralized Widget Demo")
        self.setGeometry(100, 100, 1920, 1080)

        self.current = 0  # Start with the first widget

        main_widget = QWidget()
        main_widget.setStyleSheet("background-color: #000000;")
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        self.stack = QStackedLayout()
        main_layout.addLayout(self.stack)

        self.fade_widgets = []
        self._animations = []
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._auto_switch)

        # Add widgets
        self.create_initial_widget(next_widget_index=1)
        self.create_widget1(next_widget_index=2)
        self.create_widget2(next_widget_index1=0, next_widget_index2=1)

        # Set the first widget as visible
        self.stack.setCurrentWidget(self.fade_widgets[0])
        self.fade_widgets[0].set_opacity(1)

        # Start the timer if the first widget has auto transition
        self._start_auto_timer_for_current()

    def create_initial_widget(self, next_widget_index):
        """
        Creates the initial widget with an image and auto transition to widget1.
        """
        widget = QWidget()
        widget.setStyleSheet("background-color: #000000;")
        layout = QVBoxLayout(widget)

        # Add an image to the initial widget
        label = QLabel()
        label.setPixmap(QPixmap("cupra.png").scaled(400, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        fade_widget = FadeWidget(widget)
        self.stack.addWidget(fade_widget)
        self.fade_widgets.append(fade_widget)

        # Store transition behavior
        fade_widget.auto = True
        fade_widget.duration = 3000  # Auto transition after 3 seconds
        fade_widget.next_widget_index = next_widget_index

    def create_widget1(self, next_widget_index):
        """
        Creates the first widget with manual transition via button.
        """
        widget = QWidget()
        widget.setStyleSheet("background-color: #000000;")
        layout = QVBoxLayout(widget)
          # Left, Top, Right, Bottom margins

        label = QLabel("LO QUE SIENTES\nIMPORTA", alignment=Qt.AlignCenter)

        label.setStyleSheet(f"color: white; font-size: 150px; font-family: '{jostLight}';")
        layout.addWidget(label)

        fade_widget = FadeWidget(widget)
        self.stack.addWidget(fade_widget)
        self.fade_widgets.append(fade_widget)

        # Connect button for manual transition
        # Store transition behavior
        fade_widget.auto = True
        fade_widget.duration = 2000  # Auto transition after 3 seconds
        fade_widget.next_widget_index = next_widget_index

    def create_widget2(self, next_widget_index1, next_widget_index2):
        """
        Creates the second widget with auto transition after 2000ms.
        """
        widget = QWidget()
        widget.setStyleSheet("background-color: #000000;")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(108, 108, 50, 20)
        label1 = QLabel("ENTENDER TU ESTADO DE ÁNIMO\nES CLAVE PODER PARA REFLEXIONAR SOBRE\nLO QUE PODRÍA INFLUIR EN TU\nBIENESTAR EMOCIONAL.", alignment=Qt.AlignLeft)
        font_path1 = os.path.join(os.path.dirname(__file__), "Jost-ExtraLight.ttf")
        font_id1 = QFontDatabase.addApplicationFont(font_path1)
        if font_id1 == -1:
            print("Failed to load font: Jost-ExtraLight.ttf")
        else:
            jostExtraLight = QFontDatabase.applicationFontFamilies(font_id1)[0]
            print("Loaded font family:", jostExtraLight)

        label1.setStyleSheet(f"color: white; font-size: 75px; font-family: 'Jost'; font-weight: 200;")
        layout.addWidget(label1)

        button = QPushButton("ESCANEAR ESTADO EMOCIONAL")
        button.setStyleSheet("background-color: #000; color: white; font-size: 50px; font-family: 'Jost'; font-weight: 150; border-bottom: 40px solid white;")
        layout.addWidget(button, alignment=Qt.AlignLeft)
                
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        line.setStyleSheet("background-color: orange;")
        line.setFixedSize(750, 5)
        layout.addWidget(line)

        button2 = QPushButton("VER ESTADÍSTICAS DEL ESTADO EMOCIONAL")
        button2.setStyleSheet("background-color: #000; color: white; font-size: 50px; font-family: 'Jost'; font-weight: 150;")
        layout.addWidget(button2, alignment=Qt.AlignLeft)

        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Plain)
        line2.setStyleSheet("background-color: orange;")
        line2.setFixedSize(1000, 5)
        layout.addWidget(line2)

        fade_widget = FadeWidget(widget)
        self.stack.addWidget(fade_widget)
        self.fade_widgets.append(fade_widget)

        # Connect button for manual transition
        button.clicked.connect(lambda: self.fade_to(self.current, next_widget_index1))
        button2.clicked.connect(lambda: self.fade_to(self.current, next_widget_index2))


        # Store transition behavior
        fade_widget.auto = False

    def _start_auto_timer_for_current(self):
        current_widget = self.fade_widgets[self.current]
        if getattr(current_widget, "auto", False):
            self.timer.start(getattr(current_widget, "duration", 0))
        else:
            self.timer.stop()

    def _auto_switch(self):
        # Called by timer: switch to the next widget
        next_idx = self.fade_widgets[self.current].next_widget_index
        self.fade_to(self.current, next_idx)

    def fade_to(self, from_idx, to_idx):
        fade_out_widget = self.fade_widgets[from_idx]
        fade_in_widget = self.fade_widgets[to_idx]

        fade_out_anim = QPropertyAnimation(fade_out_widget, b"opacity")
        fade_out_anim.setDuration(400)
        fade_out_anim.setStartValue(1)
        fade_out_anim.setEndValue(0)
        fade_out_anim.setEasingCurve(QEasingCurve.InOutQuad)

        def on_fade_out_finished():
            self.stack.setCurrentWidget(fade_in_widget)
            fade_in_widget.set_opacity(0)
            fade_in_anim = QPropertyAnimation(fade_in_widget, b"opacity")
            fade_in_anim.setDuration(400)
            fade_in_anim.setStartValue(0)
            fade_in_anim.setEndValue(1)
            fade_in_anim.setEasingCurve(QEasingCurve.InOutQuad)
            fade_in_anim.start()
            self._animations.append(fade_in_anim)
            fade_in_anim.finished.connect(lambda: self._animations.remove(fade_in_anim))
            # After fade in, update current and setup timer for new widget
            self.current = to_idx
            self._start_auto_timer_for_current()

        fade_out_anim.finished.connect(on_fade_out_finished)
        fade_out_anim.start()
        self._animations.append(fade_out_anim)
        fade_out_widget.set_opacity(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("QWidget { background-color: #000000; }")
    font_path = os.path.join(os.path.dirname(__file__), "Jost-Light.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)
    jostLight = QFontDatabase.applicationFontFamilies(font_id)[0]

    window = MainScreen()
    window.show()
    sys.exit(app.exec_())