import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid'
    ]

setup(name='pharaoh',
      version='0.2',
      description='Pyramid helpers, base classes, etc.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python"
          ],
      author='Nicholas Long',
      author_email='adoc@webmob.net',
      url='https://github.com/adoc/',
      keywords='pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='pharaoh',
      install_requires=requires,
      test_requires=[],
      entry_points= """\
        [pyramid.scaffold]
        srbb_stack=pharaoh.scaffolds:SrbbStack
      """
      )
