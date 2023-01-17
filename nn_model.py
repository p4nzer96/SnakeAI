import tensorflow as tf


class QModel(tf.keras.Model):

    def __init__(self):
        super().__init__()

        self.input_size = 900
        self.hidden_size = 200
        self.output_size = 4

        self.input_layer = tf.keras.layers.Dense(self.input_size, activation=tf.nn.relu)
        self.hidden_layer = tf.keras.layers.Dense(self.hidden_size, activation=tf.nn.relu)
        self.output_layer = tf.keras.layers.Dense(self.output_size, activation=tf.nn.softmax)

    def call(self, inputs, training=None, mask=None):
        x = self.input_layer(inputs)
        x = self.hidden_layer(x)
        return self.output_layer(x)
