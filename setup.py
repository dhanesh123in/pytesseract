import os

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess

README_PATH = 'README.rst'
LONG_DESC = ''
if os.path.exists(README_PATH):
    with open(README_PATH) as readme:
        LONG_DESC = readme.read()

INSTALL_REQUIRES = ['Pillow']
PACKAGE_NAME = 'pytesseract'
PACKAGE_DIR = 'src'

# https://blog.niteo.co/setuptools-run-custom-code-in-setup-py/

def customRun(subclass):
    old_run = subclass.run
    def new_run(self):
        try:
            # Only for ubuntu Docker builds as of now
            subprocess.check_call(["apt-get","-y","update"])
            subprocess.check_call(["apt-get","-y","install","tesseract-ocr"])
            subprocess.check_call(["apt-get","-y","install","tesseract-ocr-all"])
        except:
            pass
        old_run(self)
    
    subclass.run=new_run
    return subclass

@customRun
class customDevelop(develop):
    pass

@customRun
class customInstall(install):
    pass

setup(
    name=PACKAGE_NAME,
    version='0.3.6',
    author='Samuel Hoffstaetter',
    author_email='samuel@hoffstaetter.com',
    maintainer='Matthias Lee',
    maintainer_email='pytesseract@madmaze.net',
    description=(
        "Python-tesseract is a python wrapper for Google's Tesseract-OCR"
    ),
    long_description=LONG_DESC,
    license='Apache License 2.0',
    keywords='python-tesseract OCR Python',
    url='https://github.com/madmaze/pytesseract',
    #packages=find_packages(),
    packages=[PACKAGE_NAME],
    package_dir={PACKAGE_NAME: PACKAGE_DIR},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    entry_points={
        'console_scripts': ['{0} = {0}.{0}:main'.format(PACKAGE_NAME)],
    },
    cmdclass={
        'develop': customDevelop,
        'install': customInstall,
    },
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
