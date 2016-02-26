# -*- coding: utf-8 -*-
# IgorNLP: Tagger Interface
#
# Author: Igor

from nltk.internals import overridden
from nltk.metrics import accuracy
from nltk.tag.util import untag


class TaggerI(object):
    '''
    A processing interface for assigning a tag to each token in a list.
    '''

    def tag(self, tokens):
        '''
        Determine the most appropriate tag sequence for the given token sequence,
        and return a corresponding list of tagged tokens
        :param tokens: list of tokens ['我','爱','北京','天安门']
        :return: list(tuple(str,str)
        '''
        if overridden(self.tag_sents):
            return self.tag_sents([tokens])[0]
        else:
            raise NotImplementedError()

    def tag_sents(self, sentences):
        '''
        Apply 'self.tag()' to each element of *sentences*
        :param sentences:一系列句子
        :return:[self.tag(sent) for sent in sentences]
        '''
        return [self.tag(sent) for sent in sentences]

    def evaluate(self, gold):
        '''
        Score the accuracy of the tagger against the gold standard.
        Strip the tags from the gold standard text,retag it using
        the tagger,then compute the accuracy score.
        :param gold: 真实的标记
        :return: 准确率
        '''
        tagged_sents = self.tag_sents(untag(sent) for sent in gold)
        gold_tokens = sum(gold, [])
        test_tokens = sum(tagged_sents, [])
        return accuracy(gold_tokens, test_tokens)

    def _check_params(self, train, model):
        if (train and model) or (not train and not model):
            raise ValueError('Must specify either training data or trained model.')
