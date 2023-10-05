"""
A Flask Application for Deploying DBT
"""
import os
import logging
import json
import os

from flask import Flask, request, escape, render_template
import google.cloud.logging
from dbt.cli.main import dbtRunner, dbtRunnerResult


client = google.cloud.logging.Client()
client.setup_logging()

# pylint: disable=C0103
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    logging.info(f'Service: {service}, Revision: {revision}')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)


@app.route('/daily', methods=['POST'])
def daily():
    """DBT Daily Runner."""

    try:

        json = request.get_json(force=True) # https://stackoverflow.com/questions/53216177/http-triggering-cloud-function-with-cloud-scheduler/60615210#60615210
        target = escape(json['target']) if 'target' in json else 'prod'

        # initialize
        dbt = dbtRunner()

        # create CLI args as a list of strings
        cli_args = ["--project-dir", "dbt", "--profiles-dir", "dbt"]
        target_arg = ['--target', target]
 
        logging.info('Running: dbt source freshness')
        res: dbtRunnerResult = dbt.invoke(['source', 'freshness'] + cli_args + target_arg)
        # Add handle_res() function to handle the results

        logging.info('Running: dbt build')
        res: dbtRunnerResult = dbt.invoke(['build'] + cli_args + target_arg)
        # Add handle_res() function to handle the results

        ok = 'DBT Run Successfully'
        logging.info(ok)
        return ok    
    
    except Exception as e:
        logging.exception(e)
        return e


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=server_port, host='0.0.0.0')
