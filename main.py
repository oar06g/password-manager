from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
import sys
from ui_interface import Ui_MainWindow
import sqlite3
import os
from func import encrypt, decrypt

SECRET_KEY = "4Ufou1tPuzl0tp2jWfiqI-3jn79lSjx10PPxOQHzasM="


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        if not os.path.exists("dbs"):
            os.makedirs("dbs")

        self.connection = sqlite3.connect(os.path.join("dbs", "sqlite.db"))
        self.cursor = self.connection.cursor()
        self.init_db()

        self.ui.loginBtn.clicked.connect(self.login)
        self.ui.addBtn.clicked.connect(self.add_info)
        self.ui.deleteBtn.clicked.connect(self.delete_row)
        self.ui.updateBtn.clicked.connect(self.update_row)
        self.ui.tableInfo.itemSelectionChanged.connect(self.display_selected_row)

        self.selected_row_id = None

    def init_db(self):
        connection = sqlite3.connect(os.path.join("dbs", "sqlite.db"))
        cursor = connection.cursor()

        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            password TEXT
        );"""
        )
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS info (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            sitename TEXT,
            username TEXT,
            password TEXT,
            email TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );"""
        )
        connection.commit()

        cursor.execute("INSERT INTO users (id, password) VALUES (1, 'haIrySECKw');")
        connection.commit()

        connection.close()

    def login(self):
        password = self.ui.input_password.text()
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
        result = self.cursor.fetchone()

        if result and password == result[1]:
            self.switch(self.ui.homePage)
            self.load_data()
        else:
            self.ui.errorlabel.setText("The password is incorrect.")

    def switch(self, widget_page):
        self.ui.stackedWidget.setCurrentWidget(widget_page)

    def add_info(self):
        _sitename = self.ui.sitename_input.text()
        _username = self.ui.username_input.text()
        _password = self.ui.password_input.text()
        _email = self.ui.email_input.text()

        _e_sitename = encrypt(_sitename, SECRET_KEY)
        _e_username = encrypt(_username, SECRET_KEY)
        _e_password = encrypt(_password, SECRET_KEY)
        _e_email = encrypt(_email, SECRET_KEY)

        self.cursor.execute(
            "INSERT INTO info (user_id, sitename, username, password, email) VALUES (?, ?, ?, ?, ?);",
            (1, _e_sitename, _e_username, _e_password, _e_email),
        )
        self.connection.commit()

        self.ui.sitename_input.clear()
        self.ui.username_input.clear()
        self.ui.password_input.clear()
        self.ui.email_input.clear()
        self.load_data()

    def load_data(self):
        query = "SELECT id, sitename, username, password, email FROM info"
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.ui.tableInfo.setRowCount(len(data))
        self.ui.tableInfo.setColumnCount(4)
        self.row_ids = {}

        for row_index, row_data in enumerate(data):
            self.row_ids[row_index] = row_data[0]
            decrypted_row = [
                decrypt(row_data[1], SECRET_KEY),
                decrypt(row_data[2], SECRET_KEY),
                decrypt(row_data[3], SECRET_KEY),
                decrypt(row_data[4], SECRET_KEY),
            ]
            for column_index, cell_data in enumerate(decrypted_row):
                self.ui.tableInfo.setItem(
                    row_index, column_index, QTableWidgetItem(str(cell_data))
                )

    def display_selected_row(self):
        selected_row = self.ui.tableInfo.currentRow()
        if selected_row == -1:
            return

        sitename = self.ui.tableInfo.item(selected_row, 0).text()
        username = self.ui.tableInfo.item(selected_row, 1).text()
        password = self.ui.tableInfo.item(selected_row, 2).text()
        email = self.ui.tableInfo.item(selected_row, 3).text()

        self.ui.sitename_input.setText(sitename)
        self.ui.username_input.setText(username)
        self.ui.password_input.setText(password)
        self.ui.email_input.setText(email)

        self.selected_row_id = self.row_ids.get(selected_row)

    def update_row(self):
        if self.selected_row_id is None:
            self.ui.errorlabel.setText("No row selected for update!")
            return

        sitename = self.ui.sitename_input.text()
        username = self.ui.username_input.text()
        password = self.ui.password_input.text()
        email = self.ui.email_input.text()

        update_query = """
            UPDATE info
            SET sitename = ?, username = ?, password = ?, email = ?
            WHERE id = ?
        """
        self.cursor.execute(
            update_query, (sitename, username, password, email, self.selected_row_id)
        )
        self.connection.commit()

        self.load_data()
        self.ui.errorlabel.setText(
            f"Row with ID {self.selected_row_id} updated successfully!"
        )

    def delete_row(self):
        selected_row = self.ui.tableInfo.currentRow()
        if selected_row == -1:
            self.ui.errorlabel.setText("No row selected!")
            return

        row_id = self.row_ids.get(selected_row)
        if row_id is None:
            self.ui.errorlabel.setText("Row ID not found!")
            return

        self.cursor.execute("DELETE FROM info WHERE id = ?", (row_id,))
        self.connection.commit()
        self.load_data()

        self.ui.errorlabel.setText(f"Row with ID {row_id} deleted successfully!")

    def closeEvent(self, event):
        self.cursor.close()
        self.connection.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
