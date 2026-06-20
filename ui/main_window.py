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
import numpy as np
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

        self.mutation_rate = QDoubleSpinBox()
        self.mutation_rate.setRange(0, 10000)
        self.mutation_rate.setValue(50)

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.continue_button = QPushButton("Continue")

        settings_layout.addWidget(QLabel("World size"))
        settings_layout.addWidget(self.world_size)

        settings_layout.addWidget(QLabel("Sun"))
        settings_layout.addWidget(self.sun_income)

        settings_layout.addWidget(QLabel("Minerals"))
        settings_layout.addWidget(self.mineral_income)

        settings_layout.addWidget(QLabel("Mutation 0.1%"))
        settings_layout.addWidget(self.mutation_rate)

        settings_layout.addWidget(self.start_button)
        settings_layout.addWidget(self.stop_button)
        settings_layout.addWidget(self.continue_button)

        main_layout.addLayout(settings_layout)

        # ------------------------
        # Центральная область
        # ------------------------

        graphs_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        graphs_layout.addLayout(left_layout, 3)
        graphs_layout.addLayout(right_layout, 1)

        main_layout.addLayout(graphs_layout)

        # ------------------------
        # График популяции
        # ------------------------

        self.population_plot = pg.PlotWidget(title="Population")
        self.population_curve = self.population_plot.plot()

        left_layout.addWidget(self.population_plot)

        # ------------------------
        # График источников энергии
        # ------------------------

        self.energy_plot = pg.PlotWidget(title="Energy Sources")

        self.sun_curve = self.energy_plot.plot(
            name="Sun",
            pen='g'
        )

        self.mineral_curve = self.energy_plot.plot(
            name="Minerals",
            pen='b'
        )

        self.hunt_curve = self.energy_plot.plot(
            name="Hunting",
            pen='r'
        )

        left_layout.addWidget(self.energy_plot)

        # ------------------------
        # Геном лидера
        # ------------------------

        self.genome_label = QLabel(
            "Youngest genome:\n[]"
        )

        left_layout.addWidget(self.genome_label)

        # ------------------------------
        # Карта распределения по высотам
        # ------------------------------

        self.height_plot = pg.PlotWidget(
            title="Population by Height"
        )

        self.height_plot.setLabel(
            'left',
            'Height'
        )

        self.height_plot.hideAxis('bottom')

        self.height_image = pg.ImageItem()

        self.height_plot.addItem(
            self.height_image
        )
        #Цветовая карта
        color_map = pg.ColorMap(
            [0.0, 1.0],
            [
                (0, 0, 0, 0),
                (255, 140, 0, 180)
            ]
        )

        self.height_image.setColorMap(
            color_map
        )

        right_layout.addWidget(
            self.height_plot
        )

        # ------------------------
        # График возрастов
        # ------------------------

        self.age_plot = pg.PlotWidget(
            title="Age Distribution"
        )

        self.age_plot.setLabel(
            'left',
            'Bots'
        )

        self.age_plot.setLabel(
            'bottom',
            'Age'
        )

        right_layout.addWidget(
            self.age_plot
        )

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

        # Добавляем виджет для поля
        self.world_plot = pg.PlotWidget(title="World Map")
        self.world_plot.setAspectLocked(True)  # квадратные клетки
        self.world_plot.hideAxis('bottom')
        self.world_plot.hideAxis('left')
        
        self.world_image = pg.ImageItem()
        self.world_plot.addItem(self.world_image)
        
        # Добавляем сетку (опционально, но чуть медленнее)
        # Можно просто нарисовать линии через QPen, но они будут перерисовываться при каждом зумме.
        # Лучше без сетки, а клетки пусть сливаются.
        
        # Добавляем в layout, например, в правую колонку или новую вкладку
        self.world_plot.setFixedSize(400, 400)
        right_layout.addWidget(self.world_plot)  # или в левый layout

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

        self.engine = Engine(self.world_size.value(), self.sun_income.value(), self.mineral_income.value(), self.mutation_rate.value())

        self.console.append("Simulation started")

        self.population_data.clear()
        self.sun_data.clear()
        self.mineral_data.clear()
        self.hunt_data.clear()

        self.timer.start(100)

    def update_demo(self):
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

        # for log in stats.logs[self.last_log_index:]:
        #     self.console.append(log)

        if step % 3 == 0:
            pass
        self.update_world_view()

        if step % 50 == 49:
            stats.collect_rare(self.engine.world)
            self.update_height_distribution(
                stats.height_distribution
            )

            self.update_age_distribution(
                stats.age_distribution
            )

            self.console.append(
                f"Step {self.engine.tick}: population={population}"
            )
            self.genome_label.setText(
                f"Youngest genome:\n"
                f"{stats.youngest_genome}"
            )

    def update_world_view(self):
        world = self.engine.world
        size_x = world.size_x
        size_y = world.size
        img = np.zeros((size_x, size_y, 3), dtype=np.uint8)
        count = 0
        for bot in world.bots:
            x, y = bot.x, bot.y
            if 0 <= x < size_x and 0 <= y < size_y:
            # Оттенок от красного (энергия 0) до зелёного (энергия 800)
                energy_norm = min(1.0, bot.energy / 1000.0)
                r = int(255 * (1 - energy_norm))
                g = int(255 * energy_norm)
                b = 0
                r = max(0, min(r, 255))
                g = max(0, min(g, 255))
                b = max(0, min(b, 255))
                img[x, y] = [r, g, b]
                count += 1
        organics_items = world.organics.values()
        for org in organics_items:
            x, y = org.x, org.y
            if 0 <= x < size_x and 0 <= y < size_y:
                img[x, y] = org.color
        self.world_image.setImage(img, autoLevels=False)

    def update_height_distribution(self, height_distribution):
        world_size = len(height_distribution)
        max_population = max(max(height_distribution), 1)
        img = np.zeros((1, world_size), dtype=float)
        for y, count in enumerate(height_distribution):
            img[0, y] = count / max_population
        self.height_image.setImage(
            img,
            autoLevels=False,
            levels=(0, 1)
        )
        self.height_image.setRect(
            0,
            0,
            1,
            world_size
        )
        self.height_plot.setYRange(
            0,
            world_size
        )
        self.height_plot.setXRange(
            0,
            1
        )

    def update_age_distribution(
        self,
        age_distribution
    ):
        """
        age_distribution:

        {
            age: count
        }
        """

        self.age_plot.clear()

        ages = list(
            age_distribution.keys()
        )

        counts = list(
            age_distribution.values()
        )

        bars = pg.BarGraphItem(
            x=ages,
            height=counts,
            width=0.8
        )

        self.age_plot.addItem(
            bars
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