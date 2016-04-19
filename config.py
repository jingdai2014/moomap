SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://moomap:moomapduff@moomap.cm30mcffmq7o.us-west-2.rds.amazonaws.com:3306/moomap'

# Uncomment the line below if you want to work with a local DB
#SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

SQLALCHEMY_POOL_RECYCLE = 3600

WTF_CSRF_ENABLED = True
SECRET_KEY = 'compassion'
