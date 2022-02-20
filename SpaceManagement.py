import os

SIZE_LIMIT = 7 * 1000 * 1000 * 1000

def get_size_of_downloads_folder():
    folderPath = './downloads'
    size = 0
    for path, dirs, files in os.walk(folderPath):
        for f in files:
            fp = os.path.join(path,f)
            size += os.path.getsize(fp)

    return size

def delete_all_files_in_downloads_folder():
    folderPath = './downloads'
    for path, dirs, files in os.walk(folderPath):
        for f in files:
            fp = os.path.join(path,f)
            os.remove(fp)

def handle_downloads_space():
    print(get_percent_of_size_limit())
    if get_size_of_downloads_folder() > SIZE_LIMIT:
        delete_all_files_in_downloads_folder()

def get_percent_of_size_limit():
    return get_size_of_downloads_folder() / SIZE_LIMIT
