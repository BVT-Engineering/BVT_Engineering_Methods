from setuptools import setup, find_packages

setup(
    name="BVT_Engineering_Methods",
    version="0.6dev",
    packages=find_packages(),
    install_requires=["numpy", "pandas","https://github.com/sambamford-bvtengineering/BVT_Engineering_Methods/blob/main/BVT_Engineering_Methods/asnzs_1170_0_2002.py"],
)
