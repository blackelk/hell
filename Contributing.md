```
git clone git@github.com:blackelk/hell.git

pip install -r requirements-dev.txt

pylint hell.py
pytest tests
pylint tests/test_*
```

# Packaging
In `pyproject.toml` append `.dev1` to `version`, or increase number if there is already `.devN`.
```
rm -r hell.egg-info dist
python -m build
virtualenv /tmp/try_hell_wheel
source /tmp/try_hell_wheel/bin/activate
pip install dist/hell-*.whl
twine upload  --verbose --repository testpypi dist/*
```
