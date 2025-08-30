1. Ingestion, as I could not use n8n I created the python script named ingestion.py, the requierements are in the requirements.txt files.
    a. To use it call "python3 ingestion.py" after installing the requierements in the virtual environment or container.

2. The queries for the KPI model are in the SQL/kpi_model.sql file.  This data can be access in the table of the database, credentials are in the environment.py file.
    a. Table creation scripts are in the SQL/tableCreation.sql file.

3. For the API endpoint I used Flask with SQLAlchemy.  Used waitress for deploying.  It can be executed using "python3 api.py".  This will start a server.
    a. To try it you can use the following curl call "curl -X GET "http://localhost:9090/api/v1/ads/metrics?start=01/01/2025&end=01/02/2025"" in another terminal window.

4. For the NLP -> SQL I used a Gradio App and the command for execution is "python3 app.py".  I was testing it locally with Ollama.
    a. All the information for the used model is in the file app_env.py.