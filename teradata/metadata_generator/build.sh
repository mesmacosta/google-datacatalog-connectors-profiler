
#!/usr/bin/env bash
docker build -t teradata2datacatalog-metadata-generator .
docker tag teradata2datacatalog-metadata-generator gcr.io/my-project/teradata2datacatalog-metadata-generator:stable
docker push gcr.io/my-project/teradata2datacatalog-metadata-generator:stable
gcloud container images list-tags gcr.io/my-project/teradata2datacatalog-metadata-generator