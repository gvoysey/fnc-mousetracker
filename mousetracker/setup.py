from setuptools import setup, find_packages, Extension
# makes __version__ a local variable
exec(open('core/_version.py').read())
setup(
    name='mousetracker',
    version=__version__,
    packages=find_packages(),
    scripts=['scripts/analyze_bout.py',
            ],
    url='https://github.com/MEEI-SPEL/mousetracker',
    license='',
    author='Graham Voysey',
    author_email='gvoysey@bu.edu',
    description='',
    install_requires=['opencv_python',
                      'pandas',
                      'progressbar2',
                      'joblib']
)