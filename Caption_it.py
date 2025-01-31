#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import numpy as np
import keras
import json
import pickle
from keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.preprocessing import image
from tensorflow.keras.preprocessing import image
from keras.models import Model, load_model
from tensorflow.keras.utils import pad_sequences
from keras.utils import to_categorical
from keras.layers import Input, Dense, Dropout, Embedding, LSTM
from tensorflow.keras.layers import concatenate


# In[12]:


model = load_model("E:\Projects\image-captioning-master/model_weights/model_9.h5")
model.make_predict_function()

# In[13]:


model_temp = ResNet50(weights="imagenet", input_shape=(224,224,3))


# In[14]:


model_resnet=Model(model_temp.input,model_temp.layers[-2].output)
model_resnet.make_predict_function()


# In[15]:


def preprocess_image(img):
    img = image.load_img(img, target_size=(224,224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img


# In[19]:


def encode_image(img):
    img = preprocess_image(img)
    feature_vector = model_resnet.predict(img)
    feature_vector = feature_vector.reshape(1,feature_vector.shape[1])
    return feature_vector


# In[26]:


with open("E:\Projects\image-captioning-master/storage/word_to_idx.pkl","rb") as w2i:
    word_to_idx=pickle.load(w2i)
with open("E:\Projects\image-captioning-master/storage/idx_to_word.pkl","rb") as i2w:
    idx_to_word=pickle.load(i2w)


# In[ ]:





# In[28]:


def predict_caption(photo):
    in_text = "startseq"
    max_len=35
    for i in range(max_len):
        sequence = [word_to_idx[w] for w in in_text.split() if w in word_to_idx]
        sequence = pad_sequences([sequence], maxlen=max_len, padding='post')

        ypred =  model.predict([photo,sequence])
        ypred = ypred.argmax()
        word = idx_to_word[ypred]
        in_text+= ' ' +word
        
        if word =='endseq':
            break
        
        
    final_caption =  in_text.split()
    final_caption = final_caption[1:-1]
    final_caption = ' '.join(final_caption)
    
    return final_caption


# In[31]:


def caption_this_image(image):
    enc=encode_image(image)
    caption=predict_caption(enc)

    return caption


# In[ ]:




