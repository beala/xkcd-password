from setuptools import setup

setup(
        name='xkpa',
        version='0.1.0',
        author='Alex Beal',
        author_email='alexlbeal@gmail.com',
        url='https://github.com/beala/xkcd-password',
        package_data = {
            # If any package contains *.txt or *.rst files, include them:
            '': ['*.txt', '*.rst']
        },
        packages=['xkpa'],
        license='LICENSE.txt',
        description='A tool for generating xkcd style passwords.',
        entry_points={
            'console_scripts': [
                'xkpa = xkpa.xkpa:main']
        }
)
