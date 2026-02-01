#!/bin/bash

echo "=== Finding all Tekton CRDs ==="
TEKTON_CRDS=$(oc get crd -o name | grep tekton.dev)

if [ -z "$TEKTON_CRDS" ]; then
  echo "No Tekton CRDs found!"
  exit 0
fi

echo "Found the following Tekton CRDs:"
echo "$TEKTON_CRDS"
echo ""

echo "=== Removing finalizers from Tekton CRDs ==="
for crd in $TEKTON_CRDS; do
  CRD_NAME=$(echo $crd | cut -d'/' -f2)
  echo "Processing: $CRD_NAME"
  
  # Check if CRD has finalizers
  FINALIZERS=$(oc get $crd -o jsonpath='{.metadata.finalizers}')
  
  if [ -n "$FINALIZERS" ] && [ "$FINALIZERS" != "[]" ]; then
    echo "  - Current finalizers: $FINALIZERS"
    echo "  - Removing finalizers..."
    oc patch $crd -p '{"metadata":{"finalizers":[]}}' --type=merge
    
    if [ $? -eq 0 ]; then
      echo "  ✓ Finalizers removed successfully"
    else
      echo "  ✗ Failed to remove finalizers"
    fi
  else
    echo "  - No finalizers present"
  fi
  echo ""
done

echo "=== Checking CRD status ==="
oc get crd | grep tekton.dev
