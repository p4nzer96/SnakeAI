import tensorflow as tf


class QModel(tf.keras.Model):

    def __init__(self, input_size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dense1 = tf.keras.layers.Dense(input_size, activation=tf.nn.relu)
        self.dense2 = tf.keras.layers.Dense(4, activation=tf.nn.softmax)

    def call(self, inputs):
        x = self.dense1(inputs)
        return self.dense2(x)