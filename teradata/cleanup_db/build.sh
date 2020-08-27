
#!/usr/bin/env bash
docker build -t teradata-db-cleaner .
docker tag teradata-db-cleaner gcr.io/my-project/teradata-db-cleaner:stable
docker push gcr.io/my-project/teradata-db-cleaner:stable
gcloud container images list-tags gcr.io/my-project/teradata-db-cleaner