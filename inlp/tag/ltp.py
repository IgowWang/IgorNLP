# -*- coding: utf-8 -*-
# IgorNLP:ltp 词性标注模块
#
# Author: Igor

import os
import tempfile
from subprocess import PIPE

from nltk.internals import overridden, compat

from inlp.tag.api import TaggerI
from inlp.utils import ltp_cmd


class LtpPosTagger(TaggerI):
    '''
    ltp 词性标注模块

    #test:
    sentences = [['这', '是', '哈工大', '分词器', '。'], ['哈工大', '的', '分词器', '测试']]
    path_ltp = '/home/igor/PycharmProjects/ltp'
    ltpTagger = LtpPosTagger(path_to_ltp=path_ltp)

    print(ltpTagger.tag_sents(sentences))
    print(ltpTagger.tag(['这', '是', '哈工大', '分词器', '。']))

    output:
    [[('这', 'r'), ('是', 'v'), ('哈工大', 'j'), ('分词器', 'n'), ('。', 'wp')], [('哈工大', 'j'), ('的', 'u'), ('分词器', 'n'), ('测试', 'v')]]
    [('这', 'r'), ('是', 'v'), ('哈工大', 'j'), ('分词器', 'n'), ('。', 'wp')]

    '''

    def __init__(self, path_to_ltp, path_to_model=None, path_to_lexicon=None, threads=1,
                 encoding='utf8'):
        '''
        初始化分词模型：指定ltp的位置
        :param path_to_ltp: ltp工程的根目录
        :param path_to_model: ltp词性标注模型
        :param path_to_lexicon: 人工添加指定的词典
        '''
        self._path_to_ltp = path_to_ltp
        self._path_to_model = path_to_model
        self._path_to_lexicon = path_to_lexicon
        self._threads = threads
        self._encoding = encoding

    def tag_file(self, input_file_path):
        '''
        为分词后的文件进行词性标注
        构造cmd命令,执行返回标准输出
        :param input_file_path:输入的文件
        :return:分词后的结果,保留ltp标注后的结果,方便调用下一个部件
        '''
        if self._path_to_model is None:
            self._path_to_model = os.path.join(self._path_to_ltp, 'ltp_data/pos.model')
        cws_cmdline = os.path.join(self._path_to_ltp, 'bin/examples/pos_cmdline')
        cmd = [
            cws_cmdline,
            '--input', input_file_path,
            '--threads', repr(self._threads),
            '--postagger-model', self._path_to_model,
        ]
        if self._path_to_lexicon:
            cmd.extend(['--postagger-lexicon', self._path_to_lexicon])

        stdout = self._execute(cmd)

        return stdout

    def tag(self, tokens):
        '''
        标注单个句子
        :param tokens:list
        :return:list(tuple(str,str))
        '''
        if overridden(self.tag_sents):
            return self.tag_sents([tokens])[0]
        else:
            raise NotImplementedError()

    def tag_sents(self, sentences):
        encoding = self._encoding

        # create temporary input file
        _input_fh, self._input_file_path = tempfile.mkstemp(text=True)

        # Write the actural sentences to the temporary input file
        _input_fh = os.fdopen(_input_fh, 'wb')
        _input = '\n'.join('\t'.join(x) for x in sentences)
        if isinstance(_input, compat.text_type) and encoding:
            _input = _input.encode(encoding)
        _input_fh.write(_input)
        _input_fh.close()

        stdout = self.tag_file(self._input_file_path)

        return [[tuple(token.split('_')) for token in sent.split('\t')] for sent in stdout.split('\n')[:-1]]

    def _execute(self, cmd):
        encoding = self._encoding
        stdout, _stderr = ltp_cmd(cmd, stdout=PIPE, stderr=PIPE)
        stdout = stdout.decode(encoding)

        return stdout


if __name__ == '__main__':
    sentences = [['这', '是', '哈工大', '分词器', '。'], ['哈工大', '的', '分词器', '测试']]
    path_ltp = '/home/igor/PycharmProjects/ltp'
    ltpTagger = LtpPosTagger(path_to_ltp=path_ltp)

    print(ltpTagger.tag_sents(sentences))
    print(ltpTagger.tag(['这', '是', '哈工大', '分词器', '。']))
