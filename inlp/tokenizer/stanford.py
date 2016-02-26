# -*- coding: utf-8 -*-
# IgorNLP: Interface to the Stanford Tokenizer
# 斯坦福中文分词器接口
#
# Author: Igor

import tempfile
import os
import json
from subprocess import PIPE

from nltk import compat
from nltk.internals import find_jar, config_java, java, _java_options, find_jars_within_path

from inlp.tokenizer.api import TokenizerI


class StanfordChTokenizer(TokenizerI):
    '''
    Interface to Stanford Tokenizer

    Stanford version:2015-12-09

    segmenter_path = os.path.join(root, 'PATH-OF-StanfordSegmenter/stanford-segmenter/')
    segmenter = StanfordChTokenizer(
        path_to_jar=segmenter_path,
        path_to_sihan_corpora_dict=os.path.join(segmenter_path, 'data'),
        path_to_model=os.path.join(segmenter_path, 'data', 'pku.gz'),
        path_to_dict=os.path.join(segmenter_path, 'data', 'dict-chris6.ser.gz')
    )
    string = "这是斯坦福中文分词器"
    tokens = segmenter.tokenize(string)
    print(tokens)

    return:这 是 斯坦福 中文 分词器


    '''

    def __init__(self, path_to_jar=None, path_to_sihan_corpora_dict=None,
                 path_to_model=None, path_to_dict=None,
                 encoding='utf8', options=None,
                 verbose=False, java_options='-mx2g'):
        # self._stanford_jar = find_jar(
        #     self._JAR, path_to_jar,
        #     env_vars=('STANFORD_SEGMENTER'),
        #     searchpath=(),
        #     verbose=verbose
        # )
        self._stanford_jar = find_jars_within_path(path_to_jars=path_to_jar)
        self._sihan_corpora_dict = path_to_sihan_corpora_dict
        self._model = path_to_model
        self._dict = path_to_dict
        self._encoding = encoding
        self._java_options = java_options
        options = {} if options is None else options
        self._options_cmd = ','.join('{0}={1}'.format(key, json.dumps(val))
                                     for key, val in options.items())

    def segment_file(self, input_file_path):
        '''
        为文件分词
        构造cmd命令,执行返回标准输出
        :param input_file_path:输入的文件
        :return:分词后的结果
        '''
        cmd = [
            'edu.stanford.nlp.ie.crf.CRFClassifier',
            '-sighanCorporaDict', self._sihan_corpora_dict,
            '-textFile', input_file_path,
            '-sighanPostProcessing', 'true',
            '-keepAllWhitespaces', 'false',
            '-loadClassifier', self._model,
            '-serDictionary', self._dict
        ]

        stdout = self._execute(cmd)

        return stdout

    def tokenize(self, s):
        return self.tokenize_sents([s])[0]

    def tokenize_sents(self, strings):
        encoding = self._encoding
        # Create a temporary input file
        _input_fh, self._input_file_path = tempfile.mkstemp(text=True)

        # Write the actural sentences to the temporary input file
        _input_fh = os.fdopen(_input_fh, 'wb')
        _input = '\n'.join(''.join(x) for x in strings)
        if isinstance(_input, compat.text_type) and encoding:
            _input = _input.encode(encoding)
        _input_fh.write(_input)
        _input_fh.close()

        cmd = [
            'edu.stanford.nlp.ie.crf.CRFClassifier',
            '-sighanCorporaDict', self._sihan_corpora_dict,
            '-textFile', self._input_file_path,
            '-sighanPostProcessing', 'true',
            '-keepAllWhitespaces', 'false',
            '-loadClassifier', self._model,
            '-serDictionary', self._dict
        ]

        stdout = self._execute(cmd)

        # Delete the temporary file
        os.unlink(self._input_file_path)

        return [s.split() for s in stdout.split('\n')][:-1]

    def _execute(self, cmd, verbose=False):
        encoding = self._encoding
        cmd.extend(['-inputEncoding', encoding])
        _options_cmd = self._options_cmd
        if _options_cmd:
            cmd.extend(['-options', self._options_cmd])

        default_options = ''.join(_java_options)

        # Configure java
        config_java(options=self._java_options, verbose=verbose)
        print(self._stanford_jar)
        stdout, _stderr = java(cmd, classpath=self._stanford_jar, stdout=PIPE, stderr=PIPE)
        stdout = stdout.decode(encoding)

        # Return java configurations to their default values
        config_java(options=default_options, verbose=False)

        return stdout


if __name__ == '__main__':
    from inlp import root

    # Unit test
    # You have to set the right "Data" path that have stanford-segmenter root
    segmenter_path = os.path.join(root, 'Data/stanford-segmenter/')
    segmenter = StanfordChTokenizer(
        path_to_jar=segmenter_path,
        path_to_sihan_corpora_dict=os.path.join(segmenter_path, 'data'),
        path_to_model=os.path.join(segmenter_path, 'data', 'pku.gz'),
        path_to_dict=os.path.join(segmenter_path, 'data', 'dict-chris6.ser.gz')

    )
    string = "这是斯坦福中文分词器"
    tokens = segmenter.tokenize(string)
    print(tokens)
    strings = ["这是斯坦福中文分词器", "斯坦福分词器接口调用"]
    tokens = segmenter.tokenize_sents(strings)
    print(tokens)
