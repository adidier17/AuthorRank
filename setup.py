from setuptools import setup

setup(
    name='author_rank',
    packages=['author_rank'],
    version='0.0.1',
    description='',
    author='Annie Didier, Valentino Constantinou',
    author_email='akdidier@jpl.caltech.edu',
    url='https://github.com/adidier17/AuthorRank',
    download_url='https://github.com/adidier17/AuthorRank/archive/0.0.1.tar.gz',
    keywords=['author_rank', 'PageRank', 'network', 'graph', 'edges', 'nodes', 'authorship', 'author_rank'],
    classifiers=[],
    license='MIT',
    install_requires=['networkx', 'numpy', 'scikit-learn']
)
