from setuptools import setup, find_packages
version = '0.4.1.dev0'

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
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Framework :: Plone :: 5.0",
          "Framework :: Plone :: 5.1",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
      ],
      keywords='Plone content diagnosis',
      author='Godefroid Chapelle',
      author_email='gotcha@bubblenet.be',
      url='https://github.com/collective/collective.jekyll',
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
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
