# ПАРОЛЬ ДЛЯ БАЗЫ ДАННЫХ SUPABASE "SKLAD" - xUoCUJUHhsclS1YM

import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog, QGridLayout, QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox, QComboBox
from supabase import Client, create_client

# Подключение к базе данных Supabase
print("Подключение к базе данных Supabase...")
url: str = "https://tengeuuasogbhjswdqsw.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlbmdldXVhc29nYmhqc3dkcXN3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMzI1ODEzMiwiZXhwIjoyMDI4ODM0MTMyfQ.IZqo8V-91Gj3yZ_HEnXZCzlCuu8VxhxXu52BZwdVGxw"
try:
    supabase = create_client(url, key)
except Exception as e:
    print(f"[ERROR] Ошибка подключения к базе данных\n{e}")
    sys.exit()

# Главное окно управления складом
class StorageWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Storage control")

        layout = QGridLayout(self)

        # Кнопка "Обновить"
        self.refresh_button = QPushButton(self)
        self.refresh_button.setStyleSheet("font-size: 14px; background-color: #43a4e6; color: white;")
        self.refresh_button.setText("Обновить")
        self.refresh_button.clicked.connect(self.refresh)
        layout.addWidget(self.refresh_button, 0, 0)

        # Кнопка "Сохранить"
        self.save_button = QPushButton(self)
        self.save_button.setStyleSheet("font-size: 14px; background-color: #66de70; color: white;")
        self.save_button.setText("Сохранить")
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button, 2, 0)

        # Кнопка "Добавить"
        self.add_button = QPushButton(self)
        self.add_button.setStyleSheet("font-size: 14px; background-color: #66de70; color: white;")
        self.add_button.setText("Добавить")
        self.add_button.clicked.connect(self.add)
        layout.addWidget(self.add_button, 0, 1)

        # Кнопка "Удалить"
        self.remove_button = QPushButton(self)
        self.remove_button.setStyleSheet("font-size: 14px; background-color: #cf392b; color: white;")
        self.remove_button.setText("Удалить")
        self.remove_button.clicked.connect(self.remove)
        layout.addWidget(self.remove_button, 1, 1)

        # Таблица базы данных
        self.table = QTableWidget(self)
        self.table.setColumnCount(6) # Количество столбцов
        self.table.setRowCount(1) # Количество строк
        self.table.setHorizontalHeaderLabels(["id", "Наименование товара", "Количество", "Тип кол-ва", "Поставщик", "Последняя поставка"]) # Заголовки столбцов
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(4, 140)
        self.table.setColumnWidth(5, 150)
        layout.addWidget(self.table, 1, 0)

        self.resize(1000, 800)

        # AFTER INIT
        self.refresh()

    # Обновление данных
    def refresh(self):
        res = supabase.table("storage").select("*").order("id", desc=True).execute()
        data = res.data
        count = len(data)

        if count != 0:
            self.table.setRowCount(0)

            i = 0
            for row in data:
                res = supabase.table("delivers").select("name").eq("deliver_id", row["deliver_id"]).execute()
                deliver_name = res.data[0]["name"]

                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(str(row["id"])))
                self.table.setItem(i, 1, QTableWidgetItem(str(row["name"])))
                self.table.setItem(i, 2, QTableWidgetItem(str(row["count"])))
                self.table.setItem(i, 3, QTableWidgetItem(str(row["type_of_count"])))
                self.table.setItem(i, 4, QTableWidgetItem(str(deliver_name)))
                self.table.setItem(i, 5, QTableWidgetItem(str(row["last_delivery"])))
            
        else:
            print("No data")
    
    def add(self):
        dlg = AddDialog(self)
        if dlg.exec():
            print("Добавление товара выполенено!")
        else:
            print("Отмена добавления!")

    def remove(self):
        dlg = RemoveDialog(self)
        if dlg.exec():
            print("Удаление товара выполенено!")
        else:
            print("Отмена удаления!")

    def save(self):
        pass


class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавление товара")

        self.layout = QVBoxLayout()

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.save_click)
        self.buttonBox.rejected.connect(self.cancel_click)

        self.title = QLabel("Введите информацию о товаре")
        self.title.setStyleSheet("font-size: 16px;")
        self.layout.addWidget(self.title)

        self.name_label = QLabel("Наименование товара:")
        self.layout.addWidget(self.name_label)
        self.name_box = QLineEdit()
        self.layout.addWidget(self.name_box)

        self.count_label = QLabel("Текущее количество:")
        self.layout.addWidget(self.count_label)
        self.count_box = QLineEdit()
        self.layout.addWidget(self.count_box)

        self.type_of_count_label = QLabel("Тип количества:")
        self.layout.addWidget(self.type_of_count_label)
        # self.type_of_count_box = QLineEdit()
        self.type_of_count_box = QComboBox()
        self.type_of_count_box.addItem('шт')
        self.type_of_count_box.addItem('кг')
        self.layout.addWidget(self.type_of_count_box)

        self.deliver_label = QLabel("Поставщик (полностью точное имя):")
        self.layout.addWidget(self.deliver_label)
        # self.deliver_box = QLineEdit()
        self.deliver_box = QComboBox()

        res = supabase.table("delivers").select("name").execute()
        data = res.data
        # delivers = list()
        for row in data:
            # delivers.append(row["name"])
            self.deliver_box.addItem(row["name"])

        self.layout.addWidget(self.deliver_box)

        self.last_delivery_label = QLabel("Дата последней поставки (в формате ГГГГ:ММ:ДД):")
        self.layout.addWidget(self.last_delivery_label)
        self.last_delivery_box = QLineEdit()
        self.layout.addWidget(self.last_delivery_box)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def save_click(self):
        deliver = self.deliver_box.currentText()
        res = supabase.table("delivers").select("deliver_id").eq("name", deliver).execute()
        data = res.data
        count = len(data)

        if count != 0:
            id = data[0]["deliver_id"]

            supabase.table("storage").insert(
                {
                    "name": self.name_box.text(),
                    "count": self.count_box.text(),
                    "type_of_count": self.type_of_count_box.currentText(),
                    "deliver_id": id,
                    "last_delivery": self.last_delivery_box.text()
                }
            ).execute()

            self.accept()
        else:
            print("Неправильно введён поставщик!")

    
    def cancel_click(self):
        self.reject()

class RemoveDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавление товара")

        self.layout = QVBoxLayout()

        QBtn = QDialogButtonBox.Yes | QDialogButtonBox.No
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.yes_click)
        self.buttonBox.rejected.connect(self.no_click)

        self.title = QLabel("Вы уверены, что хотите\nудалить выбранный продукт?")
        self.title.setStyleSheet("font-size: 16px;")

        self.layout.addWidget(self.title)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def yes_click(self):
        self.accept()
    
    def no_click(self):
        self.reject()

def main():
    app = QApplication(sys.argv)
    w = StorageWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()