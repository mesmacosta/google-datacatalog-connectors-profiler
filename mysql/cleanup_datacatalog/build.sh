#!/usr/bin/env bash
docker build -t mysql-datacatalog-cleaner .
docker tag mysql-datacatalog-cleaner repo/mysql-datacatalog-cleaner:stable
docker push repo/mysql-datacatalog-cleaner:stable