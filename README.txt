webアプリ制作の勉強としてdjangoを用いて文章やイラスト・写真を投稿できる
snsアプリを作りました。
フォロー機能やコメント機能などは今後追加予定です。


django_envという仮想環境を作成し、パッケージをインストールします。

・django3.2.4
・Pillow
・django-bootstrap4
・bcrypt
・beautifulsoup4

仮想環境をアクティベートして、python manage.py runserverを実行し、
https://127.0.0.1:8000/accounts/home/を開くとホーム画面が表示されます。

Sign inを押すと、ユーザネーム、メールアドレス、パスワードを登録することができます。
登録したユーザネームとパスワードでログインすることで、投稿を見たり、新しく投稿を作ったりできます。