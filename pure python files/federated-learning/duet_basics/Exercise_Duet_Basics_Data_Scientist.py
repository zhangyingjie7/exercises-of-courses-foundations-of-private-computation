'''
Created on 20211213

@author: zhang
'''
import syft as sy
########## Part 1:Join the Duet Server the Data Owner connected to ##########
duet = sy.join_duet(loopback=True)

import time
time.sleep(30)
print("Pause end for data scientist...........")

########## Part 2: Search for Available Data ##########
# The data scientist can check the list of searchable data in Data Owner's duet store
print(duet)
print(duet.store.pandas)

# Data Scientist finds that there are Heights and Weights of a group of people. There are some analysis he/she can do with them together.
heights_ptr = duet.store[0]
weights_ptr = duet.store[1]

# heights_ptr is a reference to the height dataset remotely available on data owner's server
print(heights_ptr)

# weights_ptr is a reference to the weight dataset remotely available on data owner's server
print(weights_ptr)

for i in range(6):
    print("Pointer to Weight of person", i + 1, weights_ptr[i])
    print("Pointer to Height of person", i + 1, heights_ptr[i])


def BMI_calculator(w_ptr, h_ptr):
    bmi_ptr = 0
    ##TODO
    "Write your code here for calculating bmi_ptr"
    h_ptr_square = h_ptr.float().square()
    bmi_ptr = (w_ptr / h_ptr_square) * 10000
    ###
    return bmi_ptr


def weight_status(w_ptr, h_ptr):
    status = None
    bmi_ptr = BMI_calculator(w_ptr, h_ptr)
    ##TODO
    """Write your code here. 
    Possible values for status: 
    Normal, 
    Overweight, 
    Obese, 
    Out of range
    """""
    bmi_ptr = bmi_ptr.get(
        request_block=True,
        reason="accept",
        timeout_secs=10,
    )
    if bmi_ptr.int() in range(19, 25):
        status = 'Normal'
    elif bmi_ptr.int() in range(25, 30):
        status = 'Overweight'
    elif bmi_ptr.int() in range(30, 40):
        status = 'Obese'
    else:
        status = 'Out of range'
    ###
    return status

for i in range(0, 6):
    bmi_ptr = BMI_calculator(weights_ptr[i], heights_ptr[i])

statuses = []
for i in range(0, 6):
    status = weight_status(weights_ptr[i], heights_ptr[i])
    print("Weight of Person", i + 1, "is", status)
    statuses.append(status)

assert statuses == ["Normal", "Overweight", "Obese", "Normal", "Overweight", "Normal"]