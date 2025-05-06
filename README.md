# PES1UG22CS386-PES1UG22CS393-PES1UG22CS424-PES1UG22CS425-URLShortener
CC Mini-Project: URL-Shortener

# URL Shortener Project

## Week 1: URL Shortener in Docker

### Implementation Details
- Created a Flask application that shortens URLs using Redis as key-value store
- Built Docker container for the application using Python 3.9
- Configured docker-compose for local testing with Redis

### How to Run
```bash
cd url-shortener
docker-compose up --build
```

## Week 2: Kubernetes Deployment

### Implementation Details
- Containerized the URL shortener application for Kubernetes
- Created deployment manifests for both the application and Redis
- Configured Kubernetes services for internal and external access
- Implemented resilience through pod replication

### How to Run
```bash
# Start Minikube
minikube start

# Use Minikube's Docker daemon
eval $(minikube -p minikube docker-env)

# Build the Docker image
docker build -t url-shortener:latest ./app

# Apply Kubernetes configurations
kubectl apply -f kubernetes/redis-deployment.yaml
kubectl apply -f kubernetes/redis-service.yaml
kubectl apply -f kubernetes/url-shortener-configmap.yaml
kubectl apply -f kubernetes/url-shortener-secret.yaml
kubectl apply -f kubernetes/url-shortener-deployment.yaml
kubectl apply -f kubernetes/url-shortener-service.yaml

# Enable external access
minikube tunnel
```

## Week 3: Scaling, Load Balancing & Monitoring

### Implementation Details
- Set up Horizontal Pod Autoscaler (HPA) for automatic scaling based on CPU usage
- Implemented LoadBalancer service type for improved traffic distribution
- Configured monitoring using Kubernetes logs and resource metrics
- Created load testing scripts to demonstrate auto-scaling

### How to Run
```bash
# Enable metrics server for HPA
minikube addons enable metrics-server

# Apply HPA configuration
kubectl apply -f kubernetes/url-shortener-hpa.yaml

# Verify setup
kubectl get hpa url-shortener-hpa

# Run load test using Locust
pip install locust
locust --host=http://localhost
```

### Monitoring
```bash
# Watch HPA status
kubectl get hpa url-shortener-hpa --watch

# Watch pod creation/termination
kubectl get pods -w

# Monitor resource usage
watch kubectl top pods

# View application logs
kubectl logs -f -l app=url-shortener
```

## Testing the URL Shortener

### Basic Usage
```bash
# Create a shortened URL
curl -X POST -H "Content-Type: application/json" \
  -d '{"url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"}' \
  http://localhost/shorten

# Access the shortened URL (replace with your actual code)
curl -v http://localhost/Ab3X9z
```

### Load Testing
```bash
# Run the load test script
chmod +x load-test.sh
./load-test.sh
```

## Project Structure
```
url-shortener/
├── app/
│   ├── app.py              # Flask application for URL shortening
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Container configuration for app
├── docker-compose.yml      # Local development environment setup
├── load-test.sh           # Script for load testing
└── kubernetes/             # Kubernetes configuration files
    ├── redis-deployment.yaml
    ├── redis-service.yaml
    ├── url-shortener-configmap.yaml
    ├── url-shortener-deployment.yaml
    ├── url-shortener-hpa.yaml
    ├── url-shortener-secret.yaml
    └── url-shortener-service.yaml
```

## System Features
- Shortened URLs redirect to original destinations
- High availability through Kubernetes pod replication
- Automatic scaling based on CPU usage
- Load balancing across multiple instances
- Redis-based persistent storage for URL mappings
- Containerized deployment for consistency across environments
