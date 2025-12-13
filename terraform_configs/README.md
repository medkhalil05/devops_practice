## Recréer l'infrastructure (localement avec Minikube)

Prérequis
- Docker installé et en cours d'exécution
- Terraform v1.x
- Minikube
- kubectl (optionnel : `minikube kubectl -- ...` peut être utilisé)

Étapes rapides
```bash
# Initialiser les providers
terraform -chdir=terraform_configs init -upgrade

# Appliquer la configuration (crée le cluster Minikube et installe ArgoCD)
terraform -chdir=terraform_configs apply -auto-approve

# Vérifier les pods
kubectl get pods -n argocd

# Récupérer le mot de passe admin ArgoCD
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d

# Accéder à l'UI (port-forward)
kubectl -n argocd port-forward svc/argocd-server 8080:80
# puis ouvrir http://localhost:8080 (user: admin, password ci-dessus)
```

Notes
- Le provider Helm a été configuré pour utiliser directement les credentials fournis
  par la ressource `minikube_cluster` (voir `provider.tf`). Cela évite les erreurs
  "Kubernetes cluster unreachable" si `~/.kube/config` ne référence pas le profile.
- Si le profile Minikube existe mais est dans un état corrompu, utilisez :
  `minikube delete -p complete-devops-project && minikube start -p complete-devops-project --driver=docker --kubernetes-version=v1.30.0`
