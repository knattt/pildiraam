import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import webview

def plot_data():
    # Load the CSV file
    df = pd.read_csv("hinnaandmed.csv", encoding="ISO-8859-1", sep=";") 

    # Replace commas in "NPS Eesti" with dots, convert to float
    df["NPS Eesti"] = df["NPS Eesti"].str.replace(",", ".").astype(float)

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(4.8, 4))  # Adjust to half the height of the window (400px)

    # Bar plot of "Eesti aeg" vs. "NPS Eesti"
    ax.bar(pd.to_datetime(df.iloc[:, 1], dayFirst=True), df["NPS Eesti"], color="black", width=0.04, align="center")

    # Customize the x-axis to show only time
    from matplotlib.dates import DateFormatter
    time_format = DateFormatter("%H:%M")  # Format for hours and minutes
    ax.xaxis.set_major_formatter(time_format)

    # Customize the plot
    ax.set_title("Elektrihind")
    ax.set_ylabel("s/kWh")
    ax.tick_params(axis="x", rotation=90)  # Rotate x-axis labels for better readability

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, side=tk.TOP)

def show_weather_widget():
    # Launch the weather widget in a webview
    webview.create_window("Weather Widget", "https://www.yr.no/en/content/2-588335/card.html", width=480, height=400)
    webview.start()

# Initialize the Tkinter window
root = tk.Tk()
root.title("Elektrihind ja Ilm")
root.geometry("480x800")

# Plot data in the upper half
plot_data()

# Create the lower half for the weather widget
weather_button_frame = tk.Frame(root)
weather_button_frame.pack(fill=tk.BOTH, expand=True)

# Add a button to launch the weather widget in a separate window
weather_button = tk.Button(weather_button_frame, text="Open Weather Widget", command=show_weather_widget)
weather_button.pack(fill=tk.BOTH, expand=True)

# Run the Tkinter main loop
root.mainloop()
