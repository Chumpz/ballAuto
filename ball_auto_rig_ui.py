import sys

from functools import partial

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui
import maya.cmds as cmds

import ball_auto_rig as B_Auto_Rig


class RigcentColorButton(QtWidgets.QWidget):

    color_changed = QtCore.Signal()


    def __init__(self, color=(1.0, 1.0, 1.0), parent=None):
        super(RigcentColorButton, self).__init__(parent)

        self.setObjectName("RigcentColorButton")

        self.create_control()

        self.set_size(50, 16)
        self.set_color(color)

    def create_control(self):
        window = cmds.window()
        color_slider_name = cmds.colorSliderGrp()

        self._color_slider_obj = omui.MQtUtil.findControl(color_slider_name)
        if self._color_slider_obj:
            if sys.version_info.major >= 3:
                self._color_slider_widget = wrapInstance(int(self._color_slider_obj), QtWidgets.QWidget)
            else:
                self._color_slider_widget = wrapInstance(long(self._color_slider_obj), QtWidgets.QWidget)

            main_layout = QtWidgets.QVBoxLayout(self)
            main_layout.setObjectName("main_layout")
            main_layout.setContentsMargins(0, 0, 0, 0)
            main_layout.addWidget(self._color_slider_widget)

            self._slider_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "slider")
            if self._slider_widget:
                self._slider_widget.hide()

            self._color_widget = self._color_slider_widget.findChild(QtWidgets.QWidget, "port")

            cmds.colorSliderGrp(self.get_full_name(), e=True, changeCommand=partial(self.on_color_changed))

        cmds.deleteUI(window, window=True)

    def get_full_name(self):
        if sys.version_info.major >= 3:
            return omui.MQtUtil.fullName(int(self._color_slider_obj))
        else:
            return omui.MQtUtil.fullName(long(self._color_slider_obj))

    def set_size(self, width, height):
        self._color_slider_widget.setFixedWidth(width)
        self._color_widget.setFixedHeight(height)

    def set_color(self, color):
        cmds.colorSliderGrp(self.get_full_name(), e=True, rgbValue=(color[0], color[1], color[2]))
        self.on_color_changed()

    def get_color(self):
        return cmds.colorSliderGrp(self.get_full_name(), q=True, rgbValue=True)

    def on_color_changed(self, *args):
        self.color_changed.emit()  # pylint: disable=E1101


class BallAutoRigUi(QtWidgets.QDialog):

    def __init__(self):
        if sys.version_info.major < 3:
            maya_main_window = wrapInstance(long(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)
        else:
            maya_main_window = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QWidget)

        super(BallAutoRigUi, self).__init__(maya_main_window)

        self.setMinimumWidth(300)

        self.setWindowTitle("Ball Auto-Rig")
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        if sys.version_info.major < 3:
            self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        else:
            self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.name_le = QtWidgets.QLineEdit()
        self.name_le.setPlaceholderText("ball")

        self.primary_color_btn = RigcentColorButton()
        self.primary_color_btn.set_color((0.0, 0.0, 1.0))

        self.secondary_color_btn = RigcentColorButton()
        self.secondary_color_btn.set_color((1.0, 1.0, 1.0))

        self.create_btn = QtWidgets.QPushButton("Create")
        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layout(self):
        options_layout = QtWidgets.QFormLayout()
        options_layout.addRow("Name:", self.name_le)
        options_layout.addRow("Primary:", self.primary_color_btn)
        options_layout.addRow("Secondary:", self.secondary_color_btn)

        options_grp = QtWidgets.QGroupBox("Options")
        options_grp.setLayout(options_layout)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.create_btn)
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(options_grp)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.create_btn.clicked.connect(self.create_ball)
        self.close_btn.clicked.connect(self.close)

    def create_ball(self):
        name = self.name_le.text()
        if not name:
            name = self.name_le.placeholderText()
            
        primary_color = self.primary_color_btn.get_color()
        secondary_color = self.secondary_color_btn.get_color()
        
        ball_auto_rig = B_Auto_Rig.BallAutoRig()
        ball_auto_rig.set_colors(primary_color, secondary_color)
        ball_auto_rig.construct_rig()
        
        
if __name__ == "__main__":
        
    cmds.file(newFile=True, force=True)
    
    # ball = BallAutoRig()
    # ball.construct_rig()
    
    ballUi = BallAutoRigUi()
    ballUi.show()