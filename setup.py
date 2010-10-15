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
    url='http://github.com/philippWassibauer/django-support',
    license='MIT',
    version = datetime.datetime.strftime(datetime.datetime.now(), '%Y.%m.%d'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
