
#!/usr/bin/env bash
docker build -t hive-datacatalog-cleaner .
docker tag hive-datacatalog-cleaner gcr.io/my-project/hive-datacatalog-cleaner:stable
docker push gcr.io/my-project/hive-datacatalog-cleaner:stable
gcloud container images list-tags gcr.io/my-project/hive-datacatalog-cleaner