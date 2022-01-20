# coding:utf-8
'''
Created on 20220112

@author: Yingjie Zhang
'''
import tenseal as ts

# 1. created a context for CKKS encryption
context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60])

sk = context.secret_key()
print("sk",sk)
print()

# 2. Creating Tensors
import numpy as np

plain_tensor = np.random.randn(2, 3)
print("plain_tensor:")
print(plain_tensor)
print()
# encrypted_tensor = ts.ckks_tensor(context, plain_tensor, scale=2**40)
# print("encrypted_tensor",encrypted_tensor)
context.global_scale = 2 ** 40
encrypted_tensor = ts.ckks_tensor(context, plain_tensor)
print("encrypted_tensor:",encrypted_tensor)
print("encrypted_tensor.decrypt:",encrypted_tensor.decrypt())
print("encrypted_tensor.decrypt.tolist:")
print(encrypted_tensor.decrypt().tolist())
print()

# 3. Compute on Encrypted Tensors

encrypted_result = (encrypted_tensor + 2) * -3 - plain_tensor
expected_result = (plain_tensor + 2) * -3 - plain_tensor
print(encrypted_result.decrypt().tolist())
# [[-3.2258715329047387, -5.211344710933246, -3.277498460263318],
#  [-3.320211576555451, -11.521684756232458, -5.796486356321944]]

print(expected_result)
# [[ -3.22587101  -5.21134399  -3.27749793]
#  [ -3.32021105 -11.52168339  -5.79648557]]

print("inner product:")
# inner product
vec1 = np.random.randn(5)
vec2 = np.random.randn(5)
enc_vec1 = ts.ckks_tensor(context, vec1)
enc_vec2 = ts.ckks_tensor(context, vec2)
print("result:", enc_vec1.dot(enc_vec2).decrypt().tolist())
print("expected:", vec1.dot(vec2))

# result: 0.2651245105129444
# expected: 0.2651244888032714

print()

# 4. Batched computation

# a single ciphertext can hold up to `poly_modulus_degree / 2` values
# so let's use all the slots available
batch_size = 8192 // 2 #  4096
mat1 = np.random.randn(batch_size, 2, 3)
mat2 = np.random.randn(3, 4)
# batch is by default set to False, we have to turn it on to use the packing feature of ciphertexts
enc_mat1 = ts.ckks_tensor(context, mat1, batch=True)
enc_mat2 = ts.ckks_tensor(context, mat2)
# let's just compare the first result matrix in the batch
print("result:", enc_mat1.dot(enc_mat2).decrypt().tolist()[0])
print("expected:", mat1.dot(mat2)[0])

# result: [[1.871707310741, -1.64646640599, 0.907704175882, 1.041594801418], 
#          [-1.568004632635, 1.12713712214, -1.687649218268, -0.580647184131]]
# expected: [[ 1.87170707 -1.64646619  0.90770405  1.04159466]
#            [-1.56800442  1.12713697 -1.68764899 -0.58064711]]
print()

# 5. More Details
# 5.1 Parallel Computation
non_parallel_context = ts.context( ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[60, 40, 40, 60], n_threads=1, )


# 5.2 Decryption
sk = context.secret_key()
context.make_context_public()

# now let's try decryption
# enc_mat1.decrypt()
# raises ValueError: the current context of the tensor doesn't hold a secret_key, please provide one as argument

# now we need to explicitly pass the secret-key
enc_mat1.decrypt(sk)
# returns <tenseal.tensors.plaintensor.PlainTensor at 0x7f391eb8dc70>

# 5.3 Serialization
ser_context = context.serialize()
print(type(ser_context))
# bytes

ser_tensor = encrypted_tensor.serialize()
print(type(ser_tensor))
# bytes

loaded_context = ts.context_from(ser_context)
print(loaded_context)
# <tenseal.enc_context.Context at 0x7f391eb8dfa0>

loaded_enc_tensor = ts.ckks_tensor_from(loaded_context, ser_tensor)

# However, there is also a way to do it the lazy way, deserializing, then linking it to a specific context
lazy_loaded_enc_tensor = ts.lazy_ckks_tensor_from(ser_tensor)
# try to operate on a tensor that in not linked to a context yet
lazy_loaded_enc_tensor + 5
# raises ValueError: missing context

# You have to first link it
lazy_loaded_enc_tensor.link_context(loaded_context)
lazy_loaded_enc_tensor + 5
# returns <tenseal.tensors.ckkstensor.CKKSTensor at 0x7f391eb8d1f0>
