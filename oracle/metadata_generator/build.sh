
#!/usr/bin/env bash
docker build -t oracle2datacatalog-metadata-generator .
docker tag oracle2datacatalog-metadata-generator gcr.io/my-project/oracle2datacatalog-metadata-generator:stable
docker push gcr.io/my-project/oracle2datacatalog-metadata-generator:stable
gcloud container images list-tags gcr.io/my-project/oracle2datacatalog-metadata-generator