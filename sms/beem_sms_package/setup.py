from setuptools import setup, find_packages

setup(
    name='django-beem-sms',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A Django app for sending SMS via Beem Africa',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Buckets-Tanzania-Limited/django-beem-sms',
    author='Your Name',
    author_email='your.email@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        'django>=3.0',
        'requests>=2.25.0',
    ],
)