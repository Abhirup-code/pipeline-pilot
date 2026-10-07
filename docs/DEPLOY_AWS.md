# Deploying to AWS EC2 (free tier)

## 1. Launch the server
1. AWS Console > EC2 > Launch instance. Name: `taskapp`. AMI: Ubuntu 24.04 LTS. Type: `t3.micro` or `t2.micro` (free-tier eligible).
2. Create a key pair (`.pem`) and keep it safe.
3. Security group: allow SSH (22) from **your IP only**, and HTTP (80) from anywhere.
4. Launch.

## 2. Install Docker on the instance
```bash
ssh -i taskapp.pem ubuntu@<EC2_PUBLIC_IP>
sudo apt-get update && sudo apt-get install -y docker.io
sudo usermod -aG docker ubuntu
exit   # log in again so the group applies
```

## 3. Make the image pullable
Push to `main` once so CI publishes `ghcr.io/<you>/pipeline-pilot`. On GitHub: Packages > the package > Package settings > set visibility to **Public** (then no token is needed), or create a token with `read:packages`.

## 4. Add repo secrets (Settings > Secrets and variables > Actions)
| Secret | Value |
|---|---|
| `EC2_HOST` | the instance public IP or DNS name |
| `EC2_USER` | `ubuntu` |
| `EC2_SSH_KEY` | full contents of the `.pem` file |
| `GHCR_TOKEN` | a GitHub token with `read:packages` (any value works if the package is public) |

## 5. Deploy
Push to `main`. CI tests and publishes the image, then **Deploy to AWS EC2** runs and starts the container. Open `http://<EC2_PUBLIC_IP>/`.

## 6. Cost and cleanup
Stop or terminate the instance when you are done, and set an AWS billing alert. Free-tier limits change, so check your account.
