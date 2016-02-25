__author__ = 'igor'
from setuptools import setup
import os
import io
here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    seq = kwargs.get('seq', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return seq.join(buf)

# 长描述
long_description = read('README.txt', 'CHANGES.txt')

setup(
    name='IgorNLP',
    version='0.1',
    url='https://github.com/IgowWang/IgorNLP',
    license='',
    author='igor',
    install_requires=['nltk','jieba'],
    author_email='125942418@qq.com',
    description='natural language processing algorithms library and tools',
    long_description=long_description,
)

