# Use '>' as the recipe prefix so this file doesn't depend on literal tabs.
.RECIPEPREFIX := >
.PHONY: up pipeline dash clean

up:  ## Start Airflow (UI on port 8080). Login with the password it prints.
> @if [ -n "$$CODESPACE_NAME" ]; then export AIRFLOW__WEBSERVER__BASE_URL="https://$$CODESPACE_NAME-8080.$$GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN" AIRFLOW__WEBSERVER__ENABLE_PROXY_FIX=True; echo "Airflow UI: $$AIRFLOW__WEBSERVER__BASE_URL"; fi; airflow standalone

pipeline:  ## Run the data pipeline once (extract -> transform -> load)
> python -m src.pipeline

dash:  ## Run the Streamlit dashboard (port 8501)
> streamlit run app.py --server.port 8501 --server.address 0.0.0.0

clean:  ## Remove generated output and the local Airflow database
> rm -rf output .airflow
