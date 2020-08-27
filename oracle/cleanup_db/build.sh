
#!/usr/bin/env bash
docker build -t oracle-db-cleaner .
docker tag oracle-db-cleaner gcr.io/my-project/oracle-db-cleaner:stable
docker push gcr.io/my-project/oracle-db-cleaner:stable
gcloud container images list-tags gcr.io/my-project/oracle-db-cleaner