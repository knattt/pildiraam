import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSplitter
from PyQt5.QtWebEngineWidgets import QWebEngineView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None):
        # Initialize the figure for plotting
        fig, self.ax = plt.subplots(figsize=(10, 3))
        super().__init__(fig)
        self.setParent(parent)
        
        # Load and plot data
        self.plot_data()

    def plot_data(self):
        # Load the CSV file
        df = pd.read_csv("hinnaandmed.csv", encoding="ISO-8859-1", sep=";")
        df.columns = [col.replace("�", "ä") for col in df.columns]
        df["NPS Eesti"] = df["NPS Eesti"].str.replace(",", ".").astype(float) / 10
        df["Kuupäev (Eesti aeg)"] = pd.to_datetime(df["Kuupäev (Eesti aeg)"], format="%d.%m.%Y %H:%M")

        # Load last updated time
        try:
            with open("hindadevärskendamiseaeg.txt", mode="r", encoding="utf-8") as file:
                updated_time = file.read().strip()
        except FileNotFoundError:
            updated_time = "puudub"

        # Plot data
        self.ax.bar(df["Kuupäev (Eesti aeg)"], df["NPS Eesti"], color="black", width=0.04, align='edge')
        self.ax.set_title(f"Elektrihind ({updated_time} seisuga)", color="black")
        self.ax.set_ylabel("s/kWh", color="black")
        self.ax.grid(visible=True, color="gray", linestyle="--", linewidth=0.5, axis="y")

        # Format x-axis for date and time
        self.ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%H"))
        self.ax.xaxis.set_minor_formatter(plt.matplotlib.dates.DateFormatter("%d.%m.%Y"))

        # Add padding to avoid cropping
        plt.subplots_adjust(left=0.15, right=0.95, top=0.9, bottom=0.15)

        # Render the plot
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create main layout
        self.setWindowTitle("Elektrihind ja Ilm")
        self.setGeometry(100, 100, 800, 600)
        
        # Create a splitter to separate the plot and web view
        splitter = QSplitter(Qt.Vertical)
        
        # Plot canvas
        self.plot_canvas = PlotCanvas(self)
        splitter.addWidget(self.plot_canvas)

        # Web view for weather widget
        self.web_view = QWebEngineView()
        self.web_view.setUrl("https://www.yr.no/en/content/2-588335/card.html")
        splitter.addWidget(self.web_view)
        
        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(splitter)

        # Central widget to hold layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

# Run the application
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
