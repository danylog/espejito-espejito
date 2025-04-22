import tensorflow as tf
from keras.models import load_model

model = load_model('fer.h5')
tf.saved_model.save(model, 'saved_model/')