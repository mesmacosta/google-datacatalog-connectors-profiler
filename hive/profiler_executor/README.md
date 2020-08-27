# hive-profiler-executor

Executes the hive2datacatalog connector profiler.

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

export HIVE2DC_DATACATALOG_PROJECT_ID=google_cloud_project_id
export HIVE2DC_DATACATALOG_LOCATION_ID=us-google_cloud_location_id
export HIVE2DC_HIVE_METASTORE_DB_HOST=hive_metastore_db_server
export HIVE2DC_HIVE_METASTORE_DB_USER=hive_metastore_db_user
export HIVE2DC_HIVE_METASTORE_DB_PASS=hive_metastore_db_pass
export HIVE2DC_HIVE_METASTORE_DB_NAME=hive_metastore_db_name
export HIVE2DC_HIVE_METASTORE_DB_TYPE=hive_metastore_db_type
```

## Run the script
```bash
python profiler_executor.py --datacatalog-project-id=$HIVE2DC_DATACATALOG_PROJECT_ID --datacatalog-location-id=$HIVE2DC_DATACATALOG_LOCATION_ID --hive-metastore-db-host=$HIVE2DC_HIVE_METASTORE_DB_HOST --hive-metastore-db-user=$HIVE2DC_HIVE_METASTORE_DB_USER --hive-metastore-db-pass=$HIVE2DC_HIVE_METASTORE_DB_PASS --hive-metastore-db-name=$HIVE2DC_HIVE_METASTORE_DB_NAME --hive-metastore-db-type=$HIVE2DC_HIVE_METASTORE_DB_TYPE
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
