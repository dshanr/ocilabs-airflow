FROM apache/airflow:3.0.2

USER root

# Install any system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python packages
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Verify OCI SDK installation
RUN python -c "import oci; print(f'OCI SDK version: {oci.__version__}')"