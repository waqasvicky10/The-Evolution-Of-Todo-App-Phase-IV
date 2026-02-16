# Apply Secret and Restart
helm upgrade --install todo-app ./phase_iv/helm/todo-app
kubectl rollout restart deployment/todo-backend -n todo-app
