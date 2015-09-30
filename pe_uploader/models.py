from sqlalchemy.orm import synonym
from werkzeug import check_password_hash, generate_password_hash

from pe_uploader import db


class Files(db.Model):
    """
    アップロードするファイルを管理するクラス

    id, ファイル名, ファイルパス
    """
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)  # ファイル名
    hashed = db.Column(db.Text)  # ファイル名をハッシュ化したもの
    path = db.Column(db.Text)  # 相対パス

    def __repr__(self):
        return "<File id={id} name={name} path={path}>".format(
            id=self.id, name=self.name, path=self.path)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default='', nullable=False)
    _password = db.Column('password', db.String(100), nullable=False)

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        if password:
            password = password.strip()
        self._password = generate_password_hash(password)
    password_descriptor = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password_descriptor)

    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)

    @classmethod
    def authenticate(cls, query, name, password):
        user = query(cls).filter(cls.name == name).first()
        if user is None:
            return None, False
        return user, user.check_password(password)

    def __repr__(self):
        return '<User id={self.id} email={self.email!r}'.format(self=self)


def init():
    db.create_all()
