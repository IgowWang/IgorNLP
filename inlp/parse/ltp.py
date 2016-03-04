# -*- coding: utf-8 -*-
# IgorNLP:ltp parse API
#
# Author: Igor

import os
import tempfile
from subprocess import PIPE

from nltk.internals import overridden, compat

from inlp.parse.api import ParserI
from inlp.utils import ltp_cmd


class LtpParser(ParserI):
    '''
    ltp依存句法分析

    sents = [[('这', 'r'), ('是', 'v'), ('哈工大', 'j'), ('分词器', 'n'), ('。', 'wp')],
             [('哈工大', 'j'), ('的', 'u'), ('分词器', 'n'), ('测试', 'v')]]
    path_ltp = '/home/igor/PycharmProjects/ltp'
    ltpPS = ltpParser(path_ltp)
    result = ltpPS.parse_sents(sents)
    print(result)

    >>>
            这	r	2	SBV
        是	v	0	HED
        哈工大	j	4	ATT
        分词器	n	2	VOB
        。	wp	2	WP

        哈工大	j	3	ATT
        的	u	1	RAD
        分词器	n	4	ATT
        测试	v	0	HED
    '''

    def __init__(self, path_to_ltp, path_to_model=None, threads=1,
                 encoding='utf8'):
        '''
        初始化依存分析模型：指定ltp的位置
        :param path_to_ltp: ltp工程的根目录
        :param path_to_model: ltp依存分析模型
        '''
        self._path_to_ltp = path_to_ltp
        self._path_to_model = path_to_model
        self._threads = threads
        self._encoding = encoding

    def parse_file(self, input_file_path):
        '''
        为分词和词性标注后的文件进行依存分析
        构造cmd命令,执行返回标准输出
        :param input_file_path:输入的文件
        :return:依存分析后的结果
        '''
        if self._path_to_model is None:
            self._path_to_model = os.path.join(self._path_to_ltp, 'ltp_data/parser.model')
        cws_cmdline = os.path.join(self._path_to_ltp, 'bin/examples/par_cmdline')
        cmd = [
            cws_cmdline,
            '--input', input_file_path,
            '--threads', repr(self._threads),
            '--parser-model', self._path_to_model,
        ]

        stdout = self._execute(cmd)
        return stdout

    def parse(self, sent, *args, **kwargs):
        '''
        解析单个句子
        :param tokens:list
        :return:list(tuple(str,str))
        '''
        if overridden(self.parse_sents):
            return self.parse_sents([sent])[0]
        else:
            raise NotImplementedError()

    def parse_sents(self, sentences, *args, **kwargs):
        '''

        :param sents:a list of sentences
        :type [[(str,str),..,],[]]
        :param args:
        :param kwargs:
        :return:
        '''
        encoding = self._encoding

        # create temporary input file
        _input_fh, self._input_file_path = tempfile.mkstemp(text=True)

        # Write the actural sentences to the temporary input file
        _input_fh = os.fdopen(_input_fh, 'wb')

        _input = '\n'.join(['\t'.join(['_'.join(token) for token in sent]) for sent in sentences])
        # print(_input)
        if isinstance(_input, compat.text_type) and encoding:
            _input = _input.encode(encoding)
        _input_fh.write(_input)
        _input_fh.close()

        stdout = self.parse_file(self._input_file_path)

        return [[tuple(token.split()) for token in sent.split('\n')] for sent in stdout.strip().split('\n\n')]

    def _execute(self, cmd):
        encoding = self._encoding
        stdout, _stderr = ltp_cmd(cmd, stdout=PIPE, stderr=PIPE)
        stdout = stdout.decode(encoding)

        return stdout


if __name__ == '__main__':
    sents = [[('这', 'r'), ('是', 'v'), ('哈工大', 'j'), ('分词器', 'n')],
             [('哈工大', 'j'), ('的', 'u'), ('分词器', 'n'), ('测试', 'v')]]
    #
    # string = '\n'.join(['\t'.join([ '_'.join(token) for token in sent]) for sent in sents])
    # print(string)
    path_ltp = '/home/igor/PycharmProjects/ltp'
    ltpPS = LtpParser(path_ltp)
    result = ltpPS.parse_sents(sents)
    print(result)
    result = ltpPS.parse(sents[0])
    print(result)
    pass
