# -*- coding: utf-8 -*-
# IgorNLP:Parser API
#
# Author: Igor

from nltk.internals import overridden


class ParserI(object):
    '''
    A processing class for deriving trees that represent possible
    structures for a sequence of tokens.
    '''

    def grammar(self):
        '''
        :return:The grammar used by this parser
        '''
        raise NotImplementedError()

    def parse(self, sent, *args, **kwargs):
        '''
        :param sent: list(str)
        :param args:
        :param kwargs:
        :return:An iterator that generates parse for the sentence.
        '''
        if overridden(self.parse_sents):
            return next(self.parse_sents([sent], *args, **kwargs))
        elif overridden(self.parse_one):
            return (tree for tree in [self.parse_one(sent, *args, **kwargs)] if tree is not None)
        elif overridden(self.parse_all):
            return iter(self.parse_all(sent, *args, **kwargs))
        else:
            raise NotImplementedError()

    def parse_sents(self, sents, *args, **kwargs):
        return (self.parse(sent, *args, **kwargs) for sent in sents)

    def parse_all(self, sent, *args, **kwargs):
        return list(self.parse(sent, *args, **kwargs))

    def parse_one(self, sent, *args, **kwargs):
        '''
        :param sent:
        :param args:
        :param kwargs:
        :return:Tree or None
        '''
        return next(self.parse(sent, *args, **kwargs), None)
