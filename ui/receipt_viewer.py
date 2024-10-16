from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton

class ReceiptViewerDialog(QDialog):
    """Dialog to display the generated receipt."""

    def __init__(self, receipt_content, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Receipt")
        self.receipt_content = receipt_content
        self.resize(600, 800)  # Set larger default size
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setText(self.receipt_content)
        layout.addWidget(self.text_edit)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.accept)
        layout.addWidget(self.close_button)

        self.setLayout(layout)
