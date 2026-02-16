# Rebuild Frontend
docker build -t todo-frontend:optimized -f frontend/Dockerfile .

# Load into Minikube
minikube image load todo-frontend:optimized

# Restart Deployment
kubectl rollout restart deployment/todo-frontend -n todo-app
