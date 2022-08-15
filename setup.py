#-*- encoding: UTF-8 -*-
from setuptools import setup,find_packages
import io
from skyeye.config import VERSION


with io.open("README.md", 'r', encoding='utf-8') as f:
    long_description = f.read()
    
setup(name='skyeye',
      version= VERSION,
      description="APK扫描工具",
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='apk scanner',
      author='wangshuwen',
      author_email='wnwn7375@outlook.com',
      url='https://github.com/wangshuwen1107/skyeye',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
        'requests',
        'PyYaml'
      ],
      entry_points={
        'console_scripts':[
            'skyeye = skyeye.cli:run'
        ]
      },
)


