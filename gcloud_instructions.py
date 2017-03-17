# Create a Second Generation Cloud SQL instance.
#You can do this from the Cloud Console or via the Cloud SDK.
#To create it via the SDK use the following command:
gcloud sql instances create my_db_instance_1 --activation-policy=ALWAYS --tier=db-n1-standard-1

# set root password on cloud instnace
gcloud sql instances set-root-password db_instance --password password

# you can run in development mode...:

# deloy the app_tests
"https://cloud.google.com/appengine/docs/flexible/python/testing-and-deploying-your-app"
gcloud app deploy

cloud-sql pw: 3Htz8HPhuLqe6NE5

gcloud sql instances set-root-password cloud-sql --password 3Htz8HPhuLqe6NE5

# https://cloud.google.com/sql/docs/mysql/connect-external-app#createServiceAccount

cloud_sql_proxy -dir /tmp/cloudsql -instances=cloudsql-tutorial:us-central1:cloud-sql=tcp:3306 -credential_file=C:\Users\samko\OneDrive\Programming\Projects\google_app_engine\python-docs-samples\appengine\flexible\cloudsql\cloudsql-tutorial-2bf87f927d08-privatekey.json


set GOOGLE_APPLICATION_CREDENTIALS = C:/Users/samko/OneDrive/Programming/Projects/google_app_engine/python-docs-samples/appengine/flexible/cloudsql/cloudsql-tutorial-2bf87f927d08-privatekey.json


cloud_sql_proxy -instances=cloudsql-tutorial:us-central1:cloud-sql=tcp:3307


cloud_sql_proxy -instances=cloudsql-tutorial:us-central1:cloud-sql=tcp:3306

cloud_sql_proxy -instances=cloudsql-tutorial:us-central1:cloud-sql=tcp:3307 -credential_file="C:\Users\samko\OneDrive\Programming\Projects\google_app_engine\python-docs-samples\appengine\flexible\cloudsql\cloudsql-tutorial-2bf87f927d08-privatekey.json" &


# step 4

# step 5
# need to specify port as well as host
# use your mysql pw you estalbished on Cloud SQL instance


# commands to connect a databse
create database production;
CREATE USER 'newuser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'%';
FLUSH PRIVILEGES;

SQLALCHEMY_DATABASE_URI=mysql+pymysql://newuser:password@127.0.0.1/test

# hard code this into your configs
# remember to do the host:port!
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://newuser:password@127.0.0.1:3307/test"


#Create project
https://console.cloud.google.com/sql/instances/smartphrase-app/overview?project=smartphrase-app&duration=PT1H

# Create SQL instance; enable cloud SQL API
https://console.cloud.google.com/sql/instances/smartphrase-app/overview?project=smartphrase-app&duration=PT1H

# Activate Compute Engine api

#connect to proxy
template: cloud_sql_proxy -instances=<INSTANCE_CONNECTION_NAME>=tcp:3306 -credential_file=<PATH_TO_KEY_FILE> &
example: cloud_sql_proxy -instances=smartphrase-app:us-central1:smartphrase-app=tcp:3307 -credential_file="C:\Users\samko\OneDrive\Credentials\smartphrase-app-1ab89adacc8b.json" &

# start local client that will connect to proxy
mysql -u root -p --host 127.0.0.1 --port 3307

# create db and user_ip
###template:
create database <dbname>;
CREATE USER '<username>'@'%' IDENTIFIED BY '<password>';
GRANT ALL PRIVILEGES ON * . * TO '<user>'@'%';
FLUSH PRIVILEGES;
###example:
create database production;
CREATE USER 'newuser'@'%' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON * . * TO 'newuser'@'%';
FLUSH PRIVILEGES;

# create your dbs before you push by doing so in the DB_reset env
# either set your environment variable to this or set your config file to run this
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://newuser:password@127.0.0.1:3307/production"
C\: python
>>>from app.db_reset import db_reset
>>>db_reset()

# update app.yaml file (template)
template:
SQLALCHEMY_DATABASE_URI: >-
      mysql+pymysql://USER:PASSWORD@/DATABASE?unix_socket=/cloudsql/INSTANCE_CONNECTION_NAME
