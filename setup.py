from setuptools import setup, find_packages

version = '0.1'

setup(
    name='duo_auth',

    version=version,
    description="2 Factor Auth for Django using twilio SMS",
    #long_description=open('readme').read(),
    keywords='',
    author='Preston Holmes',
    author_email='preston@ptone.com',
    url='',
    license='BSD',
    packages=find_packages(),
    # namespace_packages=[],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
