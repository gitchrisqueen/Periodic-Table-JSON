import csv
import json
from collections import OrderedDict


def get_default_from_csv(element, row_header):
    with open('Listing-of-Octave-1-10-expanded.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Atomic Number'] and element['number']:
                try:
                    if int(row['Atomic Number']) == int(element['number']):
                        return row[row_header]
                except ValueError:
                    # Handle the error here
                    print("Error: Invalid value for 'Atomic Number' or 'number': {}, {}".format(row['Atomic Number'],
                                                                                            element['number']))
    return ""


# Load the data from the JSON file
with open('PeriodicTableJSON.json', 'r') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)

# Iterate over each element
for element in data['elements']:
    # Create a new OrderedDict to hold the modified element
    new_element = OrderedDict()
    for key, value in element.items():
        # Copy the attribute to the new OrderedDict
        new_element[key] = value
        # After the "group" attribute, add the new attributes if they don't exist
        if key == 'group':
            new_element.setdefault('tone_number', get_default_from_csv(new_element, 'Tone Number'))
            new_element.setdefault('tone_interval', get_default_from_csv(new_element, 'Tone Interval'))
            new_element.setdefault('tone_position', get_default_from_csv(new_element, 'Tone Position'))
            new_element.setdefault('octave', get_default_from_csv(new_element, 'Octave Number'))
    # Replace the old element with the new one
    element.clear()
    element.update(new_element)

# Write the modified data back to the JSON file
with open('PeriodicTableJSON.json', 'w') as f:
    json.dump(data, f, indent=4)
