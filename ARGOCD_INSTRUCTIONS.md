ArgoCD Setup & Access
=====================

This file explains how to apply the existing ArgoCD Application and access the ArgoCD UI so the repo-based GitOps flow (the `k8s-manifests/` folder) syncs to your cluster.

1) Ensure ArgoCD is installed

- If you don't have ArgoCD installed, follow the official quickstart:

  ```bash
  kubectl create namespace argocd
  kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
  ```

2) Apply the Application manifest (already done by CI `push-manifests` job)

- To create or update the ArgoCD Application resource from the repository locally:

  ```bash
  kubectl apply -f k8s-manifests/05-argocd-application.yaml
  ```

3) Verify the Application resource

  ```bash
  kubectl get applications -n argocd
  kubectl describe application finance-tracker-app -n argocd
  ```

4) Access the ArgoCD Web UI (port-forward)

  ```bash
  kubectl port-forward svc/argocd-server -n argocd 8080:443
  # then open https://localhost:8080 in your browser
  ```

5) Default admin password (if not changed)

  ```bash
  kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode
  # username: admin
  # password: <output above>
  ```

6) Syncing and troubleshooting

- From CLI (argocd CLI tool) you can login and sync the app:

  ```bash
  # if you have argocd CLI installed
  argocd login localhost:8080 --plaintext
  argocd app list
  argocd app sync finance-tracker-app
  argocd app status finance-tracker-app
  ```

- From kubectl you can force a sync by patching the Application (changes to the manifest in the repo + CI `push-manifests` will normally trigger sync automatically):

  ```bash
  # view object
  kubectl get application finance-tracker-app -n argocd -o yaml
  # manually trigger a refresh
  kubectl -n argocd patch application finance-tracker-app --type='merge' -p '{"spec": {"syncPolicy": null}}' || true
  ```

7) Notes & security

- The CI job `push-manifests` updates `k8s-manifests/02-deployment.yaml` with the built image tag and commits to `main` — ArgoCD will detect the change and reconcile.
- If your repo is private, ensure ArgoCD has credentials to access it (either via SSH key or deploy key configured in ArgoCD settings).
- If you use branch protection, ensure the CI token used to push manifests has permission to write to the target branch.

If you want, I can port-forward the ArgoCD UI for you now or run `argocd app sync finance-tracker-app` (requires `argocd` CLI). Which would you prefer? 
