# automatically sets up your env variables on the cloud wiht the app.yaml file
class Prod:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://newuser:password@/production?unix_socket=/cloudsql/smartphrase-app:us-central1:smartphrase-app'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

# need to run the command below to launch the proxy
# cloud_sql_proxy -instances=smartphrase-app:us-central1:smartphrase-app=tcp:3307 -credential_file="C:\Users\samko\OneDrive\Credentials\smartphrase-app-1ab89adacc8b.json"
# mysql -u root -p --host 127.0.0.1 --port 3307
class Cloud_local:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://newuser:password@127.0.0.1:3307/production"

class Dev:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://newuser:password@localhost/epic_smart_phrases'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    #SQLALCHEMY_ECHO = True

class Test:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:test_pass@localhost/test'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_ECHO = False
    TESTING = True
