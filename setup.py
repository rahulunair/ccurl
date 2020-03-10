from distutils.core import setup

setup(name="ccurl",
    version="0.1.0",
    description="Configurable curl",
    author="rahulunair",
    author_email="rahulunair@gmail.com",
    license="three-clause BSD",
    install_requires = [
        "configparser==4.0.2",
        "requests==2.23.0",
        "urllib3==1.25.8"
        ],
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Intended Audience :: Developers",
        "Topic :: Internet" ],
    py_modules=['ccurl'],)

