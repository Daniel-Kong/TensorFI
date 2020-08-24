#Suppress warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import yaml
yaml.warnings({'YAMLLoadWarning': False})

import tensorflow as tf
import sys

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import numpy
rng = numpy.random

# Parameters
learning_rate = 0.01
training_epochs = 1000
display_step = 50

# Training Data
train_X = numpy.asarray([3.3,4.4,5.5,6.71,6.93,4.168,9.779,6.182,7.59,2.167,
                         7.042,10.791,5.313,7.997,5.654,9.27,3.1])
train_Y = numpy.asarray([1.7,2.76,2.09,3.19,1.694,1.573,3.366,2.596,2.53,1.221,
                         2.827,3.465,1.65,2.904,2.42,2.94,1.3])
n_samples = train_X.shape[0]

# tf Graph Input
X = tf.placeholder("float")
Y = tf.placeholder("float")

# Set model weights
W = tf.Variable(rng.randn(), name="weight")
b = tf.Variable(rng.randn(), name="bias")

# Construct a linear model
pred = tf.add(tf.multiply(X, W), b)

# Mean squared error
cost = tf.reduce_sum(tf.pow(pred-Y, 2))/(2*n_samples)
# Gradient descent
#  Note, minimize() knows to modify W and b because Variable objects are trainable=True by default
optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost)

# Initialize the variables (i.e. assign their default value)
init = tf.global_variables_initializer()

# Start training
with tf.Session() as sess:

    # Run the initializer
    sess.run(init)

    # Fit all training data
    for epoch in range(training_epochs):
        for (x, y) in zip(train_X, train_Y):
            sess.run(optimizer, feed_dict={X: x, Y: y})

        # Display logs per epoch step
        if (epoch+1) % display_step == 0:
            c = sess.run(cost, feed_dict={X: train_X, Y:train_Y})
            run_W = sess.run(W)
            run_b = sess.run(b)
            print "Epoch: " + str(epoch+1) + ", cost = " + "{:.9f}".format(c) + ", W = " + str(run_W) + "b=" + str(run_b)

    print "Optimization Finished!"
    training_cost = sess.run(cost, feed_dict={X: train_X, Y: train_Y})
    run_W = sess.run(W)
    run_b = sess.run(b)
    print "Training cost = " + str(training_cost) + ", W = " + str(run_W) + ", b = " + str(run_b) + "\n"

    # Testing example, as requested (Issue #2)
    test_X = numpy.asarray([6.83, 4.668, 8.9, 7.91, 5.7, 8.7, 3.1, 2.1])
    test_Y = numpy.asarray([1.84, 2.273, 3.2, 2.831, 2.92, 3.24, 1.35, 1.03])

    print "Testing... (Mean square loss Comparison)"
    accuracy = tf.reduce_sum(tf.pow(pred - Y, 2)) / (2 * test_X.shape[0]),
    testing_cost = sess.run(
        accuracy,
        feed_dict={X: test_X, Y: test_Y})  # same function as cost above
    print "Testing cost=" + str(testing_cost)
    print "Absolute mean square loss difference: " + str(abs(training_cost - testing_cost))

    # Calculate accuracy (before fault injections)
    acc = sess.run(accuracy, feed_dict={X: test_X, Y: test_Y})
    print "Accuracy:" + str(acc)
    import TensorFI as ti
    fi = ti.TensorFI(sess, configFileName = "/home/daniel/TensorFICopy/GUITest/config.yaml", name = "test", logLevel = 0, disableInjections = True, logDir = "/home/daniel/TensorFICopy/GUITest/faultLogs")
    fi.turnOnConfig()
    acc_no = numpy.around(sess.run(accuracy, feed_dict={X: test_X, Y: test_Y})[0], decimals=7)
    print("Accuracy (no injections): " + str(acc_no))
    fi.turnOffConfig
    fi.turnOnInjections()
    acc_fi = numpy.around(sess.run(accuracy, feed_dict={X: test_X, Y: test_Y})[0], decimals=7)
    print("Accuracy (with injections): " + str(acc_fi))
