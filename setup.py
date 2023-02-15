from setuptools import find_packages, setup

setup(
  name='linkedin-api-client',
  packages=find_packages(exclude=['tests']),
  version='0.1.0',
  description='LinkedIn API Python client library',
  author='LinkedIn',
  install_requires=['requests'],
  python_requires='>=3.7',
  setup_requires=['pytest-runner'],
  tests_require=['pytest'],
  test_suite='tests'
)