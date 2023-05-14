# This Python file uses the following encoding: utf-8
import sys
import logging
import json

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QStringListModel, QModelIndex

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.list_model = QStringListModel()
        self.full_data = []
        self.display_data = []
        self.list_model.setStringList(self.display_data)
        self.ui.listView.setModel(self.list_model)
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.filterButton.clicked.connect(self.do_filter)
        # self.ui.listView.clicked.connect(self.select_log)
        self.ui.listView.selectionModel().currentChanged.connect(self.select_log)

    def open(self):
        log_file, _ = QFileDialog.getOpenFileName(self, 'Open file', filter='Log file(*.log)')
        if not log_file:
            return

        with open(log_file, 'r') as ifile:
            for line in ifile:
                line = line.strip()
                if not line:
                    continue

                data = json.loads(line)
                self.full_data.append(data)

        self._refresh_ui()

    def do_filter(self):
        self.display_data.clear()
        log_filter = self.ui.lineEdit.text()
        logger.info(f'do filter with {log_filter}')
        if log_filter:
            for item in self.full_data:
                if not eval(log_filter):
                    continue
                data = json.dumps(item, ensure_ascii=False, sort_keys=True)
                self.display_data.append(data)
        else:
            for item in self.full_data:
                data = json.dumps(item, ensure_ascii=False, sort_keys=True)
                self.display_data.append(data)

        self._refresh_list()

    # noinspection PyUnusedLocal
    def select_log(self, current: QModelIndex, previous: QModelIndex):
        data = self.display_data[current.row()]
        obj = json.loads(data)
        self.ui.detailView.setPlainText(json.dumps(obj, ensure_ascii=True, sort_keys=True, indent=4))

    def _refresh_ui(self):
        self.do_filter()
        self.ui.detailView.clear()

    def _refresh_list(self):
        self.list_model.setStringList(self.display_data)
        self.ui.listView.setModel(self.list_model)
        self.ui.listView.scrollToTop()
        self.ui.detailView.clear()


def main():
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.showMaximized()
    widget.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
