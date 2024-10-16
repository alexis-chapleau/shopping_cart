from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
    QPushButton, QLabel, QListWidgetItem, QMessageBox, QSplitter, QMenu
)
from PyQt5.QtCore import Qt
from shopping_cart.models.shopping_cart import ShoppingCart
from shopping_cart.models.item import Item
from ui.item_creator import ItemCreatorDialog
from ui.receipt_viewer import ReceiptViewerDialog


class MainWindow(QMainWindow):
    """Main window for the Shopping Cart application."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shopping Cart")
        self.setGeometry(100, 100, 1000, 600)  # Increased width for better layout

        self.cart = ShoppingCart()
        self.items = []  # Available items to add to the cart

        self._setup_ui()
        self._load_initial_items()  # Load initial items

    def _setup_ui(self):
        # Main layout
        main_layout = QHBoxLayout()

        # Item list widget
        self.item_list_widget = QListWidget()
        self.item_list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.item_list_widget.setDragEnabled(True)
        self.item_list_widget.viewport().setAcceptDrops(True)
        self.item_list_widget.setDragDropMode(QListWidget.DragOnly)

        # Cart list widget
        self.cart_list_widget = QListWidget()
        self.cart_list_widget.setAcceptDrops(True)
        self.cart_list_widget.setDragEnabled(False)
        self.cart_list_widget.setDragDropMode(QListWidget.DropOnly)
        self.cart_list_widget.setSpacing(5)

        # Connect drag and drop signals
        self.cart_list_widget.dragEnterEvent = self.drag_enter_event
        self.cart_list_widget.dropEvent = self.drop_event

        # Enable context menu for cart list
        self.cart_list_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.cart_list_widget.customContextMenuRequested.connect(self.show_cart_context_menu)

        # Side menu with cart info
        cart_info_layout = QVBoxLayout()
        self.total_quantity_label = QLabel("Total Quantity: 0")
        self.total_price_label = QLabel("Total Price: $0.00")
        cart_info_layout.addWidget(self.total_quantity_label)
        cart_info_layout.addWidget(self.total_price_label)

        self.generate_receipt_button = QPushButton("Generate Receipt")
        self.generate_receipt_button.clicked.connect(self.generate_receipt)
        cart_info_layout.addWidget(self.generate_receipt_button)

        # Buttons
        button_layout = QHBoxLayout()
        self.add_item_button = QPushButton("Create Item")
        self.add_item_button.clicked.connect(self.create_item)
        button_layout.addWidget(self.add_item_button)

        # Legend
        legend_label = QLabel("Legend:")
        legend_label.setStyleSheet("font-weight: bold;")
        drag_drop_label = QLabel("• Drag and drop items to add them to your shopping cart.")
        remove_label = QLabel("• Right-click on an item in the cart to remove it.")
        legend_layout = QVBoxLayout()
        legend_layout.addWidget(legend_label)
        legend_layout.addWidget(drag_drop_label)
        legend_layout.addWidget(remove_label)

        # Assemble layouts
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Available Items"))
        left_layout.addWidget(self.item_list_widget)
        left_layout.addLayout(button_layout)
        left_layout.addSpacing(20)
        left_layout.addLayout(legend_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Shopping Cart"))
        right_layout.addWidget(self.cart_list_widget)
        right_layout.addLayout(cart_info_layout)

        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)

        main_widget = QWidget()
        main_layout.addWidget(splitter)
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def _load_initial_items(self):
        # Predefined list of items
        initial_items = [
            {'name': 'Apple', 'price': 1.00},
            {'name': 'Banana', 'price': 0.50},
            {'name': 'Orange', 'price': 0.75},
            {'name': 'Milk', 'price': 2.50},
            {'name': 'Bread', 'price': 1.50},
            {'name': 'Eggs (Dozen)', 'price': 3.00},
            {'name': 'Cheese', 'price': 4.00},
            {'name': 'Chocolate', 'price': 2.25},
            {'name': 'Coffee', 'price': 5.00},
            {'name': 'Tea', 'price': 4.50},
            {'name': 'Chicken Breast', 'price': 7.50},
            {'name': 'Salmon Fillet', 'price': 9.00},
            {'name': 'Rice (1kg)', 'price': 1.80},
            {'name': 'Pasta', 'price': 1.20},
            {'name': 'Tomato Sauce', 'price': 1.00},
            {'name': 'Lettuce', 'price': 0.90},
            {'name': 'Carrots (1kg)', 'price': 1.10},
            {'name': 'Potatoes (1kg)', 'price': 0.80},
            {'name': 'Yogurt', 'price': 2.00},
            {'name': 'Cereal', 'price': 3.50},
        ]
        for item_data in initial_items:
            self.items.append(item_data)
            self.add_item_to_list(item_data)

    def create_item(self):
        dialog = ItemCreatorDialog(self)
        if dialog.exec_():
            item_data = dialog.get_item_data()
            self.items.append(item_data)
            self.add_item_to_list(item_data)

    def add_item_to_list(self, item_data):
        item_widget = QListWidgetItem(f"{item_data['name']} - ${item_data['price']:.2f}")
        item_widget.setData(Qt.UserRole, item_data)
        self.item_list_widget.addItem(item_widget)

    def drag_enter_event(self, event):
        event.accept()

    def drop_event(self, event):
        source_item = event.source().currentItem()
        if source_item:
            item_data = source_item.data(Qt.UserRole)
            # Create a new Item instance with a unique UID
            item = Item(name=item_data['name'], price=item_data['price'])
            self.cart.add_item(item)
            self.update_cart()
            self.update_cart_info()
        event.accept()

    def update_cart(self):
        self.cart_list_widget.clear()
        for item_name, item_group in self.cart.list_items().items():
            for item in item_group['instances']:
                item_widget = QListWidgetItem(f"{item.name} - ${item.price:.2f}")
                item_widget.setData(Qt.UserRole, item)
                # Center-align the text
                item_widget.setTextAlignment(Qt.AlignCenter)
                self.cart_list_widget.addItem(item_widget)

    def update_cart_info(self):
        self.total_quantity_label.setText(f"Total Quantity: {self.cart.total_quantity}")
        self.total_price_label.setText(f"Total Price: ${self.cart.total_price:.2f}")

    def generate_receipt(self):
        if self.cart.total_quantity == 0:
            QMessageBox.warning(self, "Empty Cart", "Your cart is empty.")
            return

        # For simplicity, we'll generate a receipt in text format
        receipt_content = self.cart.generate_receipt(format_type='text')
        dialog = ReceiptViewerDialog(receipt_content, self)
        dialog.resize(600, 800)  # Ensure the receipt window is larger by default
        dialog.exec_()

    def show_cart_context_menu(self, position):
        menu = QMenu()
        remove_action = menu.addAction("Remove Item")
        action = menu.exec_(self.cart_list_widget.viewport().mapToGlobal(position))
        if action == remove_action:
            selected_item = self.cart_list_widget.itemAt(position)
            if selected_item:
                item = selected_item.data(Qt.UserRole)
                self.cart.remove_item(item)
                self.update_cart()
                self.update_cart_info()
