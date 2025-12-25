"""Setup script for reconner."""

from setuptools import setup, find_packages
from pathlib import Path

readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text() if readme_file.exists() else ''

setup(
    name='reconner',
    version='1.0.0',
    description='Security reconnaissance tool orchestrator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Security Research',
    author_email='',
    url='https://github.com/yourusername/reconner',
    packages=find_packages(),
    install_requires=[
        'click>=8.0.0',
        'jinja2>=3.0.0',
        'reportlab>=3.6.0',
        'markdown>=3.4.0',
        'rich>=10.0.0',
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'reconner=reconner.cli:main',
        ],
    },
    include_package_data=True,
    package_data={
        'reconner': ['templates/*.j2'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Topic :: Security',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)

