1. 通过命令分别在cmd中进行安装

   `pip install PyQt5`

   `pip install PyQt5-tools`

2. 双击`designer.exe`（默认目录：`...\Lib\site-packages\qt5_applications\Qt\bin`）进行编辑并保存。保存后文件为：.ui 文件

3. 通过命令 将testui.ui 转换成testui.py
   `pyuic5.exe testui.ui -o testui.py`
   `pyuic5.exe .\src\interface\imeui.ui -o .\src\interface\imeui.py`

4. 打开转换成的`testui.py` 在文件末尾加入代码：

   ```python
   if __name__ == '__main__':
       app = QtWidgets.QApplication(sys.argv)
       mainWindow = QtWidgets.QMainWindow()
       ui = Ui_MainWindow()
       ui.setupUi(mainWindow)
       mainWindow.show()
       sys.exit(app.exec_())
   ```

   

