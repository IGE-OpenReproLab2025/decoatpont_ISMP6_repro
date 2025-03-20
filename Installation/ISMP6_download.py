import os 
import numpy as np

path = input("Enter the path:")
filepath = os.path.join(path, 'name.txt')

file = np.loadtxt(filepath, dtype = 'str')
name = file
new_name = [i[:-1] for i in name]

for dir in new_name:
    print(f"Downloading directory: {dir}")
    command = f"globus transfer '3881e705-3290-4e81-8990-0ef8cfb54d74:/{dir}/' `globus endpoint local-id`:./{dir}"
    os.system(command)

print("You successfully downloaded all the datastes!")
