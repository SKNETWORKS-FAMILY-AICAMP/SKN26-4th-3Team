import re
import os

file_path = '/Users/jeonjonghyeok/ReactTS_playground/frontend/src/data/personalData.ts'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

def convert_array_to_string(match):
    field = match.group(1)
    array_str = match.group(2)
    # array_str looks like '"Note1", "Note2"' or '"Note1"'
    # Extract notes by finding all strings inside double quotes
    notes = re.findall(r'"([^"]*)"', array_str)
    joined = ", ".join(notes)
    return f'{field}: "{joined}"'

# Match pattern: field: [ "Note1", "Note2" ]
# We need to handle potential newlines or spaces inside the brackets
pattern = r'(topNotes|middleNotes|baseNotes):\s*\[(.*?)\]'
new_content = re.sub(pattern, convert_array_to_string, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Conversion completed successfully.")
