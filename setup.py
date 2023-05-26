from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


if __name__ == '__main__':
    setup(
        name='pybe',
        version='0.0.2',
        license='MIT',
        description='Small package for benchmarking python functions',
        long_description=readme(),
        long_description_content_type='text/markdown',
        author='Nicolai Palm',
        author_email='nicolaipalm@googlemail.com',
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
        python_requires='>=3.9',
        install_requires=[
            'numpy',
            'plotly',
            'tqdm',
            'pandas',

        ],
        extras_require={
            'dev': ['pre-commit', 'flake8', 'flake8-print'],
            'test': ['pytest', 'pytest-cov'],  # "nbval"],
        },
        test_suite='tests',
        packages=['pybe'],
    )
