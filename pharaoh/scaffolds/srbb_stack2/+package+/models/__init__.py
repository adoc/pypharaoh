"""Core models initialization. Provides the `Base` and `Session`
"""

import datetime
import pytz
import sqlalchemy.types
import sqlalchemy.orm
import sqlalchemy.ext.declarative
import zope.sqlalchemy


Session = sqlalchemy.orm.scoped_session(
                sqlalchemy.orm.sessionmaker(
                    extension=zope.sqlalchemy.ZopeTransactionExtension()))
Base = sqlalchemy.ext.declarative.declarative_base()


def init_models(settings):
    """Initialize base models.
    """

    global Engine
    global EpochSeconds

    class EpochSeconds(sqlalchemy.types.TypeDecorator):
        impl = sqlalchemy.types.Integer
        epoch = (datetime.datetime.strptime(settings['database.epoch'],
                                            settings['datetime.date_format'])
                                    .replace(tzinfo=settings['database.timezone']))

        def process_bind_param(self, value, dialect):
            return (value - self.epoch).total_seconds()

        def process_result_value(self, value, dialect):
            return self.epoch + datetime.timedelta(seconds=value)

    Engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
    Session.configure(bind=Engine)
    Base.metadata.bind = Engine