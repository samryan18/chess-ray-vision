from setuptools import setup

'''
Setup for preprocessing package
'''

setup(
      name="preprocessing",
      version="0.1",
      author_email="samryan@seas.upenn.edu",
      packages=['preprocessing'],
      python_requires='>=3.4',
      install_requires=[
        'Click==7.0',
        'opencv-python==4.1.1.26',
        'tqdm'
      ],
      entry_points={
        'console_scripts':
        ['preprocess = preprocessing.preprocess:main_with_warped']
      }
)