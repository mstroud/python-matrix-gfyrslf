from distutils.core import setup

DESC='A simple, extensible chatbot for Matrix'

setup(
    name='python-matrix-gfyrslf',
    version='0.1',
    author='Matt Stroud',
    author_email='see github',
    url='https://github.com/mstroud/python-matrix-gfyrslf',
    packages=['python-matrix-gfyrslf'],
    install_requires=['matrix_client'],
    license='MIT',
    summary=DESC,
    long_description=DESC,
)
