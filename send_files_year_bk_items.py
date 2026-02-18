import os
import shutil
import logging

# Setup basic logging with date and time format
logging.basicConfig(
    filename='send_files_year_bk_items.log', 
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Source and destination directories
source = r'J:\Items\Backup'
destination = r'J:\Items\Backup\2026'
counter_files = 0

# List all files in the source directory
try:
    files = os.listdir(source)
except FileNotFoundError as e:
    logging.error(f"Error listing files in the source directory: {e}")
    raise SystemExit(f"Failed to list files in the source directory. Please check the path and permissions.")

# Iterate through all files and move those starting with 'IPS2026'
for file in files:
    if file.startswith('IPS_OBJ2026'):
        counter_files += 1
        source_file = os.path.join(source, file)
        destination_file = os.path.join(destination, file)
        try:
            shutil.move(source_file, destination_file)
            print(f'Moved: {source_file} -> {destination_file}')
        except Exception as e:
            logging.error(f"Error moving file {file}: {e}")

logging.info(f"Total files moved: {counter_files}")
logging.info("Move operation completed.")
print("Move operation completed.")
