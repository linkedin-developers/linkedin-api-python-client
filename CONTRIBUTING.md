# Contributing

This contributing guide is meant for internal LinkedIn maintainers. We are not currently accepting contributions from outside of LinkedIn at this time. If you are not a LinkedIn engineer, we appreciate your interest in our library and encourage you to provide bug reports or suggestions by opening an issue in the GitHub repo.

## Local Setup

Here are instructions for setting up the project on your local machine for testing and development.

1. Clone the project into a new directory: `git clone https://github.com/linkedin-developers/linkedin-api-python-client.git`
2. Install `poetry` on your machine: `pip install --user poetry`
3. From the project root directory, install all the packages: `poetry install`
4. Install git hook scripts: `poetry run pre-commit install`

Here are some other useful commands:
- Activate your virtual environment from the project root directory: `poetry shell`
- Run tests or examples. For example, inside the activated virtual environment: `python3 examples/get-profile.py`
- Deactivate your virtual environment at any time using `exit`
- Run pre-commit checks on all files: `poetry run pre-commit run --all-files`
- To install packages exactly as specified in poetry.lock: `poetry install`
- To upgrade packages to latest versions and update the poetry.lock: `poetry update`

## Commits and PRs

Pre-commit checks perform linting, some of which requires python. To avoid issues, make sure you run `poetry shell` before creating a commit.

Please follow [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for standardized commit messages.

## Documentation

Make sure the documentation is consistent with any code changes in the same PR.

## Examples

If there are code changes that might affect the example code ([/examples](examples/)), ensure each example runs correctly, or update accordingly.

## Testing

From the project root directory, run `poetry run pytest`.

## Publishing Package to PyPI

### Pre-requisites:

- Create an account on Test PyPI
- Create an account on PyPI
- Get added as a maintainer to the project on pypi.org

### One-time setup for local environment

1. Configure Test PyPI
   1. Add test repo: `poetry config repositories.test-pypi https://test.pypi.org/legacy/`
   2. Get token to upload packages here: https://test.pypi.org/manage/account/token/
   3. Copy the token and store it in the poetry config: `poetry config pypi-token.test-pypi pypi-XXXX` (Replace the last value with actual token value)
2. Configure PyPI
   1. Get token to upload packages here: https://pypi.org/manage/account/token/
   2. Copy the token and store it in the poetry config: `poetry config pypi-token.pypi pypi-XXXX` (Replace the last value with actual token value)

### Publish

1. Bump the version in pyproject.toml: `poetry version prerelease` (for testing) or `poetry version <BUMP_RULE>` based on changes
2. Create source archive and a wheel for the package: `poetry build`
3. If you've made changes to pyproject.toml, run a check to make sure package metadata will be rendered properly on PyPI: `twine check dist/*`
4. If you want to test the package upload first:
   1. Upload to TestPyPI (will used the previously saved token): `poetry publish -r test-pypi`
   2. [Search](https://test.pypi.org/search/) for your package on TestPyPI ("linkedin-api-client") and confirm it looks good.
   3. Install and test out the published test package in a local project: For example: `python -m pip install -i https://test.pypi.org/simple linkedin-api-client==0.1.1a0`
   4. Note: You cannot overwrite existing versions in TestPyPI or PyPI, so for testing, you would need to increment the version if it already exists.
5. Once everything looks good, publish to PyPI: `poetry publish`
6. Tag and release
   1. Tag the last commit: `git tag -a v<version> -m "Release <version>" <commit-hash>`. For example: `git tag -a v0.1.0 -m "Release 0.1.0" 043cc4ea`
   2. Push the local tag: `git push origin --tags`
   3. Create a new release in the Github repo based on the tagged commit.
