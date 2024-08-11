from bokeh.plotting import figure, show, output_file
from bokeh.io import curdoc

import re
from datetime import datetime

def read_data(file_path):
    timestamps = []
    speeds = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    timestamp = None
    for line in lines:
        timestamp_match = re.match(r'Timestamp: (.+)', line)
        if timestamp_match:
            timestamp = timestamp_match.group(1)
            continue
        bitrate_match = re.search(r'(\d+\.?\d*) Mbits/sec', line)
        if bitrate_match and timestamp:
            try:
                bitrate = float(bitrate_match.group(1))
                timestamp_dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                timestamps.append(timestamp_dt)
                speeds.append(bitrate)
            except ValueError:
                print(f"Warning: Unable to parse data '{line.strip()}'.")

    return timestamps, speeds


file_path = 'soal_chart_bokeh.txt'

timestamps, speeds = read_data(file_path)

output_file('line_chart.html')

p = figure(x_axis_label='Timestamp', y_axis_label='Speed', x_axis_type='datetime', title='Speed vs Timestamp')
p.line(timestamps, speeds, line_width=2)


show(p)
