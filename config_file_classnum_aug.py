import re

config_file_path =r"D:\AI_SVT_Training_mk\configs\test.config"
config_file_path = config_file_path.replace("\\","/")

new_last_digit = input("Enter the new last digit for class_num: ")

if len(new_last_digit) == 1 and new_last_digit.isdigit():
    # Read the content of the ".config" file
    with open(config_file_path, "r") as config_file:
        config_content = config_file.read()

    # Define a regular expression pattern to match the class_num line
    pattern = r"num_classes:\d"

    # Use re.sub to replace all matched instances of class_num
    new_config_content = re.sub(pattern, f"num_classes:{new_last_digit}", config_content)

    # Write the modified content back to the ".config" file
    with open(config_file_path, "w") as config_file:
        config_file.write(new_config_content)
else:
    print("Invalid input. Please enter a single digit.")

# Define text strings that indicate the start and end of the section
start_marker_text = "#start"
end_marker_text = "#end"

# Define the dictionary of lines to insert
lines_to_insert = {
    '  data_augmentation_options {random_horizontal_flip{}}',
    '  data_augmentation_options {random_vertical_flip{}}',
    '  data_augmentation_options {random_adjust_brightness{}}',
    '  data_augmentation_options {random_adjust_contrast{}}',
    '  data_augmentation_options {random_rotation90{}}'
    # Add more values as needed
}

# Read the content of the ".config" file
with open(config_file_path, "r") as config_file:
    config_lines = config_file.readlines()

start_index = None
end_index = None

for i, line in enumerate(config_lines):
    if start_marker_text in line:
        start_index = i
    if end_marker_text in line:
        end_index = i

# Check if both markers were found
if start_index is not None and end_index is not None:
    # Remove the lines within the section
    config_lines[start_index + 1:end_index] = []

    # Prompt the user to select lines to insert
    print("Select lines to insert:")
    for line_value in lines_to_insert:
        user_input = input(f"Include {line_value}? (y/n): ")
        if user_input.lower() == 'y':
            config_lines.insert(start_index + 1, f"{line_value}\n")

    # Write the modified content back to the ".config" file
    with open(config_file_path, "w") as config_file:
        config_file.writelines(config_lines)
else:
    print("Start and/or end markers not found in the file. Check your configuration.")