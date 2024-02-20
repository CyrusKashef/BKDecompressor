'''
Purpose:
'''

###################
##### IMPORTS #####
###################

from setuptools import find_packages, setup

####################
##### WORKFLOW #####
####################

packages = find_packages(exclude=["BKDecompressor.egg-info", "build", "dist"])

setup(
    name="BKDecompressor",
    version="0.0.1",
    description='None',
    # url='None',
    author='GiantJigglypuff3',
    # author_email='None',
    license='MIT',
    packages=packages,
    zip_safe=False,
)