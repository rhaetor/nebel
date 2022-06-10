from setuptools import setup, find_packages

VERSION = '3.0.0'
DESCRIPTION = 'Asciidoc modular documentation utilities tool'
LONG_DESCRIPTION = 'Nebel is a Python command-line tool to automate certain routine tasks associated with creating and managing _modular documentation_. For example, you can use Nebel to create an instance of an assembly, procedure, concept, or reference file.'

# Setting up
setup(name='nebel',
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      url='https://github.com/rhaetor/nebel',
      author='Andreas Jonsson',
      author_email='ajonsson@redhat.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[],  # add any additional packages that
      # needs to be installed along with your package. Eg: 'caer'
      keywords=['python', 'nebel', 'asciidoc', 'modular'],
      classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Documentation",
            "Programming Language :: Python :: 3",
            "Operating System :: POSIX :: Linux"],
      zip_safe = False
)
