import sys
from typing import List

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


def show_error(window, messages: List[str]):
    dialog = QDialog(window)
    dialog.setWindowTitle("Error | ElecCalc")
    dialog.setModal(True)

    layout = QVBoxLayout(dialog)
    for message in messages:
        label = QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)

    # Automatically resize to fit content
    dialog.adjustSize()

    # Optional: limit maximum height to avoid huge dialogs
    screen_height = QApplication.primaryScreen().availableGeometry().height()
    if dialog.height() > screen_height * 0.8:  # max 80% of screen
        dialog.setFixedHeight(int(screen_height * 0.8))

    dialog.exec()


def show_solution(window, solution: List[float]):
    """Show solution in a dialog"""
    dialog = QDialog(window)
    dialog.setWindowTitle("Solution | ElecCalc")
    dialog.setModal(True)

    layout = QVBoxLayout(dialog)

    # Title label
    title = QLabel("Solution:")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)

    # Create table to display solution
    table = QTableWidget(len(solution), 2)
    table.setHorizontalHeaderLabels(["Variable", "Value"])
    table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # No editing

    # Populate table
    for i, value in enumerate(solution):
        # Variable name (v1, v2, v3, etc.)
        var_item = QTableWidgetItem(f"v{i + 1}")
        var_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        table.setItem(i, 0, var_item)

        # Value
        val_item = QTableWidgetItem(f"{value:.6f}")
        val_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        table.setItem(i, 1, val_item)

    # Auto-size columns
    table.resizeColumnsToContents()

    # Set minimum column widths for readability
    metrics = QFontMetrics(table.font())
    min_width = metrics.horizontalAdvance("Variable") + 20
    table.setColumnWidth(0, max(table.columnWidth(0), min_width))

    value_width = metrics.horizontalAdvance("0.000000") + 30
    table.setColumnWidth(1, max(table.columnWidth(1), value_width))

    # Calculate table size
    total_width = (
        table.verticalHeader().width()
        + table.columnWidth(0)
        + table.columnWidth(1)
        + table.frameWidth() * 2
    )
    total_height = (
        table.horizontalHeader().height()
        + sum(table.rowHeight(r) for r in range(table.rowCount()))
        + table.frameWidth() * 2
    )

    table.setFixedSize(total_width, total_height)
    layout.addWidget(table)

    # Buttons
    button_layout = QHBoxLayout()

    continue_btn = QPushButton("Continue")
    clear_btn = QPushButton("Clear")
    exit_btn = QPushButton("Exit")

    # Button actions
    continue_btn.clicked.connect(dialog.accept)  # Just close dialog
    clear_btn.clicked.connect(lambda: dialog.done(1))  # Return code 1 for clear
    exit_btn.clicked.connect(lambda: dialog.done(2))  # Return code 2 for exit

    button_layout.addWidget(continue_btn)
    button_layout.addWidget(clear_btn)
    button_layout.addWidget(exit_btn)

    layout.addLayout(button_layout)

    # Size dialog to fit content
    dialog.adjustSize()
    dialog.setFixedSize(dialog.size())

    # Show dialog and get result
    result = dialog.exec()
    return result


class Setup(QWidget):
    def __init__(self):
        super().__init__()
        self.button = None
        self.label = None
        self.height_box = None
        self.width_box = None
        self.main = None
        self.setWindowTitle("Setup | ElecCalc")
        self.hasContextWindow = False
        self.init_ui()
        self.setFixedSize(300, 100)

    def init_ui(self):
        """Setup UI initialization"""
        self.width_box = QLineEdit()
        self.height_box = QLineEdit()
        for box in (self.width_box, self.height_box):
            box.setMaxLength(2)

        # autofit 2 characters
        size = QFontMetrics(self.width_box.font())
        char_width = size.horizontalAdvance("0" * 2) + 20
        self.width_box.setFixedWidth(char_width)
        self.height_box.setFixedWidth(char_width)

        self.label = QLabel("*")
        label = QFontMetrics(self.label.font())
        label_width = label.horizontalAdvance("0") + 10
        self.label.setFixedWidth(label_width)

        # Layout grid
        hbox = QHBoxLayout()
        hbox.addWidget(self.width_box)
        hbox.addWidget(self.label)
        hbox.addWidget(self.height_box)

        self.button = QPushButton("Continue")
        self.button.clicked.connect(self.calculate)

        # Layout grid for everything
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.button)
        vbox.setAlignment(
            self.button, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        self.setLayout(vbox)

    def calculate(self):
        # print(self.width_box.text(), self.height_box.text())
        dimensions = {"width": self.width_box.text(), "height": self.height_box.text()}
        width = None
        height = None

        try:
            for name, value in dimensions.items():
                number = int(value)
                if name == "width":
                    width = number
                else:
                    height = number
            if width and height:
                self.main = MainWindow(width, height)
                self.main.show()
                self.close()

        except Exception:
            errored_out = []
            for name, value in dimensions.items():
                try:
                    int(value)
                except Exception:
                    errored_out.append(name)
                    print(f"Error: '{name}' has invalid input '{value}'")

            errors = []
            # Add error messages to the dialog
            if errored_out:
                for name in errored_out:
                    errors.append(f"'{name}' has invalid input: '{dimensions[name]}'")

            else:
                errors.append("Unknown error occurred.")
            show_error(self, errors)

            return


class MainWindow(QMainWindow):
    def __init__(self, matrix_rows: int, matrix_columns: int) -> None:
        super().__init__()
        self.layout = None
        self.clear_button = None
        self.matrix = None
        self.calculate_button = None
        self.label = None
        self.setWindowTitle("Home | ElecCalc")

        self.matrix_rows = matrix_rows
        self.matrix_columns = matrix_columns + 1  # Constants col

        # One central container for the whole window
        self.container = QWidget()
        self.setCentralWidget(self.container)

        # Build in logical order
        self.setup_table()
        self.setup_buttons()

        # Final layout assembly
        self.build_layout()

        # Auto-fit window to table
        self.resize_window_to_table()

    def setup_table(self):
        self.matrix = QTableWidget(self.matrix_rows, self.matrix_columns)
        labels = [f"v{i + 1}" for i in range(self.matrix_columns)]
        labels[-1] = "C"
        self.matrix.setHorizontalHeaderLabels(labels)

        self.label = QLabel("Ze Matrix")
        self.label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        )

        # Column sizing for 5 characters
        metrics = QFontMetrics(self.matrix.font())
        char_width = metrics.horizontalAdvance("0" * 5) + 12

        for c in range(self.matrix.columnCount()):
            self.matrix.setColumnWidth(c, char_width)

    def setup_buttons(self):
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clr)

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setCheckable(True)
        self.calculate_button.clicked.connect(self.calculate)

    def build_layout(self):
        """Assemble all widgets into the main layout"""
        self.layout = QVBoxLayout(self.container)  # pyright: ignore[reportAttributeAccessIssue]

        button_row = QHBoxLayout()
        button_row.addWidget(self.clear_button)
        button_row.addWidget(self.calculate_button)

        self.layout.addWidget(self.label)  # pyright: ignore[reportAttributeAccessIssue]
        self.layout.addWidget(self.matrix)  # pyright: ignore[reportAttributeAccessIssue]
        self.layout.addLayout(button_row)  # pyright: ignore[reportAttributeAccessIssue]

    def resize_window_to_table(self):
        """Resize window so the table fits exactly"""
        table = self.matrix

        total_width = (
            table.verticalHeader().width()
            + sum(table.columnWidth(c) for c in range(table.columnCount()))
            + table.frameWidth() * 2
        )

        total_height = (
            table.horizontalHeader().height()
            + sum(table.rowHeight(r) for r in range(table.rowCount()))
            + table.frameWidth() * 2
        )

        self.setFixedSize(total_width + 20, total_height + 80)

    def clr(self):
        for r in range(self.matrix.rowCount()):
            for c in range(self.matrix.columnCount()):
                item = self.matrix.item(r, c)
                if item is None:
                    # create it so we can clear it
                    item = QTableWidgetItem("")
                    self.matrix.setItem(r, c, item)
                else:
                    item.setText("")

    def calculate(self):
        errors = []
        for r in range(self.matrix.rowCount()):
            for c in range(self.matrix.columnCount()):
                qt_item = self.matrix.item(r, c)

                # No item or blank text
                if qt_item is None or not qt_item.text().strip():
                    errors.append(f"value at ({r}, {c}) not specified")
                else:
                    text = qt_item.text().strip()

                    # Check fraction
                    if "/" in text:
                        parts = text.split("/")
                        if len(parts) != 2:
                            errors.append(
                                f"Value at ({r + 1}, {c + 1}) is not a valid fraction"
                            )
                        numerator, denominator = parts
                        if (
                            not numerator.replace(".", "", 1)
                            .replace("-", "", 1)
                            .isdigit()
                            or not denominator.replace(".", "", 1)
                            .replace("-", "", 1)
                            .isdigit()
                        ):
                            errors.append(
                                f"Value at ({r + 1}, {c + 1}) is not a valid fraction"
                            )
                    else:
                        # Check decimal/integer
                        if not text.replace(".", "", 1).replace("-", "", 1).isdigit():
                            errors.append(
                                f"Value at ({r + 1}, {c + 1}) is not a valid number"
                            )
        if errors:
            show_error(self, errors)
        values = self.get_table_values()
        try:
            solution = self.calculate_matrix(
                [row[:-1] for row in values], [row[-1] for row in values]
            )
            result = show_solution(self, solution)
            if result == 1:
                self.clr()
            elif result == 2:
                QApplication.exit()
        except ValueError as e:
            show_error(self, [str(e)])

    def get_table_values(self):
        rows = self.matrix.rowCount()
        cols = self.matrix.columnCount()
        arr = []

        for r in range(rows):
            row_vals = []
            for c in range(cols):
                item = self.matrix.item(r, c)
                text = item.text().strip() if item else "0"

                # Handle fractions like "1/2"
                if "/" in text:
                    num, denom = text.split("/")
                    row_vals.append(float(num) / float(denom))
                else:
                    row_vals.append(float(text))
            arr.append(row_vals)
        return arr

    def _reset_button(self):
        self.calculate_button.setEnabled(True)

    @staticmethod
    def calculate_matrix(A: list, b: list) -> List[float]:
        """
        Solve Ax = b using manual Gaussian elimination with partial pivoting.
        Returns x as a list of floats.
        """
        n = len(A)
        # Forward elimination
        for i in range(n):
            # Partial pivot: find the row with max absolute value in column i
            # aka. best row to use as base
            # checks which row has highest value per row
            max_row = max(range(i, n), key=lambda r: abs(A[r][i]))
            if abs(A[max_row][i]) < 1e-12:
                # checks floating point errors
                # and those that cant be solved
                # ex. x+2y = 5
                # and x+2y = 3
                raise ValueError("Matrix is singular or nearly singular")
                # disallows singular matrix
            # Swap rows
            # put best row on top
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            # Eliminate below
            # aka find the multiplier factor for each row.
            for k in range(i + 1, n):
                factor = A[k][i] / A[i][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
                b[k] -= factor * b[i]
        # Back substitution
        # finds x, y, z
        x = [0] * n
        for i in range(n - 1, -1, -1):
            sum_ax = sum(A[i][j] * x[j] for j in range(i + 1, n))
            x[i] = (b[i] - sum_ax) / A[i][i]
        return x


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Setup()
    window.show()
    app.exec()
