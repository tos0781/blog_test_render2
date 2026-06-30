from company_blog import app, db
from company_blog.models import User

with app.app_context():
    db.create_all()

    # ✅ 既存チェック
    existing_user = User.query.filter_by(email="admin_user@test.com").first()

    if not existing_user:
        user1 = User(
            email="admin_user@test.com",
            username="Admin User",
            password="123",
            administrator="1",
        )

        # user1.password = "123"  # ← setterがある前提
        # user1.administrator = True  # ← boolに変更

        db.session.add(user1)
        db.session.commit()
        print("User created")
    else:
        print("User already exists")

print("DB initialized")
