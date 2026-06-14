try:
    from PyQt6.QtCore import QTimer
    from PyQt6.QtWidgets import (
        QWidget,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QPushButton,
        QTextEdit,
        QSpinBox,
        QDoubleSpinBox,
    )
except Exception:
    try:
        from PySide6.QtCore import QTimer
        from PySide6.QtWidgets import (
            QWidget,
            QVBoxLayout,
            QHBoxLayout,
            QLabel,
            QPushButton,
            QTextEdit,
            QSpinBox,
            QDoubleSpinBox,
        )
    except Exception:
        try:
            from PyQt5.QtCore import QTimer
            from PyQt5.QtWidgets import (
                QWidget,
                QVBoxLayout,
                QHBoxLayout,
                QLabel,
                QPushButton,
                QTextEdit,
                QSpinBox,
                QDoubleSpinBox,
            )
        except Exception:
            from PySide2.QtCore import QTimer
            from PySide2.QtWidgets import (
                QWidget,
                QVBoxLayout,
                QHBoxLayout,
                QLabel,
                QPushButton,
                QTextEdit,
                QSpinBox,
                QDoubleSpinBox,
            )

import pyqtgraph as pg
import random
import sys

from engine import Engine
from export_logs import save_logs

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Evolution Simulator")
        self.resize(1200, 800)

        self.population_data = [] # число популяции
        self.sun_data = [] # кол-во получаемой энергии от солнца
        self.mineral_data = [] # кол-во получаемой энергии от минералов
        self.hunt_data = [] # кол-во получаемой энергии от охоты
        self.setup_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_demo)

        self.last_log_index = 0

    def setup_ui(self):
        main_layout = QVBoxLayout()

        # ------------------------
        # Панель настроек
        # ------------------------

        settings_layout = QHBoxLayout()

        self.world_size = QSpinBox()
        self.world_size.setRange(10, 1000)
        self.world_size.setValue(100)

        self.sun_income = QDoubleSpinBox()
        self.sun_income.setRange(0, 1000)
        self.sun_income.setValue(100)

        self.mineral_income = QDoubleSpinBox()
        self.mineral_income.setRange(0, 1000)
        self.mineral_income.setValue(100)

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.continue_button = QPushButton("Continue")

        settings_layout.addWidget(QLabel("World size"))
        settings_layout.addWidget(self.world_size)

        settings_layout.addWidget(QLabel("Sun"))
        settings_layout.addWidget(self.sun_income)

        settings_layout.addWidget(QLabel("Minerals"))
        settings_layout.addWidget(self.mineral_income)

        settings_layout.addWidget(self.start_button)
        settings_layout.addWidget(self.stop_button)
        settings_layout.addWidget(self.continue_button)

        main_layout.addLayout(settings_layout)

        # ------------------------
        # График популяции
        # ------------------------

        self.population_plot = pg.PlotWidget(title="Population")
        self.population_curve = self.population_plot.plot()

        main_layout.addWidget(self.population_plot)

        # ------------------------
        # График источников энергии
        # ------------------------

        self.energy_plot = pg.PlotWidget(title="Energy Sources")

        # set plot colors: Sun=green, Minerals=blue, Hunting=red
        self.sun_curve = self.energy_plot.plot(name="Sun", pen='g')
        self.mineral_curve = self.energy_plot.plot(name="Minerals", pen='b')
        self.hunt_curve = self.energy_plot.plot(name="Hunting", pen='r')

        main_layout.addWidget(self.energy_plot)

        # ------------------------
        # Геном лидера
        # ------------------------

        self.genome_label = QLabel(
            "Most common genome:\n[]"
        )

        main_layout.addWidget(self.genome_label)

        # ------------------------
        # Консоль
        # ------------------------

        self.console = QTextEdit()
        self.console.setReadOnly(True)

        main_layout.addWidget(self.console)

        self.setLayout(main_layout)

        self.start_button.clicked.connect(self.start_simulation)
        self.stop_button.clicked.connect(self.stop_simulation)
        self.continue_button.clicked.connect(self.continue_simulation)

        self.paused = False

    def stop_simulation(self):
        if hasattr(self, 'engine'):
            try:
                path = save_logs(self.engine.hist_logs.logs)
                self.console.append(f"Logs saved to: {path}")
            except Exception as e:
                self.console.append(f"Failed to save logs: {e}")

        # pause the timer so `step` is not called
        if self.timer.isActive():
            self.timer.stop()
        self.paused = True

    def continue_simulation(self):
        # resume the timer
        if not self.timer.isActive():
            self.timer.start(100)
        self.paused = False

    def start_simulation(self):

        self.engine = Engine(self.world_size.value(), self.sun_income.value(), self.mineral_income.value())

        self.console.append("Simulation started")

        self.population_data.clear()
        self.sun_data.clear()
        self.mineral_data.clear()
        self.hunt_data.clear()

        self.timer.start(100)

    def update_demo(self):
        """
        Заглушка.
        Потом сюда подключишь свою симуляцию.
        """
        stats = self.engine.step()
        
        step = len(self.population_data)

        population = stats.population_size

        sun = stats.get_sun_energy()
        minerals = stats.get_mineral_energy()
        hunt = stats.get_hunt_energy()

        self.population_data.append(population)

        self.sun_data.append(sun)
        self.mineral_data.append(minerals)
        self.hunt_data.append(hunt)

        self.population_curve.setData(self.population_data)

        self.sun_curve.setData(self.sun_data)
        self.mineral_curve.setData(self.mineral_data)
        self.hunt_curve.setData(self.hunt_data)

        self.genome_label.setText(
            f"Most common genome:\n"
            f"[1, 4, 2, 8, 3, {step % 10}]"
        )

        # for log in stats.logs[self.last_log_index:]:
        #     self.console.append(log)

        if step % 50 == 49:
            self.console.append(
                f"Step {self.engine.tick}: population={population}"
            )


if __name__ == "__main__":
    try:
        from PyQt6.QtWidgets import QApplication
    except Exception:
        try:
            from PySide6.QtWidgets import QApplication
        except Exception:
            try:
                from PyQt5.QtWidgets import QApplication
            except Exception:
                from PySide2.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())