import os

def create_project_dir(directory):
    if not os.path.exists(directory):
        print("Creating project " + directory)
        os.mkdir(directory)

		import numpy as np

def pearson(s1, s2):
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    return np.sum(s1_c * s2_c)/np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))
	
create_project_dir('USER')