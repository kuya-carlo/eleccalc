import sys
from typing import Optional

from PySide6.QtWidgets import QApplication, QMainWindow


class Calculator:
    pass


if __name__ == "__main__":
    cols: Optional[int] = None
    if sys.argv[1].isdigit():
        cols = int(sys.argv[1])
        if cols < 3:
            raise ValueError("Number given is less than 3. Cannot continue.")
    else:
        raise ValueError(f"{sys.argv[1]} is not convertable to matrix size, try again/")
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.show()
    app.exec()
