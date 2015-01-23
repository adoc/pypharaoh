"""
"""

import random
import time
import datetime
import operator

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.types
import sqlalchemy.ext.declarative

from pprint import pprint

_ini = {'sqlalchemy.url': 'sqlite:///sqlalchemy_datetime_vs_epoch.sqlite'}
_timings = {}

Base = sqlalchemy.ext.declarative.declarative_base()
Session = sqlalchemy.orm.scoped_session(
                sqlalchemy.orm.sessionmaker())


class EpochSeconds(sqlalchemy.types.TypeDecorator):
    impl = sqlalchemy.types.Integer
    epoch = datetime.datetime(1970, 1, 1, hour=0, minute=0, second=0)

    def process_bind_param(self, value, dialect):
        return (value - self.epoch).total_seconds()

    def process_result_value(self, value, dialect):
        return self.epoch + datetime.timedelta(seconds=value)


class ModelDateTime(Base):
    __tablename__ = 'datetime'
    id = sqlalchemy.Column(sqlalchemy.types.Integer, primary_key=True)
    datum = sqlalchemy.Column(sqlalchemy.types.DateTime)


class ModelEpoch(Base):
    __tablename__ = 'epoch'
    id = sqlalchemy.Column(sqlalchemy.types.Integer, primary_key=True)
    datum = sqlalchemy.Column(EpochSeconds)


def main(*sysargs):
    """
    """

    global Engine

    Engine = sqlalchemy.engine_from_config(_ini, 'sqlalchemy.')
    Session.configure(bind=Engine)
    Base.metadata.bind = Engine

    # Drop and create all tables for each test (scientific and all).
    Base.metadata.drop_all(Engine)
    Base.metadata.create_all(Engine)

    epoch = datetime.datetime(1970, 1, 1, hour=0, minute=0, second=0)

    max_epoch_delta = 2000000000
    statistical_median = epoch + datetime.timedelta(seconds=max_epoch_delta / 2)

    # Build the dataset (same for each test.)
    # 1000 random dates from 1970 to 2033 or so.
    print('dataset.gen')
    pt = time.time()
    dataset = [epoch + datetime.timedelta(seconds=max_epoch_delta * random.random())
                for _ in range(200000)]
    # _timings['dataset.gen'] = time.time() - pt

    # Add dataset as ModelDateTime
    print('datetime.add')
    pt = time.time()
    for datum in dataset:
        Session.add(ModelDateTime(datum=datum))
    _timings['datetime.add'] = time.time() - pt

    # Commit the ModelDateTime add.
    print('datetime.commit')
    pt = time.time()
    Session.commit()
    _timings['datetime.commit'] = time.time() - pt

    # Add dataset as ModelEpoch
    print('epoch.add')
    pt = time.time()
    for datum in dataset:
        Session.add(ModelEpoch(datum=datum))
    _timings['epoch.add'] = time.time() - pt

    # Commit the ModelEpoch add.
    print('epoch.commit')
    pt = time.time()
    Session.commit()
    _timings['epoch.commit'] = time.time() - pt

    # Query all of the ModelDateTime dataset.
    print('datetime.query.all')
    pt = time.time()
    queried_dataset = Session.query(ModelDateTime).all()
    _timings['datetime.query.all'] = time.time() - pt

    # Run calculation against ModelDateTime dataset.
    print('datetime.calculate.dataset')
    pt = time.time()
    for datum in queried_dataset:
        _ = statistical_median - datum.datum
    _timings['datetime.calculate.dataset'] = time.time() - pt

    # Query all of the ModelEpoch dataset.
    print('epoch.query.all')
    pt = time.time()
    queried_dataset = Session.query(ModelEpoch).all()
    _timings['epoch.query.all'] = time.time() - pt

    # Run calculation against ModelDateTime dataset.
    print('epoch.calculate.dataset')
    pt = time.time()
    for datum in queried_dataset:
        _ = statistical_median - datum.datum
    _timings['epoch.calculate.dataset'] = time.time() - pt


    # Display timing results.
    sorted_timing = sorted(_timings.items(), key=operator.itemgetter(1))
    sorted_key = sorted(_timings.items(), key=operator.itemgetter(0))

    print("="*80)
    print("Results ordered by key.")
    for k,v in sorted_key:
        print('%s: %f' % (k,v))

    print("="*80)
    print("Results ordered by timing.")
    for k,v in sorted_timing:
        print('%s: %f' % (k,v))


import sys


if __name__ == '__main__':
    main(sys.argv)