# oracle-profiler-executor

Executes the oracle2datacatalog connector profiler.

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

export ORACLE2DC_DATACATALOG_PROJECT_ID=google_cloud_project_id
export ORACLE2DC_DATACATALOG_LOCATION_ID=google_cloud_location_id
export ORACLE2DC_ORACLE_SERVER=my_oracle_server
export ORACLE2DC_ORACLE_SERVER_PORT=1521
export ORACLE2DC_ORACLE_USERNAME=system
export ORACLE2DC_ORACLE_PASSWORD=system_pwd
export ORACLE2DC_ORACLE_DATABASE_SERVICE=XEPDB1
```

## Run the script
```bash
python profiler_executor.py --datacatalog-project-id=$ORACLE2DC_DATACATALOG_PROJECT_ID --datacatalog-location-id=$ORACLE2DC_DATACATALOG_LOCATION_ID --oracle-host=$ORACLE2DC_ORACLE_SERVER --oracle-port=$ORACLE2DC_ORACLE_SERVER_PORT --oracle-user=$ORACLE2DC_ORACLE_USERNAME --oracle-pass=$ORACLE2DC_ORACLE_PASSWORD --oracle-db-service=$ORACLE2DC_ORACLE_DATABASE_SERVICE
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
