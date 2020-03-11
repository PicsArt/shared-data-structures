from setuptools import setup
from setuptools import find_packages

NUMPY_MIN_VERSION = '1.16.4'
POSIX_IP_MIN_VERSION = '1.0.4'


setup(name='shared_ds',
      version='0.1',
      description='Provide shared memory data structures!',
      url='http://github.com/storborg/kalksdjlkasdkl',
      author='Vigen Sahakyan',
      author_email='vigen.sahakyan@picsart.com',
      license='MIT',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      install_requires=[
                        'numpy>={}'.format(NUMPY_MIN_VERSION),
                        'posix_ipc>={}'.format(POSIX_IP_MIN_VERSION),
                    ],
      platforms=["Linux", "Mac OS-X", "Unix"],
      zip_safe=False)
