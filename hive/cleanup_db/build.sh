
#!/usr/bin/env bash
docker build -t hive-db-cleaner .
docker tag hive-db-cleaner gcr.io/my-project/hive-db-cleaner:stable
docker push gcr.io/my-project/hive-db-cleaner:stable
gcloud container images list-tags gcr.io/my-project/hive-db-cleaner