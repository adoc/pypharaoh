import os
import functools
import hashlib
import sqlalchemy
import sqlalchemy.types
import sqlalchemy.orm.exc

import core.models


def get_user(userident):
    """Get user based on `ident`. This is so we don't expose any
    details about the user in cookies or other transports that may
    be transmitted unencrypted.
    """

    try:
        return (core.models.Session
                    .query(User)
                    .filter(User.ident==userident)
                    .one())
    except sqlalchemy.orm.exc.NoResultFound:
        return None


def init_auth_models(settings):
    """
    """

    global UserGroup
    global Group
    global User
    global get_user

    user_tablename = settings.get('authn.models.user.tablename', 'users').strip()
    group_tablename = settings.get('authn.models.group.tablename', 'groups').strip()
    user_group_tablename = settings.get('authn.models.user_group.tablename',
                                        'users_groups').strip()
    ident_secret = settings.get('authn.models.identity.secret', '').strip()
    ident_use_password = settings.get('authn.models.identity.use_password', False)

    class UserGroup(core.models.Base):
        __tablename__ = user_group_tablename

        id = sqlalchemy.Column(sqlalchemy.types.Integer, primary_key=True)
        userid = sqlalchemy.Column(sqlalchemy.types.Integer,
                                    sqlalchemy.ForeignKey(
                                        '.'.join([user_tablename, 'id'])))
        groupid = sqlalchemy.Column(sqlalchemy.types.Integer,
                                    sqlalchemy.ForeignKey(
                                        '.'.join([group_tablename, 'id'])))

    @functools.total_ordering
    class Group(core.models.Base):
        __tablename__ = group_tablename

        id = sqlalchemy.Column(sqlalchemy.types.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.types.String(length=64),
                                    unique=True)
        level = sqlalchemy.Column(sqlalchemy.types.SmallInteger, nullable=False,
                                    default=0)
        users = sqlalchemy.orm.relationship("User", 
                                            secondary=UserGroup.__table__)

        # Comparators
        def __lt__(self, other):
            return self._level < other._level

        def __eq__(self, other):
            return self._level == other._level


    class User(core.models.Base):
        __tablename__ = user_tablename

        id = sqlalchemy.Column(sqlalchemy.types.Integer, primary_key=True)
        _name = sqlalchemy.Column('name', sqlalchemy.types.String(length=64),
                                    unique=True, index=True)
        #ident_salt = sqlalchemy.Column('ident_salt',
        #                            sqlalchemy.LargeBinary(length=8),
        #                            default=lambda: os.urandom(8))
        ident = sqlalchemy.Column(sqlalchemy.types.LargeBinary(length=32),
                                    unique=True, index=True)
        pass_salt = sqlalchemy.Column('pass_salt',
                                    sqlalchemy.LargeBinary(length=8),
                                    default=lambda: os.urandom(8))
        passhash = sqlalchemy.Column(sqlalchemy.types.LargeBinary(length=64))

        groups = sqlalchemy.orm.relationship(Group,
                                             secondary=UserGroup.__table__)

        def _gen_hash(self, *args, alg=hashlib.sha512):
            hash_ = alg()
            for arg in args:
                if arg:
                    try:
                        value = arg.encode()
                    except AttributeError:
                        value = arg
                    hash_.update(value)
            return hash_.digest()

        def set_ident(self):
            args = ()
            if ident_secret:
                args += (ident_secret,)
            ident_nonce = os.urandom(8)
            args += (ident_nonce, self.name)
            if ident_use_password:
                args += (self.pass_salt, self.passhash)
            self.ident = self._gen_hash(*args, alg=hashlib.sha256)

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, name):
            self._name = name
            self.set_ident()

        '''
        @property
        def ident_salt(self):
            if not self._ident_salt:
                self._ident_salt = os.urandom(8)
            return self._ident_salt'''

        '''
        @property
        def pass_salt(self):
            if not self._pass_salt: 
                self._pass_salt = os.urandom(8)
            return self._pass_salt'''

        @property
        def password(self):
            raise ValueError("Cannot get a password.")

        @password.setter
        def password(self, password):
            self.pass_salt = os.urandom(8)
            self.passhash = self._gen_hash(self.pass_salt, password)
            self.set_ident()

        def check_password(self, challenge):
            return self.passhash == self._gen_hash(self.pass_salt, challenge)

        @property
        def level(self):
            return max([group.level for group in self.groups])

        def __json__(self, request):
            return {
                'id': self.id,
                'name': self.name
            }