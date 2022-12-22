# REST API - Python - Flask - MySQL - Grafana - Docker(Docker-image/Docker-compose)

REST API created with Python, the web/Api framework Flask and MySQL, with the protocol HTTP and the methos GET and POST.


- To test locally the poetry dependencies must be installed:
    - `pip install poetry` 
    - `poetry install`
    - And the configuration of the connection of mysql, must be set as the the default (user=root, password=password and host=localhost, if running mysql of the docker compose)




# Challenge 1
## Snippets For test:

### 1) Creating Database, tables, and doing the initial migration with /migration endpoint for point 1, moving the historic data from csv to the new database:
    
        import requests
        result = requests.get('http://127.0.0.1:5001/migration')
        print(result.status_code,result.text)


#### 2) Inserting new rows with the /insert_rows endpoint for point 2, recieving new data:
  - Conditions met: 
    - 2.1 Filters for Data Dictotionary rules. 
    - 2.2 Able to insert batch transactions with one request (must send the data to the endpoint as shown below).
    - 2.3 Able to receive the data for each table in the same service (that's why table must be specified in the message to the endpoint).
    - 2.4 Idem 2.1
   
  ###
        import requests

        data = {'messages': 
                        [{'id': 1001, 'name': 'Luciano Argolo', 'datetime':'2021-07-27T16:02:08Z', 'department_id': 2, 'job_id': 3},
                        {'id': 1002, 'name': 'Agustin Argolo', 'datetime':'2021-08-22T11:02:08Z', 'department_id': 3, 'job_id': 4},
                        {'id': 1002, 'name': 'Agustin Argolo', 'datetime':'2021-08-22T11:02:08Z', 'department_id': None, 'job_id': None}],
                'table':'employes'}

        #The third Row is filtered because it doesn't apply to Data Rules, and is also shown on log as "Warning".
        result = requests.post('http://127.0.0.1:5000/insert_rows', json=data)
        print(result.status_code,result.text)

    
#### 3) Generating avro backup with the /backup_table endpoint (needs to be specified the table for point 3, backup feature:
  - The backup feature, generates a file locally in AVRO format (at the location backups inside utils/backups)
  - The table to be backuped as asked, must be after the endpoint like this '?table=xxx'

###
    import requests
    result = requests.get('http://127.0.0.1:5000/backup_table?table=employees')
    print(result.status_code,result.text)

#### 4) generating the restore process with the /restore_table endpoint (needs to be specified the table) for point 4, restore table feature:
  - The restore feature, deletes everything in the table and then loads the last backup generated from AVRO
  - The table to be backuped as asked, must be after the endpoint like this '?table=xxx'
  
###
    import requests
    result = requests.get('http://127.0.0.1:5000/restore_table?table=employees')
    print(result.status_code,result.text)

## Clarifications of Challenge 1:
  - Code published here at Github.
  - The csv files are located inside utils/Data.
  - The Database chosen was Mysql.
  - Feature interpreted as endpoint (a way to accomplish the requirements).

    
## Not mandatory:
  - Markdown created.
  - Security Considerations, the passwords and user where set as environment variables for avoid hardcoding them. (the passwords of Grafana and Mysql, i left them as default to be easier to use, not because i don't know those passwords shouldn't be as default)
  - I had some issues with the repository, was branching each feature, until i discovered i was working on another repo of mine (so decided to avoid that point)
  - Created a Dockerfile.
      - Used Poetry for installation of dependencies.
      - Created also a Docker-compose file, with a network that connects mysql, grafana and the api together, so we also have monitoring tools (grafana).
  - Didn't use cloud, didn't know how to deploy de dockerfile or compose (even though i work with AWS and GCP, i know very few)
        

# Challenge 2
## Queries are inside utils/queries for further evaluation
#### generating the metric hired by quarters with the /hired_by_qs endpoint

    import requests
    result = requests.get('http://127.0.0.1:5001/hired_by_qs')
    result = result.status_code,result.text

![image](https://user-images.githubusercontent.com/75091406/209176385-5ef9882c-1654-497a-b969-0531f032ce43.png)


#### generating the metric over the mean 2021 with the /hired_over_the_mean endpoint

    import requests
    result = requests.get('http://127.0.0.1:5001/hired_over_the_mean')
    result = result.status_code,result.text

![image](https://user-images.githubusercontent.com/75091406/209176345-43db4048-7d56-41cc-bf80-3f1287d853b5.png)


#### Create (an attempt of) a visual report
   (Even though i have created dashboards in DataDog and Grafana for metrics, i don't know how to do visual reports (a trully report), so i tried my best haha.)

![Captura de Pantalla 2022-12-22 a la(s) 13 04 06](https://user-images.githubusercontent.com/75091406/209174630-7cdab635-6fd9-44ad-81d3-66bab15e38cc.png)




## Not mandatory:
  - I tried to do a report in Grafana.
