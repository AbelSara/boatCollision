#!/usr/bin/env python
# -*- coding:utf-/ -*-
__author__ = '&USER'
import tensorflow as tf


class Layer:
    def weight_variable(self, shape, name):
        weights = tf.Variable(tf.random_normal(shape=shape), name=name)
        return weights

    def biase_variable(self, shape, name):
        biases = tf.Variable(tf.zeros(shape=shape), name=name)
        return biases

    def addlayer(self, inputs, weights, biases, name, activation_function=None):
        wx_plus_b = tf.add(tf.matmul(inputs, weights), biases, name=name)
        if activation_function is None:
            outputs = wx_plus_b
        else:
            outputs = activation_function(wx_plus_b)
        return outputs
