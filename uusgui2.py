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

    # Convert the second column to datetime
    timestamps = pd.to_datetime(df.iloc[:, 1], dayfirst=True)

    # Load the datetime from the file
    try:
        with open("hindadevärskendamiseaeg.txt", "r", encoding="utf-8") as file:
            update_time = file.read().strip()
    except FileNotFoundError:
        update_time = "Teadmata"

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(4.8, 4))  # Adjust to half the height of the window (400px)

    # Adjust bottom margin to make room for the text
    plt.subplots_adjust(bottom=0.2)  # Increase bottom margin to 20% of the figure

    # Bar plot of "Eesti aeg" vs. "NPS Eesti"
    bar_width = 0.05  # Adjusted width to ensure gaps
    ax.bar(timestamps, df["NPS Eesti"]/10, color="black", width=bar_width, align="edge", edgecolor="white")

    # Set x-ticks at the left edge of each bar
    tick_positions = timestamps - pd.Timedelta(seconds=bar_width * 3600)  # Adjust ticks to left edge
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(timestamps.dt.strftime("%H:%M"))  # Format for hours and minutes

    # Customize the plot
    ax.set_title("Elektrihind")
    ax.set_ylabel("s/kWh")
    ax.tick_params(axis="x", rotation=90)  # Rotate x-axis labels for better readability

    # Add the "Uuendatud" text below the plot
    fig.text(
        0.01, 0.03,  # Position near the bottom-left corner with more vertical space
        f"Uuendatud: {update_time}",
        fontsize=8,  # Smaller font size
        ha="left"  # Align to the left
    )

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
