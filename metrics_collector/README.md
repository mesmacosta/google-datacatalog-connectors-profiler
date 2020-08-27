# metrics_collectors

## Activate your virtualenv if it’s not up
```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

## Install the requirements for the metadata generator
```bash
pip install ./lib/datacatalog_connectors_commons-1.0.1-py2.py3-none-any.whl
pip install --editable .
```

## Run the script
```bash
python metrics_collector.py --project-id MY_PROJECT --location-id us-central1 --entry-group-id MY_ENTRY_GROUP --start-time '12/16/19 16:00:00' --end-time '12/16/19 17:00:00' --generate-csv true
```

## Developer environment

### Install and run Yapf formatter

```bash
pip install --upgrade yapf

# Auto update files
yapf --in-place --recursive src

# Show diff
yapf --diff --recursive src

# Set up pre-commit hook
# From the root of your git project.
curl -o pre-commit.sh https://raw.githubusercontent.com/google/yapf/master/plugins/pre-commit.sh
chmod a+x pre-commit.sh
mv pre-commit.sh .git/hooks/pre-commit
```

### Install and run Flake8 linter

```bash
pip install --upgrade flake8
flake8 src
```

### Build
```bash
python setup.py bdist_wheel --universal
```