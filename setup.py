 try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
	'author': 'Matt Harrison',
	'url': 'URL to get it',
	'download_url': 'Where to Download',
	'author_email': 'matt.harrison91@gmail.com',
	'version': '0.1',
	'install_requires': ['nose'],
	'packages': ['NAME'],
	'scripts': [],
	'name': 'projectname'
}

setup(**config)
