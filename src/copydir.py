import os
import shutil

def copy_dir_contents(from_dir, to_dir):
    if not os.path.exists(from_dir):
        raise Exception(f"Can't find directory: {from_dir}")
    if os.path.exists(to_dir):
        shutil.rmtree(to_dir)
    os.mkdir(to_dir)
    contents = os.listdir(from_dir)
    for item in contents:
        from_path = os.path.join(from_dir, item)
        to_path = os.path.join(to_dir, item)
        if os.path.isfile(from_path):
            shutil.copy(from_path, to_path)
        elif os.path.isdir(from_path):
            os.mkdir(to_path)
            copy_dir_contents(from_path, to_path)
