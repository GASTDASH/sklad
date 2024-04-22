# ПАРОЛЬ ДЛЯ БАЗЫ ДАННЫХ SUPABASE "SKLAD" - xUoCUJUHhsclS1YM

import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QLineEdit,
    QPushButton,
    QLabel,
    QFileDialog,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QDialog, 
    QDialogButtonBox,
    QComboBox,
    QAbstractItemView,
    QCheckBox
)
from supabase import Client, create_client
from product import Product

# Подключение к базе данных Supabase
def connect():
    print("Подключение к базе данных Supabase...")
    url: str = "https://tengeuuasogbhjswdqsw.supabase.co"
    key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRlbmdldXVhc29nYmhqc3dkcXN3Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxMzI1ODEzMiwiZXhwIjoyMDI4ODM0MTMyfQ.IZqo8V-91Gj3yZ_HEnXZCzlCuu8VxhxXu52BZwdVGxw"
    try:
        supabase = create_client(url, key)
    except Exception as e:
        print(f"[ERROR] Ошибка подключения к базе данных\n{e}")
        sys.exit()

    return supabase

supabase = connect()

# Главное окно управления складом
class StorageWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.set_ui()

        self.refresh()

    def set_ui(self):
        self.setWindowTitle("Управление складом")

        layout = QGridLayout(self)

        self.search_text = QLabel(text="Введите запрос:")
        layout.addWidget(self.search_text, 0, 0)

        # Поле поиска
        self.search_box = QLineEdit()
        self.search_box.setFixedSize(300, 30)
        layout.addWidget(self.search_box, 1, 0)

        # # Кнопка поиска
        # self.search_button = QPushButton(text="Найти")
        # self.search_button.setFixedSize(300, 30)
        # layout.addWidget(self.search_button, 1, 0)

        # Кнопка "Обновить"
        self.refresh_button = QPushButton(self)
        self.refresh_button.setStyleSheet("font-size: 14px; background-color: #43a4e6; color: white;")
        self.refresh_button.setText("Найти")
        self.refresh_button.setFixedSize(300, 30)
        self.refresh_button.clicked.connect(self.refresh)
        layout.addWidget(self.refresh_button, 2, 0)

        # Кнопка "Добавить"
        self.add_button = QPushButton(self)
        self.add_button.setStyleSheet("font-size: 14px; background-color: #66de70; color: white;")
        self.add_button.setText("Добавить")
        self.add_button.clicked.connect(self.add)
        layout.addWidget(self.add_button, 0, 1)

        # Кнопка "Изменить"
        self.edit_button = QPushButton(self)
        self.edit_button.setStyleSheet("font-size: 14px; background-color: #43a4e6; color: white;")
        self.edit_button.setText("Изменить")
        self.edit_button.clicked.connect(self.edit)
        layout.addWidget(self.edit_button, 1, 1)

        # Кнопка "Удалить"
        self.remove_button = QPushButton(self)
        self.remove_button.setStyleSheet("font-size: 14px; background-color: #cf392b; color: white;")
        self.remove_button.setText("Удалить")
        self.remove_button.clicked.connect(self.remove)
        layout.addWidget(self.remove_button, 2, 1)

        # Кнопка "+1"
        self.plus_1_button = QPushButton(self)
        self.plus_1_button.setStyleSheet("font-size: 14px; background-color: #3a64f0; color: white;")
        self.plus_1_button.setText("+1")
        self.plus_1_button.clicked.connect(self.plus_1)
        layout.addWidget(self.plus_1_button, 4, 1)

        # Кнопка "-1"
        self.minus_1_button = QPushButton(self)
        self.minus_1_button.setStyleSheet("font-size: 14px; background-color: #3a64f0; color: white;")
        self.minus_1_button.setText("-1")
        self.minus_1_button.clicked.connect(self.minus_1)
        layout.addWidget(self.minus_1_button, 5, 1)

        # Таблица базы данных
        self.table = QTableWidget(self)
        self.table.setColumnCount(6) # Количество столбцов
        self.table.setRowCount(1) # Количество строк
        self.table.setHorizontalHeaderLabels(["id", "Наименование товара", "Количество", "Тип кол-ва", "Поставщик", "Последняя поставка"]) # Заголовки столбцов
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(4, 140)
        self.table.setColumnWidth(5, 150)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.table, 3, 0)

        self.resize(1000, 800)

    # Поиск данных
    def search(self, q: str):
        if q == "*":
            res = supabase.table("storage").select("*").order("id", desc=True).execute()
        else:
            res = supabase.table("storage").select("*").like("name", f"%{q}%").order("id", desc=True).execute()
        data = res.data
        count = len(data)
        return data,count

    # Обновление данных
    def refresh(self):
        if self.search_box.text().strip() == "" or self.search_box.text().strip() == "*":
            data, count = self.search(q = "*")
        else:
            data, count = self.search(q = self.search_box.text().strip())

        self.table.setRowCount(0)
        if count != 0:
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
    
    # Добавление записи
    def add(self):
        dlg = AddDialog(self)
        if dlg.exec():
            print("Добавление товара выполенено!")
            self.refresh()
        else:
            print("Отмена добавления!")

    # Удаление записи
    def remove(self):
        # index = self.table.currentRow()
        # print(f"index = {index}")
        # print(f"item value = {self.table.item(index, 0).text()}")
        id = self.get_selected_id()
        dlg = RemoveDialog(self)
        if dlg.exec():
            supabase.table("storage").delete().eq("id", id).execute()
            print("Удаление товара выполенено!")
            self.refresh()
        else:
            print("Отмена удаления!")

    # Редактирование записи
    def edit(self):
        index = self.table.currentRow()
        id = self.table.item(index, 0).text()

        res = supabase.table("delivers").select("deliver_id").eq("name", self.table.item(index, 4).text()).execute()
        data = res.data
        deliver_id = data[0]["deliver_id"]
        print(f"[DEBUG] deliver_id = {deliver_id}")

        product = Product()
        product.name = self.table.item(index, 1).text(),
        product.count = int(self.table.item(index, 2).text()),
        product.type_of_count = self.table.item(index, 3).text(),
        product.deliver_id = deliver_id,
        product.last_delivery = self.table.item(index, 5).text()
        dlg = EditDialog(self, id, product)
        if dlg.exec():
            print("Изменение товара выполенено!")
            self.refresh()
        else:
            print("Отмена изменения!")

    # +1
    def plus_1(self):
        id = self.get_selected_id()
        res = supabase.table("storage").select("count").eq("id", id).execute()
        count = int(res.data[0]["count"])
        supabase.table("storage").update(
            {
                "count": count + 1
            }
        ).eq("id", id).execute()

    # -1
    def minus_1(self):
        id = self.get_selected_id()
        res = supabase.table("storage").select("count").eq("id", id).execute()
        count = int(res.data[0]["count"])
        supabase.table("storage").update(
            {
                "count": count - 1
            }
        ).eq("id", id).execute()

    # Получение id выбранного продукта
    def get_selected_id(self):
        index = self.table.currentRow()
        return self.table.item(index, 0).text()

# Окно добавления записи
class AddDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.set_ui()

    def set_ui(self):
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

# Окно редактирования записи
class EditDialog(QDialog):
    old_product = Product()

    def __init__(
            self,
            parent,
            id: int,
            old_product: Product
        ):
        super().__init__(parent)

        self.id = id
        self.old_product = old_product

        self.setWindowTitle("Изменение товара")

        self.layout = QVBoxLayout()

        QBtn = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.save_click)
        self.buttonBox.rejected.connect(self.cancel_click)

        self.title = QLabel("Информация о товаре")
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
        self.deliver_box = QComboBox()

        res = supabase.table("delivers").select("name").execute()
        data = res.data
        for row in data:
            self.deliver_box.addItem(row["name"])

        self.layout.addWidget(self.deliver_box)

        self.last_delivery_label = QLabel("Дата последней поставки (в формате ГГГГ:ММ:ДД):")
        self.layout.addWidget(self.last_delivery_label)
        self.last_delivery_box = QLineEdit()
        self.layout.addWidget(self.last_delivery_box)

        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.show_info()

    def show_info(self):
        res = supabase.table("delivers").select("name").eq("deliver_id", self.old_product.deliver_id[0]).execute()
        data = res.data
        deliver_name = data[0]["name"]

        self.name_box.setText(self.old_product.name[0])
        self.count_box.setText(str(self.old_product.count[0]))
        self.type_of_count_box.setCurrentText(str(self.old_product.type_of_count[0]))
        self.deliver_box.setCurrentText(str(deliver_name))
        self.last_delivery_box.setText(self.old_product.last_delivery)

    def save_click(self):
        res = supabase.table("delivers").select("deliver_id").eq("name", self.deliver_box.currentText()).execute()
        data = res.data
        deliver_id = data[0]["deliver_id"]
        
        supabase.table("storage").update(
            {
                "name": self.name_box.text(),
                "count": self.count_box.text(),
                "type_of_count": self.type_of_count_box.currentText(),
                "deliver_id": deliver_id,
                "last_delivery": self.last_delivery_box.text()
            }
        ).eq("id", self.id).execute()

        self.accept()
    
    def cancel_click(self):
        self.reject()

# Окно удаление записи
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