
#!/usr/bin/env bash
docker build -t hive2datacatalog-metadata-generator .
docker tag hive2datacatalog-metadata-generator gcr.io/my-project/hive2datacatalog-metadata-generator:stable
docker push gcr.io/my-project/hive2datacatalog-metadata-generator:stable
gcloud container images list-tags gcr.io/my-project/hive2datacatalog-metadata-generator