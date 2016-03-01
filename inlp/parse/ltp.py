# -*- coding: utf-8 -*-
# IgorNLP:ltp parse API
#
# Author: Igor

import os
import tempfile

from nltk.internals import overridden, compat

from inlp.parse.api import ParserI


class ltpParser(ParserI):
    '''
    ltp依存句法分析
    '''

    def __init__(self, path_to_ltp, path_to_model=None, threads=1,
                 encoding='utf8'):
        '''
        初始化分词模型：指定ltp的位置
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
            '--postagger-model', self._path_to_model,
        ]

        stdout = self._execute(cmd)
        return stdout

    def parse(self, sent, *args, **kwargs):
        '''
        解析单个句子
        :param tokens:list
        :return:list(tuple(str,str))
        '''
        if overridden(self.parse_sents()):
            return self.parse_sents([sent])
        else:
            raise NotImplementedError()

    def parse_sents(self, sents, *args, **kwargs):
        '''

        :param sents:a list of sentences
        :param args:
        :param kwargs:
        :return:
        '''
