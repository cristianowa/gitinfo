from setuptools import setup, find_packages
setup(
        name='gitinfo',
        packages=find_packages(),
        scripts=["gitinfo.py"],
        version='0.1',
        description='Git info',
        author='Cristiano W. Araujo',
        author_email="cristianowerneraraujo@gmail.com",
        url='',
        install_requires=["exdict", "path.py"]
)

