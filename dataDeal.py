#!/usr/bin/env python
# -*- coding:utf-/ -*-
__author__ = '&USER'
import pandas as pd
import numpy as np

np.set_printoptions(suppress=True)


class DataDeal:
    def readData(self, column_shape):
        train_data = pd.read_csv('data.csv')
        train_data = np.array(train_data)
        agent_data = [0 for i in range(train_data.shape[0])]
        for i in range(train_data.shape[0]):
            string = str(train_data[i][0])
            string = string.replace(' ', '')
            agent_data[i] = string
        agent_data = np.array(agent_data, dtype='float32')
        row_shape = int(train_data.shape[0] / column_shape)
        res_data = [[0.0 for i in range(column_shape)] for i in range(row_shape)]
        res_data = np.array(res_data)
        for i in range(0, row_shape):
            for j in range(0, column_shape):
                column_index = i + j * row_shape
                res_data[i][j] = agent_data[column_index]
        return res_data

    def normalization(self, train_data):
        res_data = np.zeros(train_data.shape)
        min_array = train_data.min(0)
        max_array = train_data.max(0)
        row_shape = train_data.shape[0]
        column_shape = train_data.shape[1]
        for i in range(column_shape):
            minus = max_array[i] - min_array[i]
            for j in range(row_shape):
                res_data[j][i] = (train_data[j][i] - min_array[i]) / minus
        return res_data

    def preTreatment(self, train_data):
        train_data = train_data[np.lexsort(train_data.T)]
        return train_data
