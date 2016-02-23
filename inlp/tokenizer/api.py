'''
Tokenizer Interface
分词的接口
'''

from abc import ABCMeta, abstractmethod
from nltk.six import add_metaclass

from nltk.internals import overridden


@add_metaclass(ABCMeta)
class TokenizerI(object):
    '''
    a processing interface for tokenizing a string
    分词的抽象类
    Subclass must define 'tokenize()' or 'tokenize_sents()' (or both)
    '''

    @abstractmethod
    def tokenize(self, s):
        '''
        Return a tokenized copy of *s*.
        :param s: string
        :return: list of str
        '''
        if overridden(self.tokenize_sents): # 判断是否被重写
            return self.tokenize_sents([s])[0]

    def tokenize_sents(self, strings):
        '''
        Apply 'self.tokenize()' to each element of 'strings'
        :param strings:
        :return: list(list(str))
        '''
        return [self.tokenize(s) for s in strings]


class StringTokenizer(TokenizerI):
    '''
    A tokenizer that divides a string into substrings
    by specified string(defined in subclasses)
    '''

    def tokenize(self, s):
        return s.split(self._string)

