
#!/usr/bin/env bash
docker build -t teradata-datacatalog-cleaner .
docker tag teradata-datacatalog-cleaner gcr.io/my-project/teradata-datacatalog-cleaner:stable
docker push gcr.io/my-project/teradata-datacatalog-cleaner:stable
gcloud container images list-tags gcr.io/my-project/teradata-datacatalog-cleaner