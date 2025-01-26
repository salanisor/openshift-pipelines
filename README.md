Within the openshift-pipelines directory designated as areas for where we’ll put each respective pipelines configurations:

* app-build
* image-build

git-secret.yaml => Openshift secret object file that specifies git creds for the repo that will contain the Dockerfile.
pipeline.yaml => Openshift pipeline object definition that defines the different tasks and execution order for the pipeline.
  * Note you’ll want to specify where the Git repository location is within pipeline.yaml on line 11.
  * An example of this pipeline should still reside in the namespace example-jboss

* Create registry authentication robot account [link](https://access.redhat.com/RegistryAuthentication)

redhat-registry-io-secret.yaml => Openshift Secret Object definition that defines credentials for access to JBoss image base from registry.redhat.io

* See official documentation [link](https://docs.redhat.com/en/documentation/red_hat_openshift_pipelines/1.17/html/securing_openshift_pipelines/authenticating-pipelines-repos-using-secrets)

1) create secret containing the Quay registry robot credentials
~~~
oc create secret docker-registry quay-registry-creds --docker-server=quay.apps.ocp4.example.com --docker-username="jboss-example+jboss_example_robot" --docker-password=GFYMM4VYJKE9DAWZTPHJVDSJ2SBBXW9EAHGX3MB8MW2FU5MTKZX2RK11DOZCO1FZ --docker-email=apps@bastion.ocp4.example.com -n jboss-example
~~~

Annotate secret
~~~
oc annotate secret quay-registry-creds tekton.dev/docker-0='quay.apps.ocp4.example.com'
~~~

Link secret to pipelines service account in the `jboss-example` namespace
~~~
oc secrets link pipeline quay-registry-creds --for=mount -n jboss-example
~~~

2) Repeat the same steps for the registry.redhat.io robot service account.

Annotate secret
~~~
oc annotate secret/tekton-pull-secret tekton.dev/docker-1='registry.redhat.io'
~~~

Link secret to pipelines service account in the `jboss-example` namespace
~~~
oc secrets link pipeline tekton-pull-secret --for=mount -n jboss-example
~~~

Adding Quarkus upload upon successful image build completion

Verify if Galleon/Jboss 8 image building streamlining can be utilized in JBoss 7.4 (Will try to get some red hat answers on my end on this one)
Adding some JBoss configuration as part of the image building process (within dockerfile)