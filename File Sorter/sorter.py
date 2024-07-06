import os
import mimetypes
from datetime import datetime
from PIL import Image, ExifTags
import shutil


def test(directory):
    try:
        # List all entries in the top-level directory
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file():
                    print(f'File: {entry.name}')
                elif entry.is_dir():
                    print(f'Subdirectory: {entry.name}')
    except FileNotFoundError as e:
        print(f'Error: {e}')
    except PermissionError as e:
        print(f'Error: {e}')


def file_type(directory):
        file_types = {}

        # Use os.scandir to iterate through the entries in the top-level directory
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.is_file():
                    file_path = str(entry.path)
                    file_type, _ = mimetypes.guess_type(file_path)
                    if file_type:
                        main_type = file_type.split('/')[0]
                        if main_type in file_types:
                            file_types[main_type].append(entry.name)
                        else:
                            file_types[main_type] = [entry.name]

        return file_types


def file_ext(directory):
    file_types = {}

    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                file_path = str(entry.path)
                file_type, _ = mimetypes.guess_type(file_path)
                if file_type:
                    ext = file_type.split('/')[1]
                    if ext in file_types:
                        file_types[ext].append(entry.name)
                    else:
                        file_types[ext] = [entry.name]

    print(file_types)
    return file_types


def extract(directory):
    directory = os.path.abspath(directory)

    for root, dirnames, filenames in os.walk(directory, topdown=False):
        for filename in filenames:
            file_path = str(os.path.join(root, filename))
            new_path = str(os.path.join(directory, filename))
            shutil.move(file_path, new_path)

        for dirname in dirnames:
            dir_path = os.path.join(root, dirname)
            try:
                os.rmdir(dir_path)
            except OSError:
                pass


def file_date_new(directory, sort_by='days'):
    file_types = {}

    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                file_path = entry.path
                file_type, _ = mimetypes.guess_type(file_path)

                if file_type and (file_type.startswith('image') or file_type.startswith('video')):
                    date_taken = "None"
                    try:
                        if file_type.startswith('image'):
                            image = Image.open(file_path)
                            exif_data = image.getexif()
                            print(exif_data, type(exif_data))
                            if exif_data:
                                for tag, value in exif_data.items():
                                    if ExifTags.TAGS.get(tag) == 'DateTime':
                                        date_taken = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                                        break

                        if date_taken:
                            if sort_by == 'years':
                                date_key = date_taken.strftime('%Y')
                            elif sort_by == 'months':
                                date_key = date_taken.strftime('%Y-%m')
                            elif sort_by == 'days':
                                date_key = date_taken.strftime('%Y-%m-%d')
                            else:
                                raise ValueError("sort_by must be 'days', 'months', or 'years'")

                            if date_key in file_types:
                                file_types[date_key].append(entry.name)
                            else:
                                file_types[date_key] = [entry.name]
                    except Exception as e:
                        pass  # Ignore errors and continue

    return file_types


def move(dictionary, base_directory):
    if not os.path.isdir(base_directory):
        print(f"The base directory {base_directory} does not exist.")
        return
    for dir_name, file_names in dictionary.items():
        target_dir = str(os.path.join(base_directory, dir_name))
        os.makedirs(target_dir, exist_ok=True)

        for file_name in file_names:
            source_path = str(os.path.join(base_directory, file_name))
            target_path = str(os.path.join(target_dir, file_name))

            try:
                shutil.move(source_path, target_path)
                print(f"Moved {file_name} to {target_dir}")
            except Exception as e:
                print(f"Error moving {file_name} to {target_dir}: {e}")
                print(source_path)