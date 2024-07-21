import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import os

def xspf_to_m3u(xspf_path):
    # Determine the output path (same directory, but .m3u extension)
    m3u_path = os.path.splitext(xspf_path)[0] + '.m3u'

    # Parse the XSPF file
    tree = ET.parse(xspf_path)
    root = tree.getroot()

    # Namespace for XSPF
    ns = {'xspf': 'http://xspf.org/ns/0/'}

    # Extract track locations
    locations = [track.find('xspf:location', ns).text for track in root.findall(".//xspf:track", ns)]

    # Write to M3U file
    with open(m3u_path, 'w') as m3u_file:
        # Write header
        m3u_file.write("#EXTM3U\n")
        for location in locations:
            m3u_file.write(location + '\n')

# Example usage
root = tk.Tk()
root.withdraw()  # To hide the empty tkinter window
xspf_path = filedialog.askopenfilename(title = "Select the xspf file to convert", filetypes = (("xspf files", "*.xspf"), ("all files", "*.*")))
if xspf_path:  # Check if a file was selected
    xspf_to_m3u(xspf_path)
