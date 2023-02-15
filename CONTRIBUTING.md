# Contributing

This contributing guide is meant for internal LinkedIn maintainers. We are not currently accepting contributions from outside of LinkedIn at this time. If you are not a LinkedIn engineer, we appreciate your interest in our library and encourage you to provide bug reports or suggestions by opening an issue in the GitHub repo.

## Local Setup

Here are instructions for setting up the project on your local machine for testing and development.

1. Clone the project into a new directory: `git clone https://github.com/linkedin-developers/linkedin-api-python-client.git`
2. Install `pipenv` on your machine: `pip install pipenv`
3. From the project root directory, create your virtual environment and install all the packages: `pipenv install --dev`
4. Activate your virtual environment from the project root directory: `pipenv shell`
5. Run tests or examples. For example: `python3 examples/get-profile.py`
6. Deactivate your virtual environment at any time using `exit`

To install packages exactly as specified in Pipfile.lock: `pipenv sync`

To upgrade packages to latest versions and update the Pipfile.lock: `pipenv update`

## Commit Messages

Please follow [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)

## Documentation

Make sure the documentation is consistent with any code changes in the same PR.

## Examples

If there are code changes that might affect the example code ([/examples](examples/)), ensure each example runs correctly, or update accordingly.

## Testing

From the project root directory, run `pytest`.

## Publishing Package to PyPI

Pre-requisites:
- Create an account on TestPyPI
- Create an account on PyPI

1. Create source archive and a wheel for the package: `python -m build`
2. If you've made changes to pyproject.toml, run a check to make sure package metadata will be rendered properly on PyPI: `twine check dist/*`
3. If you want to test the package upload first:
   1. Upload to TestPyPI (enter your account credentials): `twine upload -r testpypi dist/*`
   2. [Search](https://test.pypi.org/search/) for your package on TestPyPI and confirm it looks good.
   3. Install and test out the published test package in a local project: `python -m pip install -i https://test.pypi.org/simple linkedin-api-client`
   4. Note: You cannot overwrite existing versions in TestPyPI or PyPI, so for testing, you would need to increment the version if it already exists.
4. Once everything looks good, upload to PyPI: `twine upload dist/*`

