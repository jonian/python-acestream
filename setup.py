import setuptools

with open('README.md', 'r') as fh:
  long_description = fh.read()

setuptools.setup(
  name='acestream',
  version='0.2.0',
  author='Jonian Guveli',
  author_email='jonian@hardpixel.eu',
  description='Interact with the AceStream Engine and the HTTP API',
  long_description=long_description,
  long_description_content_type='text/markdown',
  url='https://github.com/jonian/python-acestream',
  packages=setuptools.find_packages(),
  classifiers=[
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: POSIX :: Linux'
  ],
  project_urls={
    'Bug Reports': 'https://github.com/jonian/python-acestream/issues',
    'Source': 'https://github.com/jonian/python-acestream',
  }
)
