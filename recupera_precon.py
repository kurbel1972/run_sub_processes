import shutil
import os

# Directories
input_directory = r"\\gov004\IPS-EDI\Input\Error\precon"
output_directory = r"\\gov004\IPS-EDI\Input"

def process_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        print(f"Processing file: {input_file_path}")

        # Initialize the replacement count
        replacements_u = content.count("TSR++++U")
        replacements_e = content.count("TSR++++E")
        total_replacements = replacements_u + replacements_e

        # Replace "TSR++++U" and "TSR++++E" with "TSR++++A"
        new_content = content.replace("TSR++++U", "TSR++++A")
        new_content = new_content.replace("TSR++++E", "TSR++++A")

        # Check if any replacements were made
        if total_replacements > 0:
            with open(input_file_path, 'w', encoding='utf-8') as file:
                print(f"Saving modified file, {total_replacements} replacements made.")
                file.write(new_content)
            print(f"File processed and saved at: {output_file_path}")

            # Move the original file to the output directory
            shutil.move(input_file_path, os.path.join(output_directory, os.path.basename(input_file_path)))
            print(f"Original file moved to: {output_directory}")
        else:
            print(f"No changes needed for: {input_file_path}")
    except Exception as e:
        print(f"Error processing file {input_file_path}: {e}")

def main():
    for file_name in os.listdir(input_directory):
        if file_name.startswith("IPC") and file_name.endswith(".edi"):
            input_file_path = os.path.join(input_directory, file_name)
            output_file_path = os.path.join(output_directory, file_name)

            # Process the file
            process_file(input_file_path, output_file_path)

if __name__ == "__main__":
    main()
