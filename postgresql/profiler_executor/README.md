# postgresql-profiler-executor

Executes the postgresql2datacatalog connector profiler.

## Activate your virtualenv if it’s not up
```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

## Install the requirements for the metadata generator
```bash
pip install ./lib/metrics_collector-0.0.1-py3-none-any.whl
```

## environment variables

Replace below values according to your environment:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=data_catalog_credentials_file

export POSTGRESQL2DC_DATACATALOG_PROJECT_ID=google_cloud_project_id
export POSTGRESQL2DC_DATACATALOG_LOCATION_ID=google_cloud_location_id
export POSTGRESQL2DC_SQLSERVER_SERVER=sqlserver_server
export POSTGRESQL2DC_SQLSERVER_USERNAME=sqlserver_username
export POSTGRESQL2DC_SQLSERVER_PASSWORD=sqlserver_password
export POSTGRESQL2DC_SQLSERVER_DATABASE=sqlserver_database
```

## Run the script
```bash
python profiler_executor.py --datacatalog-project-id=$POSTGRESQL2DC_DATACATALOG_PROJECT_ID --datacatalog-location-id=$POSTGRESQL2DC_DATACATALOG_LOCATION_ID --sqlserver_host=$POSTGRESQL2DC_SQLSERVER_SERVER --sqlserver_user=$POSTGRESQL2DC_SQLSERVER_USERNAME --sqlserver_pass=$POSTGRESQL2DC_SQLSERVER_PASSWORD --sqlserver_database=$POSTGRESQL2DC_SQLSERVER_DATABASE
```

## Developer environment

### Install and run Yapf formatter

```bash
pip install --upgrade yapf

# Auto update files
yapf --in-place profiler_executor.py

# Show diff
yapf --diff profiler_executor.py

# Set up pre-commit hook
# From the root of your git project.
curl -o pre-commit.sh https://raw.githubusercontent.com/google/yapf/master/plugins/pre-commit.sh
chmod a+x pre-commit.sh
mv pre-commit.sh .git/hooks/pre-commit
```

### Install and run Flake8 linter

```bash
pip install --upgrade flake8
flake8 profiler_executor.py
```
