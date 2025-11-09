import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit,
                             QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox,
                             QTableWidget, QTableWidgetItem, QGroupBox)
from PyQt5.QtGui import QFont
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import graph_module as gm
import detection
import resolution
import data

class DeadlockGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Deadlock Detection & Resolution System")
        self.setGeometry(100, 100, 1000, 600)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        controls_layout = QVBoxLayout()

        self.p_input = QLineEdit()
        self.p_input.setPlaceholderText("Enter Process ID (e.g., P1)")
        self.p_priority = QLineEdit()
        self.p_priority.setPlaceholderText("Priority (1-10)")
        controls_layout.addWidget(QLabel("Add Process"))
        controls_layout.addWidget(self.p_input)
        controls_layout.addWidget(self.p_priority)
        p_btn = QPushButton("Add Process")
        p_btn.clicked.connect(self.add_process)
        controls_layout.addWidget(p_btn)

        self.r_input = QLineEdit()
        self.r_input.setPlaceholderText("Enter Resource ID (e.g., R1)")
        controls_layout.addWidget(QLabel("Add Resource"))
        controls_layout.addWidget(self.r_input)
        r_btn = QPushButton("Add Resource")
        r_btn.clicked.connect(self.add_resource)
        controls_layout.addWidget(r_btn)

        a_btn = QPushButton("Allocate Resource")
        a_btn.clicked.connect(self.allocate)
        q_btn = QPushButton("Request Resource")
        q_btn.clicked.connect(self.request)
        controls_layout.addWidget(a_btn)
        controls_layout.addWidget(q_btn)

        detect_btn = QPushButton("Detect & Resolve Deadlock")
        detect_btn.setStyleSheet("background-color: orange")
        detect_btn.clicked.connect(self.detect)
        controls_layout.addWidget(detect_btn)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.canvas, stretch=1)
        self.setLayout(main_layout)

    def add_process(self):
        pid = self.p_input.text()
        priority = self.p_priority.text()
        if pid:
            gm.add_process(pid)
            try:
                data.process_metadata[pid] = {
                    "priority": int(priority) if priority else 5,
                    "runtime": 5
                }
            except ValueError:
                data.process_metadata[pid] = {"priority": 5, "runtime": 5}
            self.update_graph()

    def add_resource(self):
        rid = self.r_input.text()
        if rid:
            gm.add_resource(rid)
            self.update_graph()

    def allocate(self):
        pid = self.p_input.text()
        rid = self.r_input.text()
        if pid and rid:
            gm.allocate_resource(pid, rid)
            self.update_graph()

    def request(self):
        pid = self.p_input.text()
        rid = self.r_input.text()
        if pid and rid:
            gm.request_resource(pid, rid)
            self.update_graph()

    def detect(self):
        if detection.detect_deadlock():
            QMessageBox.warning(self, "Deadlock Detected", "Deadlock Detected! Resolving...")
            resolution.resolve_deadlock()
            self.update_graph()
        else:
            QMessageBox.information(self, "Safe", "No Deadlock Detected.")

    def update_graph(self):
        self.figure.clear()
        G = nx.DiGraph()
        for node, neighbors in data.rag.items():
            for neighbor in neighbors:
                G.add_edge(node, neighbor)
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, arrows=True)
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = DeadlockGUI()
    gui.show()
    sys.exit(app.exec_())
