import os
import hashlib
import sqlalchemy
import sqlalchemy.types
import sqlalchemy.orm.exc

import core.models


def init_auth_models(settings):
    """
    """

    global UserGroup
    global Group
    global User
    global get_user

    user_tablename = settings.get('authn.models.user.tablename', 'users')
    group_tablename = settings.get('authn.models.group.tablename', 'groups')
    user_group_tablename = settings.get('authn.models.user_group.tablename',
                                        'users_groups')

    class UserGroup(core.models.Base):
        __tablename__ = user_group_tablename

        id = sqlalchemy.Column(sqlalchemy.types.Integer, primary_key=True)
        userid = sqlalchemy.Column(sqlalchemy.types.Integer,
                                    sqlalchemy.ForeignKey(
                                        '.'.join([user_tablename, 'id'])))
        groupid = sqlalchemy.Column(sqlalchemy.types.Integer,
                                    sqlalchemy.ForeignKey(
                                        '.'.join([group_tablename, 'id'])))

    class Group(core.models.Base):
        __tablename__ = group_tablename

        id = sqlalchemy.Column(sqlalchemy.types.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.types.String(length=64),
                                    unique=True)
        users = sqlalchemy.orm.relationship("User", 
                                            secondary=UserGroup.__table__)

    class User(core.models.Base):
        __tablename__ = user_tablename

        id = sqlalchemy.Column(sqlalchemy.types.Integer, primary_key=True)
        _name = sqlalchemy.Column('name', sqlalchemy.types.String(length=64),
                                    unique=True, index=True)
        _name_salt = sqlalchemy.Column('name_salt',
                                    sqlalchemy.LargeBinary(length=8),
                                    default=lambda: os.urandom(8))
        _pass_salt = sqlalchemy.Column('pass_salt',
                                    sqlalchemy.LargeBinary(length=8),
                                    default=lambda: os.urandom(8))
        namehash = sqlalchemy.Column(sqlalchemy.types.LargeBinary(length=32),
                                        index=True)
        passhash = sqlalchemy.Column(sqlalchemy.types.LargeBinary(length=64))

        groups = sqlalchemy.orm.relationship(Group,
                                             secondary=UserGroup.__table__)

        def _get_hash(self, value, nonce, alg=hashlib.sha512):
            hash_ = alg(nonce)
            hash_.update(value.encode())
            return hash_.digest()

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, name):
            self.namehash = self._get_hash(name, self.name_salt,
                                            alg=hashlib.sha256)
            self._name = name

        @property
        def name_salt(self):
            if not self._name_salt:
                self._name_salt = os.urandom(8)
            return self._name_salt

        @property
        def pass_salt(self):
            if not self._pass_salt: 
                self._pass_salt = os.urandom(8)
            return self._pass_salt

        @property
        def password(self):
            raise ValueError("Cannot get a password.")

        @password.setter
        def password(self, password):
            self.passhash = self._get_hash(password, self.pass_salt)

        def check_password(self, password):
            return self.passhash == self._get_hash(password, self.pass_salt)

        def __json__(self, request):
            return {
                'id': self.id,
                'name': self.name
            }

    def get_user(userident):
        """Get user based on namehash. This is so we don't expose any
        details about the user in cookies that may be transmitted
        unencrypted.
        """

        try:
            return (core.models.Session
                        .query(User)
                        .filter(User.namehash==userident)
                        .one())
        except sqlalchemy.orm.exc.NoResultFound:
            return None