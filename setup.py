from distutils.core import setup
import datetime

""" django-support instalation script """
setup(
    name = 'django-support',
    description = 'generic support and ticket system',
    author = 'Philipp Wassibauer',
    author_email = 'phil@maptales.com',
    packages=['support','support.templatetags'],
    package_data={'support':['support/templates/support/*.html']},
    dependency_links = [
        'git://github.com/philippWassibauer/templated-emails.git#egg=templated-emails',
    ],
    url='http://github.com/philippWassibauer/django-support',
    license='MIT',
    version = "0.2",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
