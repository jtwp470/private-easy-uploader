from pe_uploader import db


class Files(db.Model):
    """
    アップロードするファイルを管理するクラス

    id, ファイル名, ファイルパス
    """
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    path = db.Column(db.Text)

    def __repr__(self):
        return "<File id={id} name={name} path={path}>".format(
            id=self.id, name=self.name, path=self.path)


def init():
    db.create_all()
