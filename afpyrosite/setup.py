try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='afpyrosite',
    version='0.1',
    description='',
    keywords='Afpyro Afpy social',
    author='afpy',
    author_email='contact@afpy.org',
    url='http://afpy.org',
    license='Beerware',
    install_requires=[
        "Pylons>=1.0",
        "SQLAlchemy>=0.5",
    ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'afpyrosite': ['i18n/*/LC_MESSAGES/*.mo']},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = afpyrosite.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
