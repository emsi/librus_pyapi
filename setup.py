from setuptools import setup, find_packages

# Load the README file's content
with open('README.MD', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Read the content of your requirements file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='librus_pyapi',
    version='0.1.1',
    packages=find_packages(exclude=("tests",)),  # Automatically find all packages
    url='',  # Add your project's URL
    license='GNU AFFERO GENERAL PUBLIC LICENSE',
    author='emsi',
    author_email='',  # Consider adding an email
    description='',  # Add a short description
    long_description=long_description,  # Use the long description from README
    long_description_content_type='text/markdown',
    install_requires=requirements,
    python_requires='>=3.6',  # Specify compatible Python versions
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries',
    ]
)
