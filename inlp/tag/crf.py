# -*- coding: utf-8 -*-
# IgorNLP: A module for tagging using CRFSuite
#
# Author: Igor

import re
import pickle

from inlp.tag.api import TaggerI

try:
    import pycrfsuite
except ImportError:
    pass


class CRFTagger(TaggerI):
    '''
    A module for tagging using CRFSuite
    '''

    def __init__(self, feature_func=None, verbose=False, training_opt={}):
        '''
        Initialize the CRF tagger

        :param feature_func:特征函数,从句子中的token中抽取特征.
            This function should take 2 parameters: tokens and index
            which extract features at index position from tokens list.
            See the build in _get_features function for more detail.
        :param verbose:output the debugging message during training
        :param training_opt:python-crfsuite training options

        Set of possible training options (using LBFGS training algorithm).
         'feature.minfreq' : The minimum frequency of features.特征的最小出现次数
         'feature.possible_states' : Force to generate possible state features.
         'feature.possible_transitions' : Force to generate possible transition features.
         'c1' : Coefficient for L1 regularization.
         'c2' : Coefficient for L2 regularization.
         'max_iterations' : The maximum number of iterations for L-BFGS optimization.
         'num_memories' : The number of limited memories for approximating the inverse hessian matrix.
         'epsilon' : Epsilon for testing the convergence of the objective.
         'period' : The duration of iterations to test the stopping criterion.
         'delta' : The threshold for the stopping criterion; an L-BFGS iteration stops when the
                    improvement of the log likelihood over the last ${period} iterations is no greater than this threshold.
         'linesearch' : The line search algorithm used in L-BFGS updates:
                           { 'MoreThuente': More and Thuente's method,
                              'Backtracking': Backtracking method with regular Wolfe condition,
                              'StrongBacktracking': Backtracking method with strong Wolfe condition
                           }
         'max_linesearch' :  The maximum number of trials for the line search algorithm.
        '''

        self._model_file = ''
        self._tagger = pycrfsuite.Tagger()

        if feature_func is None:
            self._feature_func = self._get_features
        else:
            self._feature_func = feature_func

        self._verbose = verbose
        self._training_options = training_opt
        self._pattern = re.compile(r'\d')

    def set_model_file(self, model_file):
        '''
        设置模型文件
        :param model_file:
        :return:
        '''
        self._model_file = model_file
        self._tagger.open(self._model_file)  # open a model file

    def _get_features(self, tokens, idx):
        '''
        Extract basic features about this word including
            - current word
            - next word
            - previous word
        :param tokens: 待标记的tokens
        :param idx:
        :return:a list which contains the features
        '''

        token = tokens[idx]
        feature_list = []

        if idx == 0:
            previous_word = 'START'
        else:
            previous_word = tokens[idx - 1]

        if idx == len(tokens) - 1:
            next_word = "STOP"
        else:
            next_word = tokens[idx + 1]

        feature_list.extend([previous_word, token, next_word])

        return feature_list

    def tag_sents(self, sentences):
        '''
        Tag a list of sentences
        :param sentences: list of sentences needed to tag
        :return: list(list(tuple(str,str))
        '''
        if self._model_file == '':
            raise Exception('No model file is found!!Please use train or set_model_file')

        result = []
        for tokens in sentences:
            features = [self._feature_func(tokens, i) for i in range(len(tokens))]
            lables = self._tagger.tag(features)

            if len(lables) != len(tokens):
                raise Exception("Predicted Length Not Matched,Expect Errors!")

            tagged_sent = list(zip(tokens, lables))
            result.append(tagged_sent)
        return result

    def tag(self, tokens):
        return self.tag_sents([tokens])[0]

    def train(self, train_data, model_file, save=None):
        '''
        Train the CRF tagger using CRFSuite
        :param train_data: is the list of annotated sentences.
        :param model_file:the model will be saved to this file.
        :param save:if save not None, save is the save path for new model
        '''

        trainer = pycrfsuite.Trainer(verbose=self._verbose)
        trainer.set_params(self._training_options)

        for sent in train_data:
            tokens, lables = zip(*sent)
            features = [self._feature_func(tokens, i) for i in range(len(tokens))]
            trainer.append(features, lables)

        trainer.train(model_file)
        self.set_model_file(model_file)
