# -*- coding: utf-8 -*-
# IgorNLP: 
# ltp分词接口,pipe方式
# Author: Igor

import subprocess
import os
import tempfile
from subprocess import PIPE

from nltk import compat

from inlp.tokenizer.api import TokenizerI
from inlp.utils import ltp_cmd


class LtpTokenizer(TokenizerI):
    '''
    哈工大ltp分词器接口

    ltp的工程路径，默认情况下模型放在/home/igor/PycharmProjects/ltp/ltp_data中
    path_ltp = '/home/igor/PycharmProjects/ltp'
    ltp = LtpTokenizer(path_to_ltp=path_ltp)
    string = "这是哈工大分词器"
    token = ltp.tokenize(string)
    print(token)
    strings = ['这是哈工大分词器。', "哈工大的分词器测试"]
    token = ltp.tokenize_sents(strings)
    print(token)

    return：
    这	是	哈工大	分词器

    这	是	哈工大	分词器	。
    哈工大	的	分词器	测试
    '''

    def __init__(self, path_to_ltp, path_to_model=None, path_to_lexicon=None, threads=1,
                 encoding='utf8'):
        '''
        初始化分词模型：指定ltp的位置
        :param path_to_ltp: ltp工程的根目录
        :param path_to_model: ltp分词模型
        :param path_to_lexicon: 人工添加指定的词典
        '''
        self._path_to_ltp = path_to_ltp
        self._path_to_model = path_to_model
        self._path_to_lexicon = path_to_lexicon
        self._threads = threads
        self._encoding = encoding

    def segment_file(self, input_file_path):
        '''
        为文件分词
        构造cmd命令,执行返回标准输出
        :param input_file_path:输入的文件
        :return:分词后的结果
        '''
        if self._path_to_model is None:
            self._path_to_model = os.path.join(self._path_to_ltp, 'ltp_data/cws.model')
        cws_cmdline = os.path.join(self._path_to_ltp, 'bin/examples/cws_cmdline')
        cmd = [
            cws_cmdline,
            '--input', input_file_path,
            '--threads', repr(self._threads),
            '--segmentor-model', self._path_to_model,
        ]
        if self._path_to_lexicon:
            cmd.extend(['--segmentor-lexicon', self._path_to_lexicon])

        stdout = self._execute(cmd)

        return stdout

    def tokenize(self, s):
        return self.tokenize_sents([s])[0]

    def tokenize_sents(self, strings):
        encoding = self._encoding

        # create temporary input file
        _input_fh, self._input_file_path = tempfile.mkstemp(text=True)

        # Write the actural sentences to the temporary input file
        _input_fh = os.fdopen(_input_fh, 'wb')
        _input = '\n'.join(''.join(x) for x in strings)
        if isinstance(_input, compat.text_type) and encoding:
            _input = _input.encode(encoding)
        _input_fh.write(_input)
        _input_fh.close()

        stdout = self.segment_file(self._input_file_path)

        return [s.split() for s in stdout.strip().split('\n')]

    def _execute(self, cmd):
        encoding = self._encoding
        stdout, _stderr = ltp_cmd(cmd, stdout=PIPE, stderr=PIPE)
        stdout = stdout.decode(encoding)


        return stdout


if __name__ == '__main__':
    path_ltp = '/home/igor/PycharmProjects/ltp'
    ltp = LtpTokenizer(path_to_ltp=path_ltp)
    string = "这是哈工大分词器"
    token = ltp.tokenize(string)
    print(token)
    strings = ['这是哈工大分词器。', "哈工大的分词器测试"]
    token = ltp.tokenize_sents(strings)
    print(token)

    # file_path = '../test/10000.txt'

    # print(ltp.segment_file(file_path))
