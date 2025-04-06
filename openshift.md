# Download 

curl -O https://developers.redhat.com/content-gateway/file/pub/openshift-v4/clients/crc/latest/crc-linux-amd64.tar.xz

~~~
mv pull-secret.txt rhpull-secret.json
~~~

Run `crc setup` to set up your host operating system for the OpenShift Local virtual machine.

Then, `run crc` start to create a minimal OpenShift 4 cluster on your computer
