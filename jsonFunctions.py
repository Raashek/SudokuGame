###########
# modules #
###########
from tkinter import filedialog
import json



#############
# functions #
#############

# Saves data into an file
# I: Name and data
# O: None

def writeFile(contents):
    # Open a file dialog for saving the JSON file
    filePath = filedialog.asksaveasfilename(defaultextension='.json')

    try:
        # Write contents to the JSON file
        with open(filePath, 'w') as file:
            json.dump(contents, file)

    except IOError:
        return []



# Loads data from a file
# I: file name
# O: File contents
def loadFile():
    # Open file dialog to select a JSON file
    filePath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])


    try:
        with open(filePath, "r") as file:
            # Load JSON data from the file
            jsonData = json.load(file)
            # Process the loaded data as needed
            return jsonData

    except (IOError, json.JSONDecodeError) as e:
        # Handle file loading or JSON parsing errors
        return []


