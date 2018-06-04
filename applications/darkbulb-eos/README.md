Steps to create nested instance image:

```
gcloud compute instances create nested-centos-7 --zone europe-west1-d \
              --image-family centos-7 --image-project=centos-cloud

gcloud compute instances stop nested-centos-7 --zone europe-west1-d

gcloud compute images create nested-centos-7 --family centos-7 \
  --source-disk nested-centos-7 --source-disk-zone europe-west1-d \
  --licenses "https://www.googleapis.com/compute/v1/projects/vm-options/global/licenses/enable-vmx"

gcloud compute instances create nested-rhel-7 --zone europe-west1-d \
              --image-family=rhel-7 --image-project=rhel-cloud

gcloud compute instances stop nested-rhel-7 --zone europe-west1-d

gcloud compute images create nested-rhel-7 --family rhel-7 \
  --source-disk nested-rhel-7 --source-disk-zone europe-west1-d \
  --licenses "https://www.googleapis.com/compute/v1/projects/vm-options/global/licenses/enable-vmx"
```
