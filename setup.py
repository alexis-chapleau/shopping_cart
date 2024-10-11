from setuptools import setup, find_packages

setup(
    name='shopping_cart',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List your project's dependencies here.
        # For example: 'numpy', 'requests', etc.
    ],
    python_requires='>=3.6',
    include_package_data=True,
    description='A shopping cart application',
    author='Alexis Gervais-Chapleau',
    author_email='alexis.chapleau@gmail.com',
    url='https://github.com/alexis-chapleau/shopping_cart',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
