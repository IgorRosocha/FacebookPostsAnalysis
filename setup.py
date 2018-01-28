from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = ''.join(f.readlines())

setup(
    name='FacebookPostsAnalysis',
    version='0.1',
    description='Application to analyze the posts of a Facebook page/group.',
    long_description=long_description,
    author='Igor Rosocha',
    author_email='rosocigo@fit.cvut.cz',
    keywords='facebook,group,page,post,analysis',
    license='MIT',
    url='https://github.com/IgorRosocha/FacebookPostsAnalysis',
    packages=find_packages(),
    python_requires='~=3.6',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Framework :: Jupyter',
        'Environment :: Console'
    ],
    install_requires=[
    	'jupyter',
    	'click>=6',
    	'requests'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
         'analysis = FacebookPostsAnalysis.analysis:main',
        ],
    },
)
