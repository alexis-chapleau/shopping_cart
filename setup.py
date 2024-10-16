from setuptools import setup, find_packages

setup(
    name='shopping_cart',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PyYAML>=5.4.1',
        'PyQt5>=5.15.0'
    ],
    python_requires='>=3.7',
    include_package_data=True,
    description='A shopping cart application',
    author='Alexis Gervais-Chapleau',
    author_email='alexis.chapleau@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
