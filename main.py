import inspect
import sys

from PyQt6.QtWidgets import QApplication

import engine
#from importlib.metadata.diagnose import inspect
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

def debugging():
    print("module file:", getattr(engine, '__file__', None))
    print("engine attrs:", [n for n in dir(engine) if not n.startswith('_')])
    print("Engine type:", getattr(engine, 'Engine', None))
    print("Engine has step:", hasattr(engine.Engine, 'step'))
    try:
        print(inspect.getsource(engine.Engine))
    except Exception as e:
        print("cannot show source:", e)
        
if __name__ == "__main__":
    main()