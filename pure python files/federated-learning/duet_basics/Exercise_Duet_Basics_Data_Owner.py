'''
Created on 20211213

@author: Yingjie zhang
'''
import syft as sy


# Part 1: Launch a Duet Server
duet = sy.launch_duet(loopback=True)

import time
time.sleep(10)
print("Pause end for data owner, begin to upload data...........")

# Part 2: Upload data to Duet Server
import torch as th

# Data owner has HEIGHTS (cm) data of 6 people - GROUP A
height_data = th.tensor([157.48, 147.32, 149.86, 177.8, 170.18, 182.88])

# Data owner names the data with tag "HEIGHTS"
height_data = height_data.tag("HEIGHTS of GROUP A")

# Data owner adds a description to the tensor where height data is located
height_data = height_data.describe(
    "This is a list of heights (cm) of GROUP A - 6 people."
)

# Finally the data owner UPLOADS THE DATA to the Duet server and makes it searchable
# by data scientists.
height_data_pointer = height_data.send(duet, searchable=True)


# Data owner also has WEIGHTS (kg) data of 6 people - GROUP A
weight_data = th.tensor([57, 61, 74, 76, 78, 67])

# Data owner names the data with tag "WEIGHTS"
weight_data = weight_data.tag("WEIGHTS of GROUP A")

# Data owner adds a description to the tensor where weights data is located
weight_data = weight_data.describe(
    "This is a list of body weights (kg) of GROUP A - 6 people."
)

# Finally the data owner UPLOADS THE DATA to the Duet server and makes it searchable
# by data scientists.
weight_data_pointer = weight_data.send(duet, searchable=True)

print(duet)
print(duet.store.pandas)

assert len(duet.store) == 2

# Part 3: Response to requests coming from Data Scientist
duet.requests.add_handler(action="accept")
print("Upload data end...........")

print("wait for scientist............")
time.sleep(60)       
print(duet.store.pandas)
print("Wait..................")
time.sleep(3600)   