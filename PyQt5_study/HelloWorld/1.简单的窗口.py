import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    # 创建一个应用
    app = QApplication(sys.argv)
    # 在这个应用下创建一个窗口
    w = QWidget()
    # 重新设置大小
    w.resize(500, 150)
    # 移动距离
    w.move(100, 100)
    # 设置标题
    w.setWindowTitle("FirstApp")
    # 显示窗口
    w.show()
    # 将app的退出信号传给程序进程，让程序进程退出
    sys.exit(app.exec_())
