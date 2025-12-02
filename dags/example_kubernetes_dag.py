"""
Example Airflow DAG using KubernetesExecutor
This DAG demonstrates basic tasks that run in separate Kubernetes pods
Compatible with Airflow 3.0+
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'kubernetes_executor_example',
    default_args=default_args,
    description='A simple DAG to test KubernetesExecutor',
    schedule=None,  # Manual trigger only (Airflow 3.0+)
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['example', 'kubernetes'],
) as dag:

    # Task 1: Simple Bash command
    hello_task = BashOperator(
        task_id='say_hello',
        bash_command='echo "Hello from Kubernetes Pod!" && hostname && date',
    )

    # Task 2: Python function
    def print_context(**context):
        """Print some context information"""
        import socket
        print(f"Task executed on pod: {socket.gethostname()}")
        print(f"Execution date: {context['ds']}")
        print(f"Task instance: {context['task_instance']}")
        return "Success!"

    python_task = PythonOperator(
        task_id='print_info',
        python_callable=print_context,
    )

    # Task 3: Process some data
    def process_data():
        """Simulate data processing"""
        import time
        print("Starting data processing...")
        for i in range(5):
            print(f"Processing batch {i+1}/5")
            time.sleep(2)
        print("Data processing complete!")
        return "Processed 5 batches"

    process_task = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
    )

    # Task 4: Install and use external library
    def use_external_library():
        """Demonstrates using Python libraries"""
        import json
        from datetime import datetime
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'message': 'Running in Kubernetes!',
            'status': 'success'
        }
        print(json.dumps(data, indent=2))
        return data

    library_task = PythonOperator(
        task_id='use_libraries',
        python_callable=use_external_library,
    )

    # Task 5: Final summary
    summary_task = BashOperator(
        task_id='summary',
        bash_command='''
            echo "==================================="
            echo "DAG Execution Summary"
            echo "==================================="
            echo "All tasks completed successfully!"
            echo "Pod: $(hostname)"
            echo "Timestamp: $(date)"
            echo "==================================="
        ''',
    )

    # Define task dependencies
    # Tasks run in parallel, then summary at the end
    [hello_task, python_task, process_task, library_task] >> summary_task