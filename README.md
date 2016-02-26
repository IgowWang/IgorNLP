# IgorNLP:
natural language processing algorithms library and tools

## dependences
- nltk

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
    