from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)

class ItemCreatorDialog(QDialog):
    """Dialog to create a new item template."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Item")
        self.item_data = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        # Item name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Item Name:"))
        self.name_input = QLineEdit()
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Item price input
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("Item Price:"))
        self.price_input = QLineEdit()
        price_layout.addWidget(self.price_input)
        layout.addLayout(price_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.create_item)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def create_item(self):
        name = self.name_input.text().strip()
        price_text = self.price_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Item name cannot be empty.")
            return
        try:
            price = float(price_text)
            if price <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid price. Please enter a positive number.")
            return

        self.item_data = {'name': name, 'price': price}
        self.accept()

    def get_item_data(self):
        return self.item_data
