class Prod:
    pass

class Dev:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://newuser:password@localhost/epic_smart_phrases'
    SQLALCHEMY_ECHO = True

class Test:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://newuser:password@localhost/epic_smart_phrases_test'
    SQLALCHEMY_ECHO = False
    TESTING: True
