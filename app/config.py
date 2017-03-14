class Prod:
    pass

class Dev:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://newuser:password@localhost/epic_smart_phrases'
    SQLALCHEMY_ECHO = True

class Test:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://test:test_pass@localhost/test'
    SQLALCHEMY_ECHO = False
    TESTING: True
