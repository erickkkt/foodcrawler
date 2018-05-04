import os

def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating project " + directory)
        os.mkdir(directory)

create_project_dir('USER')