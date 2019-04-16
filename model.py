#!/usr/bin/env python
# -*- coding:utf-/ -*-
__author__ = '&USER'
from bb.dataDeal import DataDeal
from bb.layer import Layer
import tensorflow as tf
import numpy as np


class Model:
    # 梯度
    gradient = 0.01

    # 迭代次数
    n_batch = 5000

    # 危险度阈值
    riskThre = 0.25

    # 数据维度
    column_shape = 6
    row_shape = 0

    # 数据直方图
    def variable_summaries(self, var):
        with tf.name_scope('summaries'):
            mean = tf.reduce_mean(var)
            with tf.name_scope('stddev'):
                stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
            tf.summary.scalar('stddev', stddev)
            tf.summary.scalar('max', tf.reduce_max(var))
            tf.summary.scalar('min', tf.reduce_min(var))
            tf.summary.histogram('histogram', var)

    def train_model(self):
        # 数据处理实例
        dataDeal = DataDeal()
        # 数据处理
        train_data = dataDeal.readData(self.column_shape)
        train_data = dataDeal.normalization(train_data)
        train_data = np.array(train_data)
        train_data = dataDeal.preTreatment(train_data)

        x_data = train_data[:, [0, 1, 2, 3, 4]]
        y_data = train_data[:, [5]]

        # 接收
        with tf.name_scope('input'):
            x = tf.placeholder(tf.float32, [None, 5], name='x_input')
            y = tf.placeholder(tf.float32, [None, 1], name='y_input')

        # 隐藏层实例
        layerIns = Layer()

        # 第一层隐藏层
        with tf.name_scope('layer_1'):
            with tf.name_scope('weight_l1'):
                weights_l1 = layerIns.weight_variable([5, 1024], 'weight_l1')
                self.variable_summaries(weights_l1)
            with tf.name_scope('biases_l1'):
                biases_l1 = layerIns.biase_variable([1024], 'biases_l1')
                self.variable_summaries(biases_l1)
            with tf.name_scope('result_l1'):
                result_l1 = layerIns.addlayer(x, weights_l1, biases_l1, 'result_l1', activation_function=tf.nn.relu)
        # result_l1 = layerIns.addlayer(x, weights_l1, biases_l1, activation_function=tf.nn.softmax)
        # result_l1 = layerIns.addlayer(x, weights_l1, biases_l1, activation_function=tf.nn.tanh)

        # 第二层隐藏层
        with tf.name_scope('layer_2'):
            with tf.name_scope('weights_l2'):
                weights_l2 = layerIns.weight_variable([1024, 128], 'weight_l2')
                self.variable_summaries(weights_l2)
            with tf.name_scope('biases_l2'):
                biases_l2 = layerIns.biase_variable([128], 'biases_l2')
                self.variable_summaries(biases_l2)
            with tf.name_scope('result_l2'):
                result_l2 = layerIns.addlayer(result_l1, weights_l2, biases_l2, 'result_l2',
                                              activation_function=tf.nn.sigmoid)
        # result_l2 = layerIns.addlayer(result_l1, weights_l2, biases_l2, activation_function=tf.nn.tanh)

        # 第三层隐藏层
        with tf.name_scope('layer_3'):
            with tf.name_scope('weight_l3'):
                weights_l3 = layerIns.weight_variable([128, 1], 'weight_l3')
                self.variable_summaries(weights_l3)
            with tf.name_scope('biases_l3'):
                biases_l3 = layerIns.biase_variable([1], 'biases_l3')
                self.variable_summaries(biases_l3)
            with tf.name_scope('prediction'):
                prediction = layerIns.addlayer(result_l2, weights_l3, biases_l3, 'prediction', activation_function=None)

        # 损失函数
        with tf.name_scope('loss'):
            loss = tf.reduce_mean(tf.reduce_sum(tf.square(prediction - y), reduction_indices=[1]), name='loss')
            tf.summary.scalar('loss', loss)
        # loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=prediction))

        # 训练
        with tf.name_scope('train_step'):
            train_step = tf.train.GradientDescentOptimizer(self.gradient).minimize(loss)

        # 合并所有的summary
        merged = tf.summary.merge_all()

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            # 模型保存.
            saver = tf.train.Saver(max_to_keep=1)
            writer = tf.summary.FileWriter('logs/', sess.graph)
            for epoch in range(self.n_batch):
                summary, _ = sess.run([merged, train_step], feed_dict={x: x_data, y: y_data})
                prediction_value = sess.run(prediction, feed_dict={x: x_data, y: y_data})
                loss_value = sess.run(loss, feed_dict={x: x_data, y: y_data})
                writer.add_summary(summary, epoch)
                if epoch % 200 == 0:
                    print("loss value is " + str(loss_value))
            saver.save(sess, 'model/design_model')
            print("the matrix is:")
            for i in range(y_data.shape[0]):
                print('{0:.5f},{1:.5f}'.format(prediction_value[i][0], y_data[i][0]))

    def collision_prediction(self, sample):
        with tf.Session() as sess:
            ckpt_state = tf.train.get_checkpoint_state('./model/')
            if ckpt_state:
                saver = tf.train.import_meta_graph('./model/design_model.meta')
                graph = tf.get_default_graph()
                x_input = graph.get_tensor_by_name('input/x_input:0')
                prediction = graph.get_tensor_by_name('layer_3/prediction/prediction:0')
                saver.restore(sess, tf.train.latest_checkpoint('./model/'))
                risk_index = sess.run(prediction, feed_dict={x_input: sample})
                if risk_index > 1:
                    risk_index = 1
                return risk_index
