# IgorNLP:
natural language processing algorithms library and tools

## dependences
- nltk


## install
- 源码安装 python setup.py install
- 仅支持python3,测试只在linux平台下

## tokenizer
- 支持斯坦福中文分词器(2015-12-09),需要配置java环境和斯坦福分词路径,接口与nltk一致
```Python
segmenter_path = os.path.join(root, 'Data/stanford-segmenter/')
    segmenter = StanfordChTokenizer(
        path_to_jar=segmenter_path,
        path_to_sihan_corpora_dict=os.path.join(segmenter_path, 'data'),
        path_to_model=os.path.join(segmenter_path, 'data', 'pku.gz'),
        path_to_dict=os.path.join(segmenter_path, 'data', 'dict-chris6.ser.gz'))
string = "这是斯坦福中文分词器"
tokens = segmenter.tokenize(string)
print(tokens)
```
- 支持哈工大ltp分词器的接口,配置和编译ltp参考[ltp官网](https://github.com/HIT-SCIR/ltp)

```Python
path_ltp = '/home/igor/PycharmProjects/ltp'(ltp工程路径)
ltp = LtpTokenizer(path_to_ltp=path_ltp)
string = "这是哈工大分词器"
token = ltp.tokenize(string)
print(token)
strings = ['这是哈工大分词器。', "哈工大的分词器测试"]
token = ltp.tokenize_sents(strings)
print(token)
```

## tagger
- ltp词性标注,文件方式的调用保持ltp的输出格式方便后续依存/实体的标注,其他的接口保持和nltk相同的输出格式list(tuple(str,str))
```Python
sentences = [['这', '是', '哈工大', '分词器', '。'], ['哈工大', '的', '分词器', '测试']]
path_ltp = '/home/igor/PycharmProjects/ltp'
ltpTagger = LtpPosTagger(path_to_ltp=path_ltp)
```
- 支持crf标注,根据不同的处理认为选择特征函数,依赖于[python-crfsuite](https://github.com/tpeng/python-crfsuite),注意定制自己的特征函数，以及通过参数training_opt
调节训练的模型参数,具体的参数配置参见接口
```Python
from nltk.corpus import brown
train = brown.tagged_sents()[0:300]
tagger = CRFTagger(verbose=True)
tagger.train(train_data=train, model_file='../test/model') # model_file存储模型文件的位置

test = brown.sents()[0]
print(test)
print(tagger.tag(test))
print(tagger.tag_sents(brown.sents()[1:5]))
```

## parser
- ltp依存句法分析,注意输入结果,还没有兼容nltk的树形输出结构
```Python
sents = [[('这', 'r'), ('是', 'v'), ('哈工大', 'j'), ('分词器', 'n'), ('。', 'wp')],
             [('哈工大', 'j'), ('的', 'u'), ('分词器', 'n'), ('测试', 'v')]]
path_ltp = '/home/igor/PycharmProjects/ltp'
ltpPS = ltpParser(path_ltp)
result = ltpPS.parse_sents(sents)
print(result)
>>>
[('这', 'r', '2', 'SBV'), ('是', 'v', '0', 'HED'), ('哈工大', 'j', '4', 'ATT'), ('分词器', 'n', '2', 'VOB'), ('。', 'wp', '2', 'WP')]
```
    