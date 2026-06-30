from company_blog import app, db

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run()
    # app.run(debug=True)
    # デバッグモードでアプリケーションを実行するための設定です。デバッグモードでは、コードの変更が自動的に反映され、エラーが発生した場合に詳細なエラーメッセージが表示されます。
