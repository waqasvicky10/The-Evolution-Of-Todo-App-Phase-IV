# Rebuild and Redeploy Script

# 1. Build Backend Image
docker build -t todo-backend:optimized -f backend/Dockerfile .

# 2. Build Frontend Image
docker build -t todo-frontend:optimized -f frontend/Dockerfile .

# 3. Load images into Minikube (if using Minikube and not strict local docker env)
# minikube image load todo-backend:optimized
# minikube image load todo-frontend:optimized

# 4. Update Helm Release
helm upgrade --install todo-app ./phase_iv/helm/todo-app

# 5. Restart Pods
kubectl rollout restart deployment/todo-backend -n todo-app
kubectl rollout restart deployment/todo-frontend -n todo-app
