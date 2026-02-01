I can help you query etcd to check for any leftover resources from the previous OpenShift Pipelines installation. Here's how to do this:

## Query etcd for pipelines-operator namespace resources

First, you'll need to access the etcd pod. Here's the complete process:

**1. Get into an etcd pod:**
```bash
oc rsh -n openshift-etcd $(oc get pods -n openshift-etcd -l app=etcd -o jsonpath='{.items[0].metadata.name}')
```

**2. Query for all resources in the pipelines-operator namespace:**
```bash
# Search for any keys related to openshift-pipelines or pipelines-operator
etcdctl get --prefix /kubernetes.io/namespaces/openshift-pipelines
etcdctl get --prefix /kubernetes.io/namespaces/pipelines-operator
```

**3. More comprehensive search for pipeline-related resources:**
```bash
# Search across all namespaces for pipeline resources
etcdctl get --prefix "" --keys-only | grep -i pipeline
etcdctl get --prefix "" --keys-only | grep -i tekton
```

**4. Check specific resource types in the namespace:**
```bash
# Look for specific resources
etcdctl get --prefix /kubernetes.io/configmaps/openshift-pipelines
etcdctl get --prefix /kubernetes.io/secrets/openshift-pipelines
etcdctl get --prefix /kubernetes.io/serviceaccounts/openshift-pipelines
etcdctl get --prefix /kubernetes.io/deployments/openshift-pipelines
```

## Before querying etcd directly, try these safer approaches:

**Check for finalizers blocking deletion:**
```bash
oc get all,cm,secret,sa -n openshift-pipelines -o json | jq '.items[] | select(.metadata.finalizers != null) | {kind: .kind, name: .metadata.name, finalizers: .metadata.finalizers}'
```

**Check operator resources:**
```bash
oc get subscription,operatorgroup,csv -n openshift-operators | grep pipelines
oc get subscription,operatorgroup,csv -n openshift-pipelines | grep pipelines
```

**Force remove finalizers if needed (use cautiously):**
```bash
oc patch <resource-type> <resource-name> -n openshift-pipelines -p '{"metadata":{"finalizers":[]}}' --type=merge
```

Would you like me to help you interpret any specific findings or create a cleanup script based on what you discover?


Here's how to delete all Tekton-related CRDs from your OpenShift cluster:

## 1. List all Tekton CRDs

First, identify all Tekton-related CRDs:

```bash
oc get crd | grep tekton
```

Or more comprehensive search for pipeline-related CRDs:

```bash
oc get crd | grep -E 'tekton|pipeline|trigger|operator.tekton'
```

## 2. Delete all Tekton CRDs at once

**Option A: Delete by pattern (recommended):**
```bash
# Delete all tekton.dev CRDs
oc get crd -o name | grep tekton.dev | xargs oc delete

# Or be more specific
oc delete crd $(oc get crd -o name | grep tekton | cut -d'/' -f2)
```

**Option B: Delete specific common Tekton CRDs:**
```bash
oc delete crd \
  pipelines.tekton.dev \
  pipelineruns.tekton.dev \
  tasks.tekton.dev \
  taskruns.tekton.dev \
  clustertasks.tekton.dev \
  conditions.tekton.dev \
  pipelineresources.tekton.dev \
  runs.tekton.dev \
  customruns.tekton.dev \
  eventlisteners.triggers.tekton.dev \
  triggerbindings.triggers.tekton.dev \
  triggertemplates.triggers.tekton.dev \
  clusterinterceptors.triggers.tekton.dev \
  interceptors.triggers.tekton.dev \
  triggers.triggers.tekton.dev \
  config.operator.tekton.dev \
  tektonaddons.operator.tekton.dev \
  tektonchains.operator.tekton.dev \
  tektonconfigs.operator.tekton.dev \
  tektondashboards.operator.tekton.dev \
  tektonhubs.operator.tekton.dev \
  tektoninstallersets.operator.tekton.dev \
  tektonpipelines.operator.tekton.dev \
  tektonresults.operator.tekton.dev \
  tektontriggers.operator.tekton.dev
```

## 3. Handle stuck CRDs with finalizers

If CRDs are stuck in "Terminating" state:

```bash
# Check for CRDs with finalizers
oc get crd -o json | jq -r '.items[] | select(.metadata.name | contains("tekton")) | select(.metadata.finalizers != null) | .metadata.name'

# Remove finalizers from stuck CRDs
for crd in $(oc get crd -o name | grep tekton); do
  oc patch $crd -p '{"metadata":{"finalizers":[]}}' --type=merge
done
```

## 4. Clean up custom resources before deleting CRDs

**Important:** Delete custom resources (CRs) first to avoid orphaned objects:

```bash
# Delete all pipeline resources across all namespaces
oc delete pipelineruns --all --all-namespaces
oc delete taskruns --all --all-namespaces
oc delete pipelines --all --all-namespaces
oc delete tasks --all --all-namespaces

# Delete trigger resources
oc delete eventlisteners --all --all-namespaces
oc delete triggerbindings --all --all-namespaces
oc delete triggertemplates --all --all-namespaces
```

## 5. Complete cleanup script

Here's a comprehensive script to clean everything:

```bash
#!/bin/bash

echo "Deleting all Tekton custom resources..."
oc delete pipelineruns,taskruns,pipelines,tasks,clustertasks --all --all-namespaces --wait=false
oc delete eventlisteners,triggerbindings,triggertemplates,triggers --all --all-namespaces --wait=false

echo "Waiting 10 seconds..."
sleep 10

echo "Removing finalizers from stuck resources..."
for ns in $(oc get ns -o name); do
  for resource in pipelineruns taskruns pipelines tasks; do
    oc get $resource -n ${ns#namespace/} -o name 2>/dev/null | while read r; do
      oc patch $r -n ${ns#namespace/} -p '{"metadata":{"finalizers":[]}}' --type=merge 2>/dev/null
    done
  done
done

echo "Deleting Tekton CRDs..."
oc get crd -o name | grep tekton | xargs oc delete --wait=false

echo "Removing finalizers from stuck CRDs..."
sleep 5
for crd in $(oc get crd -o name | grep tekton); do
  oc patch $crd -p '{"metadata":{"finalizers":[]}}' --type=merge
done

echo "Done! Checking remaining Tekton CRDs..."
oc get crd | grep tekton
```

## 6. Verify cleanup

```bash
# Should return nothing
oc get crd | grep tekton

# Also check for any remaining resources
oc api-resources | grep tekton
```

After deleting the CRDs, you can proceed with a fresh installation of OpenShift Pipelines. Let me know if you encounter any stuck resources!
