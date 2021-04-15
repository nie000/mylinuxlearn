# -*- coding: utf-8 -*-
import tempfile
import Qt as Qtegg
from Qt.QtWidgets import *
from Qt.QtCore import *
from Qt.QtGui import *
from screen_shot_ui import Ui_ThumbnailWidget
import screen_grab


class ThumbnailWidget(QWidget):
    """
    Thumbnail widget that provides screen capture functionality
    _get_thumbnail_path() can return the screen path  C:/..../Temp/******.png
    """

    thumbnail_changed = Signal()

    def __init__(self, parent=None):
        """
        Construction
        """
        QWidget.__init__(self, parent)
        self._ui = Ui_ThumbnailWidget()
        self._ui.setupUi(self)

        # create layout to control buttons frame
        layout = QHBoxLayout()
        layout.addWidget(self._ui.buttons_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        # connect to buttons:
        self._ui.camera_btn.clicked.connect(self._on_camera_clicked)

        self._btns_transition_anim = None
        self._update_ui()

        self.thumbnail_changed.connect(self._on_thumbnail_changed)

    # @property
    def _get_thumbnail(self):
        pm_map = self._ui.thumbnail.pixmap()
        return pm_map if pm_map and not pm_map.isNull() else None

    def get_thumbnail_path(self):
        pm_map = self._get_thumbnail()
        if pm_map:
            output_path = tempfile.NamedTemporaryFile(suffix=".png",
                                                      prefix="screencapture_",
                                                      delete=False).name
            pm_map.save(output_path)
            return output_path
        return None

    # @thumbnail.setter
    def _set_thumbnail(self, value):
        self._ui.thumbnail.setPixmap(value if value else QPixmap())
        self._update_ui()
        self.thumbnail_changed.emit()
    thumbnail = property(_get_thumbnail, _set_thumbnail)

    def enable_screen_capture(self, enable):
        self._ui.camera_btn.setVisible(enable)

    def resizeEvent(self, event):
        self._update_ui()

    def enterEvent(self, event):
        """
        when the cursor enters the control, show the buttons
        """
        if self.thumbnail and self._are_any_btns_enabled():
            self._ui.buttons_frame.show()
            if hasattr(Qtegg.QtCore, "QAbstractAnimati1on"):
                self._run_btns_transition_anim(QAbstractAnimation.Forward)
            else:
                # Q*Animation classes aren't available so just
                # make sure the button is visible:
                self.btn_visibility = 1.0

    def leaveEvent(self, event):
        """
        when the cursor leaves the control, hide the buttons
        """
        if self.thumbnail and self._are_any_btns_enabled():
            if hasattr(Qtegg.QtCore, "QAbstractAnimation"):
                self._run_btns_transition_anim(QAbstractAnimation.Backward)
            else:
                # Q*Animation classes aren't available so just
                # make sure the button is hidden:
                self._ui.buttons_frame.hide()
                self.btn_visibility = 0.0

    def _are_any_btns_enabled(self):
        """
        Return if any of the buttons are enabled
        """
        return not (self._ui.camera_btn.isHidden())

    """
    button visibility property used by QPropertyAnimation
    """
    def get_btn_visibility(self):
        return self._btns_visibility

    def set_btn_visibility(self, value):
        self._btns_visibility = value
        self._ui.buttons_frame.setStyleSheet("#buttons_frame {border-radius: 2px; background-color: rgba(32, 32, 32, %d);}" % (64 * value))
    btn_visibility = Property(float, get_btn_visibility, set_btn_visibility)

    def _run_btns_transition_anim(self, direction):
        """
        Run the transition animation for the buttons
        """
        if not self._btns_transition_anim:
            # set up anim:
            self._btns_transition_anim =  QPropertyAnimation(self, "btn_visibility")
            self._btns_transition_anim.setDuration(150)
            self._btns_transition_anim.setStartValue(0.0)
            self._btns_transition_anim.setEndValue(1.0)
            self._btns_transition_anim.finished.connect(self._on_btns_transition_anim_finished)

        if self._btns_transition_anim.state() == QAbstractAnimation.Running:
            if self._btns_transition_anim.direction() != direction:
                self._btns_transition_anim.pause()
                self._btns_transition_anim.setDirection(direction)
                self._btns_transition_anim.resume()
            else:
                pass # just let animation continue!
        else:
            self._btns_transition_anim.setDirection(direction)
            self._btns_transition_anim.start()

    def _on_btns_transition_anim_finished(self):
        if self._btns_transition_anim.direction() == QAbstractAnimation.Backward:
            self._ui.buttons_frame.hide()

    def _on_camera_clicked(self):
        if self.parent():
            self.parent().hide()
        else:
            self.hide()
        pm_map = self._on_screenshot()
        if pm_map:
            self.thumbnail = pm_map

    def _update_ui(self):
        # maximum size of thumbnail is widget geom:
        thumbnail_geom = self.geometry()
        thumbnail_geom.moveTo(0, 0)
        scale_contents = False

        pm_map = self.thumbnail
        if pm_map:
            # work out size thumbnail should be to maximize size
            # whilst retaining aspect ratio
            pm_sz = pm_map.size()

            h_scale = float(thumbnail_geom.height()-4)/float(pm_sz.height())
            w_scale = float(thumbnail_geom.width()-4)/float(pm_sz.width())
            scale = min(1.0, h_scale, w_scale)
            scale_contents = (scale < 1.0)

            new_height = min(int(pm_sz.height() * scale), thumbnail_geom.height())
            new_width = min(int(pm_sz.width() * scale), thumbnail_geom.width())

            new_geom = QRect(thumbnail_geom)
            new_geom.moveLeft(((thumbnail_geom.width()-4)/2 - new_width/2)+2)
            new_geom.moveTop(((thumbnail_geom.height()-4)/2 - new_height/2)+2)
            new_geom.setWidth(new_width)
            new_geom.setHeight(new_height)
            thumbnail_geom = new_geom

        self._ui.thumbnail.setScaledContents(scale_contents)
        self._ui.thumbnail.setGeometry(thumbnail_geom)

        # now update buttons based on current thumbnail:
        if not self._btns_transition_anim or self._btns_transition_anim.state() == QAbstractAnimation.Stopped:
            if self.thumbnail or not self._are_any_btns_enabled():
                self._ui.buttons_frame.hide()
                self._btns_visibility = 0.0
            else:
                self._ui.buttons_frame.show()
                self._btns_visibility = 1.0

    def _safe_get_dialog(self):
        """
        Get the widgets dialog parent.

        just call self.window() but this is unstable in Nuke
        Previously this would
        causing a crash on exit - suspect that it's caching
        something internally which then doesn't get cleaned
        up properly...
        """
        current_widget = self
        while current_widget:
            if isinstance(current_widget, QDialog):
                return current_widget
            current_widget = current_widget.parentWidget()
        return None

    def _on_screenshot(self):
        """
        Perform the actual screenshot
        """
        # hide the containing window - we can't actuall hide
        # the window as this will break modality!  Instead
        # we have to move the window off the screen:
        win = self._safe_get_dialog()

        win_geom = None
        if win:
            win_geom = win.geometry()
            win.setGeometry(1000000, 1000000, win_geom.width(), win_geom.height())
            # make sure this event is processed:
            QCoreApplication.processEvents()
            QCoreApplication.sendPostedEvents(None, 0)
            QCoreApplication.flush()
        try:
            # get temporary file to use:
            # to be cross-platform and python 2.5 compliant, we can't use
            # tempfile.NamedTemporaryFile with delete=False.  Instead, we
            # use tempfile.mkstemp which does practically the same thing!
            # tf, path = tempfile.mkstemp(suffix=".png", prefix="tanktmp")
            # if tf:
            #     os.close(tf)
            pm_map = screen_grab.screen_capture()
        finally:
            # restore the window:
            if win:
                win.setGeometry(win_geom)
                QCoreApplication.processEvents()
        return pm_map

    def _on_thumbnail_changed(self):
        if self.parent():
            self.parent().show()
        else:
            self.show()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    tw = ThumbnailWidget()
    tw.show()
    sys.exit(app.exec_())
