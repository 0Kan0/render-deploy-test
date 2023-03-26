gcloud builds submit --tag gcr.io/academic-failure-prediction/academic-failure-prediction-tool --project=academic-failure-prediction

gcloud run deploy --image gcr.io/academic-failure-prediction/academic-failure-prediction-tool --platform managed --project=	academic-failure-prediction --allow-unauthenticated