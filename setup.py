from setuptools import setup, find_packages
version = '0.4.0'

long_description = (
    open('docs/README.rst').read()
    + '\n' +
    'Contributors\n'
    '============\n'
    + '\n' +
    open('CONTRIBUTORS.txt').read()
    + '\n' +
    open('CHANGES.txt').read()
    + '\n')

setup(name='collective.jekyll',
      version=version,
      description="Diagnostic for your Plone content",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
      ],
      keywords='Plone content diagnosis',
      author='Godefroid Chapelle',
      author_email='gotcha@bubblenet.be',
      url='http://svn.plone.org/svn/collective/',
      license='gpl',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.app.registry',
          'beautifulsoup4',
      ],
      extras_require=dict(
          test=[
              'Products.PloneTestCase',
              'plone.app.testing',
              'plone.app.robotframework',
          ],
          pytest=[
              'pytest',
              'gocept.pytestlayer',
          ]),
      )
