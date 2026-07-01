import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)  # FlaskFormを使用するための設定

app.config["SECRET_KEY"] = "mysecretkey"
# 通常はこのように秘密鍵をコーディングすることはないが、わかりやすいようにコーディングしておく


basedir = os.path.abspath(os.path.dirname(__file__))
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
#     basedir, "data.sqlite"
# )
uri = os.environ.get("DATABASE_URL")
print("DEBUG DATABASE_URL =", uri, flush=True)

if uri:
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
else:
    # app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:im1046@localhost"
    # ローカル用（SQLite）
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        basedir, "data.sqlite"
    )

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# # ★★★ ここに追加 ★★★
# print("DB URI =", app.config["SQLALCHEMY_DATABASE_URI"], flush=True)


db = SQLAlchemy(app)
Migrate(app, db)


# ✅ これ追加
with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"


def localize_callback(*args, **kwargs):
    return "このページにアクセスするには、ログインが必要です。"


login_manager.localize_callback = localize_callback

# SQLiteで外部キー制約を設定するコード
# from sqlalchemy.engine import Engine
# from sqlalchemy import event

# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     # the sqlite3 driver will not set PRAGMA foreign_keys
#     # if autocommit=False; set to True temporarily
#     # ac = dbapi_connection.autocommit
#     # dbapi_connection.autocommit = True

#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()

#     # restore previous autocommit setting
#     # dbapi_connection.autocommit = ac


from company_blog.main.views import main

app.register_blueprint(main)
from company_blog.users.views import users
from company_blog.error_pages.handlers import error_pages

app.register_blueprint(users)
app.register_blueprint(error_pages)
