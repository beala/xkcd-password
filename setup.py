from setuptools import setup

setup(
        name='xkpa',
        version='0.1.1',
        author='Alex Beal',
        author_email='alexlbeal@gmail.com',
        url='https://github.com/beala/xkcd-password',
        include_package_data = True,
        package_data = {
            # If any package contains *.txt or *.rst files, include them:
            '': ['*.txt', '*.rst', '*.md'],
            #'xkpa': ['dict.txt']
        },
        packages=['xkpa'],
        license='LICENSE.txt',
        description='A tool for generating xkcd style passwords.',
        entry_points={
            'console_scripts': [
                'xkpa = xkpa.xkpa:main']
        },
        classifiers=[
            "Topic :: Security",
            "Environment :: Console",
            "Development Status :: 5 - Production/Stable",
            "License :: OSI Approved :: MIT License",
        ],
)
