# coding:utf-8
'''
Created on 20220105

@author: Yingjie Zhang
'''
import matplotlib.pyplot as plt
import numpy as np

def plot_array(img: np.array, size = (5,5)):
    #plt.clf()
    fig = plt.figure()
    fig.set_size_inches(size[0],size[1])
    ax = fig.add_axes([0, 0, 1, 1], frameon = False, aspect = 1)
    ax.set_xticks = ([])
    ax.set_yticks = ([])
    plt.imshow(img,cmap="Greys")
    plt.show()

def encryptionWithMode(mode):
    # Open image with PIL.Image
    from PIL import Image
    img = Image.open("data/tux.png")
    
    # Convert image to numpy ndarray
    img = np.array(img)
    
    # Plot shape and type of pixels
    print(f"shape of image: {img.shape}")
    print(f"type of image: {img.dtype}")
    # Show plot of tux
    plot_array(img)
    
    # Save the shape of the image
    shape = (img.shape[0],img.shape[1],img.shape[2])
    
    # Flatten the image
    img_flat = img.flatten()
    
    # recall that all pixels are of type unsigned integer of 8 bits (uint8), that's a byte! 
    img_bytes = bytes([x for x in img_flat])
    
    # print the first 10 bytes
    print(img_bytes[:10])
    
    # check if we need to pad the message (image), if so use PKCS7 from cryptography library
    block_size = 16
    print(f"Bytes remainder {len(img_bytes)%block_size}")
    
    # Declare the AES in ECB mode
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    import os
    
    # draw 32 random bytes for secret key
    secret_key = os.urandom(32)
    
    if mode == "ECB":
        # define cipher with AES algorithm and ECB mode
        cipher = Cipher(algorithms.AES(secret_key), modes.ECB(), backend=default_backend())
    elif mode == "CBC":
        # draw initialization vector 16 bytes
        iv = os.urandom(16)
        
        # define cipher with AES algorithm and CBC mode
        cipher = Cipher(algorithms.AES(secret_key), modes.CBC(iv), backend=default_backend())
        
    # define encryptor and decryptor
    encryptor = cipher.encryptor()
    decryptor = cipher.decryptor()
    
    # encrypt the image
    ctx = encryptor.update(img_bytes) + encryptor.finalize()
    print(ctx[0:50])
    
    # Plot the ciphertext
    # reshape the ciphertext to the oringial shape of the image
    ctx_flat_int = [x for x in ctx]
    ctx_img = np.array(ctx_flat_int).reshape(shape[0], shape[1], shape[2])
    # plot ciphertext of Tux!
    plot_array(ctx_img)
    
    # Recover the original image
    # get the plaintext in bytes
    pltx = decryptor.update(ctx)
    
    # reshape the plaintext to get the pixels
    pltx_img = np.array([x for x in pltx], dtype=np.uint8).reshape(shape[0], shape[1], shape[2])
    # plot image
    plot_array(pltx_img)

encryptionWithMode("ECB")
    