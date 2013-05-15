import os, sys

from setuptools import setup

long_description = """
fsredis: very partial in-process implementation of the Redis API, using the
filesystem, meant to be compatible to pyredis.
(c) Holger Krekel 2013
"""
def main():
    setup(
        name='fsredis',
        description='fsredis: in-process redis api, persisting to file system.',
        long_description = long_description,
        version="0.3",
        url='http://github.com/hpk42/fsredis',
        license='MIT license',
        platforms=['unix', 'linux', 'osx', 'cygwin', 'win32'],
        author='holger krekel',
        author_email='holger at merlinux.eu',
        classifiers=['Development Status :: 3 - Alpha',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: MIT License',
                     'Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Topic :: Utilities',
                     'Intended Audience :: Developers',
                     'Programming Language :: Python'],
        py_modules = ['fsredis'],
    )

if __name__ == '__main__':
    main()

