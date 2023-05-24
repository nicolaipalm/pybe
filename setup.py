from setuptools import setup

if __name__ == '__main__':
    setup(
        name='pybe',
        version='1.0.0',
        license='MIT',
        description='Small package in order to benchmark python functions',
        author='Nicolai Palm',
        author_email='nicolaipalm@googlemail.com',
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Development Status:: 1 - Planning'
        ],
        python_requires='>=3.11',
        install_requires=[
            'numpy',
            'plotly',
            'tqdm',
        ],
        extras_require={
            'dev': ['pre-commit', 'flake8', 'flake8-print'],
            'test': ['pytest', 'pytest-cov'],  # "nbval"],
        },
        test_suite='tests',
        packages=['pybe'],
    )