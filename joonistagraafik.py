import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, HourLocator
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def plot_data():
    # Load the CSV file with specified encoding and delimiter
    df = pd.read_csv("hinnaandmed.csv", encoding="ISO-8859-1", sep=";")

    # Replace any incorrect characters in the column names
    df.columns = [col.replace("�", "ä") for col in df.columns]

    # Replace commas with dots in the "NPS Eesti" column, convert to float, and divide by 10
    df["NPS Eesti"] = df["NPS Eesti"].str.replace(",", ".").astype(float) / 10

    # Convert the "Kuupäev (Eesti aeg)" column to datetime format
    df["Kuupäev (Eesti aeg)"] = pd.to_datetime(df["Kuupäev (Eesti aeg)"], format="%d.%m.%Y %H:%M")

    # Load the last updated time from the text file
    try:
        with open("hindadevärskendamiseaeg.txt", mode="r", encoding="utf-8") as file:
            updated_time = file.read().strip()
    except FileNotFoundError:
        updated_time = "puudub"  # Default if file is not found

    # Create a figure for the plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Bar plot with black bars, offset to align with full hours
    ax.bar(df["Kuupäev (Eesti aeg)"], df["NPS Eesti"], color="black", width=0.04, align='edge')  # Align on edge

    # Set the title with the updated time included
    ax.set_title(f"Elektrihind ({updated_time} seisuga)", color="black")
    ax.set_ylabel("s/kWh", color="black")
    
    # Format the x-axis to show date changes and time only otherwise
    ax.xaxis.set_major_locator(HourLocator(interval=1))  # Set major ticks every hour
    ax.xaxis.set_major_formatter(DateFormatter("%H"))  # Format tick labels as time
    ax.xaxis.set_minor_formatter(DateFormatter("%d.%m.%Y"))  # Format minor ticks as date
    
    # Display the date label only where it changes
    for label in ax.get_xticklabels(which='minor'):
        label.set_horizontalalignment('center')
        label.set_rotation(45)
        label.set_color('black')

    # Remove vertical grid lines and keep horizontal grid lines
    plt.grid(visible=True, color="gray", linestyle="--", linewidth=0.5, axis="y")
    plt.tight_layout()

    # Embed the plot in a frame within the Tkinter window
    plot_frame = tk.Frame(root)
    plot_frame.pack(fill=tk.BOTH, expand=True)
    
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Set up the Tkinter window
root = tk.Tk()
root.title("Elektrihind")
root.geometry("480x800")

# Call the plot function to display data in the GUI
plot_data()

# Run the Tkinter main loop
root.mainloop()
