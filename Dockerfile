# Python image to use.
FROM ghcr.io/dbt-labs/dbt-bigquery:1.5.6

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Download dbt dependencies
RUN dbt deps --profiles-dir dbt --project-dir dbt

# Run app.py when the container launches
ENTRYPOINT ["python", "app.py"]
