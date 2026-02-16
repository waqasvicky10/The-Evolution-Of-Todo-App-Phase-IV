# Manual ConfigMap Apply
# Since Helm upgrade failed, I will manually patch the ConfigMap if needed.

# 1. Check current ConfigMap
kubectl get configmap todo-app-config -n todo-app -o yaml

# 2. Apply if missing API_URL
kubectl patch configmap todo-app-config -n todo-app --type merge -p '{"data":{"API_URL":"http://todo-backend:8000"}}'
