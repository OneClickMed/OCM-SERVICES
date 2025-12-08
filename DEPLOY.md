# Deploying OCM Service Backend to Google Cloud Run

This file documents a minimal, safe path to deploy this Django app to Google Cloud Run.

Prerequisites
- Google Cloud project and billing enabled
- gcloud SDK installed and authenticated
- Cloud Run API enabled

Build and push image (recommended: use Cloud Build)

1. Build and push with Cloud Build (CI):

   gcloud builds submit --config cloudbuild.yaml --substitutions=_CLOUD_RUN_REGION=us-central1

2. Or build locally and push to Artifact Registry / Container Registry:

   docker build -t gcr.io/PROJECT-ID/ocm-service-backend:latest .
   docker push gcr.io/PROJECT-ID/ocm-service-backend:latest

Deploy to Cloud Run

1. Deploy using gcloud (replace PROJECT-ID and REGION):

   gcloud run deploy ocm-service-backend \
     --image gcr.io/PROJECT-ID/ocm-service-backend:latest \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars DJANGO_SETTINGS_MODULE=config.settings,DEBUG=false

   Automating deploy with Cloud Build triggers (GitHub)

   1) Connect GitHub to Cloud Build (one-time):

      - In Cloud Console: Cloud Build > Triggers > Connect Repository > GitHub (follow OAuth)
      - Or (CLI) use the Cloud Console flow — the CLI `gcloud alpha builds triggers github connect` flow opens the browser to connect.

   2) Create a trigger that runs on branch push and uses `cloudbuild.yaml`:

      gcloud beta builds triggers create github \
        --name="ocm-backend-trigger" \
        --repo-owner="GITHUB_OWNER" \
        --repo-name="GITHUB_REPO" \
        --branch-pattern="^main$" \
        --build-config="cloudbuild.yaml" \
        --substitutions=_CLOUD_RUN_REGION=us-central1,_CLOUD_SQL_INSTANCE="PROJECT:REGION:INSTANCE" \
        --project=PROJECT-ID

   3) Required IAM roles for Cloud Build service account (PROJECT_NUMBER@cloudbuild.gserviceaccount.com):

      - roles/run.admin (Cloud Run Admin)
      - roles/iam.serviceAccountUser
      - roles/storage.admin or Artifact Registry push permissions
      - roles/secretmanager.secretAccessor (if using Secret Manager)
      - roles/cloudsql.client (if using Cloud SQL)

   4) Best practices
      - Use Secret Manager for SECRET_KEY and attach via `--update-secrets` or `--set-secrets` in the deploy step.
      - Prefer private Cloud SQL connections or IAM-authenticated connections for production DBs.

Secrets and database
- Use Secret Manager for SECRET_KEY, BREVO_API_KEY, etc., and inject into Cloud Run via `--set-secrets` or the Cloud Console.
- For Postgres/Cloud SQL, use the Cloud SQL Proxy or a private IP and set `DATABASE_URL` environment variable for the connection string. Example:

  postgresql://USER:PASSWORD@HOST:5432/DBNAME

Notes
- The container listens on port 8080 (Cloud Run default). Adjust `MAX_INSTANCES` or concurrency on deploy as needed.
- The `entrypoint.sh` will attempt migrations and collectstatic by default. Set `DJANGO_DISABLE_MIGRATIONS=true` to skip migrations.
