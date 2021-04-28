import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_POSTS_PER_PAGE = int(os.environ.get('FLASKY_POSTS_PER_PAGE')) or 20
    FLASKY_COMMENTS_PER_PAGE = int(os.environ.get('FLASKY_COMMENTS_PER_PAGE')) or 20
    FLASKY_FOLLOWERS_PER_PAGE = int(os.environ.get('FLASKY_FOLLOWERS_PER_PAGE')) or 20
    FLASKY_SLOW_DB_QUERY_TIME = float(os.environ.get('FLASKY_SLOW_DB_QUERY_TIME')) or 0.5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
    
    # Send emails to admins
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    secure = None

    if getattr(cls, 'MAIL_USERNAME', None) is not None:
        credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
        if getattr(cls, 'MAIL_USE_TLS', None):
            secure = ()
    mail_handler = SMTPHandler(
        mailhost = (cls.MAIL_SERVER, cls.MAIL_PORT),
        fromaddr = cls.FLASKY_MAIL_SENDER,
        toaddrs = [cls.FLASKY_ADMIN],
        subject = cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
        credentials = credentials,
        secure = secure 
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}