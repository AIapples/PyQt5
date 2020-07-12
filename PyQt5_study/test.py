import sys
import re
import pandas as pd
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QPushButton, QFileDialog, QLineEdit,\
    QHBoxLayout, QMessageBox


class FileDeal(QWidget):
    def __init__(self):
        super().__init__()
        self.filepath_line_edit = QLineEdit()
        self.export_button = QPushButton("导出")
        self.import_button = QPushButton("导入")
        self.init_ui()
        # 点击事件
        self.import_button.clicked.connect(self.connect_file)

    def init_ui(self):
        self.resize(600, 100)
        self.center()
        # 内部布局
        self.layout_ui()

        self.setWindowTitle("平台分摊金额处理")
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def layout_ui(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(30, 0, 30, 0)
        hbox.addWidget(self.filepath_line_edit)
        hbox.addWidget(self.import_button)
        hbox.addWidget(self.export_button)
        self.setLayout(hbox)

    def connect_file(self):
        get_filename_path, ok = QFileDialog.getOpenFileName(self, "选取单个文件", "C:/")
        if ok:
            self.filepath_line_edit.setText(str(get_filename_path))
            try:
                self.export_button.clicked.connect(lambda: self.export_file(str(get_filename_path), "成功"))
            except Exception as e:
                self.export_button.clicked.connect(lambda: self.export_file(str(get_filename_path), "失败，未知原因。"))
        else:
            self.export_button.clicked.connect(lambda: self.export_file(None, "失败，未导入文件。"))

    def prompt_box(self, is_success):
        # 提示导出成功
        reply = QMessageBox.question(self, "Message", "导出{}, 是否退出？".format(is_success), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()
        elif reply == QMessageBox.No:
            pass

    def export_file(self, file_path, is_success):
        if file_path:
            df_obj = pd.read_excel(file_path, index=None)
            data = df_obj['优惠明细（A表示含有订单优惠，B表示只有单品优惠，C表示无优惠）']
            add_list = []
            # 【平台分摊金额:75.00】 【平台分摊金额:6.60】【平台分摊金额:12.00】
            for line in data:
                if '平台分摊金额' in str(line):
                    platform_divide = re.findall(r'【平台分摊金额:(\d+\.\d*)】', line)
                    if not platform_divide:
                        add_list.append(0)
                    else:
                        if len(platform_divide) == 1:
                            add_list.append(float(platform_divide[0]))
                        else:
                            add_list.append(platform_divide)
                else:
                    add_list.append(0)
            df_obj['平台分摊金额'] = add_list
            new_filepath = file_path.replace(".xls", "-new.xls")
            df_obj.to_excel(new_filepath, index=None)
        self.prompt_box(is_success)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fileDeal = FileDeal()
    sys.exit(app.exec_())


