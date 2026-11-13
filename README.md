# Kubernetes End-to-End Application Deployment 

This repository contains a full production-ready Kubernetes setup deploying a multi-tier web application (Python/Flask backend connected to PostgreSQL database) with self-healing, rolling updates, Ingress networking, and Helm packaging.

---

## 🏗️ Architecture Overview

```text
                        [ User Request ]
                               │
                               ▼
                        [ NGINX Ingress ] (myapp.local)
                               │
                               ▼
                     [ ClusterIP Service ] (port 80)
                               │
                               ▼
                   ┌───────────────────────┐
                   │  Flask App Deployment │ (2+ Replicas)
                   │  (Probes + Limits)    │
                   └───────────┬───────────┘
                               │
                        (ConfigMap & Secret)
                               │
                               ▼
                   ┌───────────────────────┐
                   │ Postgres StatefulSet  │ (PVC Mounted)
                   └───────────────────────┘
