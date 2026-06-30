from company_blog import app, db
from company_blog.models import User, BlogCategory

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

    # ✅ カテゴリ（これ追加！！）
    existing_category = BlogCategory.query.first()

    if not existing_category:
        category1 = BlogCategory(category="Test Category")
        db.session.add(category1)
        print("Category created")

    db.session.commit()


print("DB initialized")
