# Django 学習用 API プロジェクト

## プロジェクト概要

Django の基礎を学ぶための最小構成 API プロジェクトです。
Django REST Framework を使い、ユーザー認証、DB保存、APIテストまで確認できる構成です。

## 環境構築手順

Python を確認します。

```bash
python --version
```

仮想環境を作成します。

```bash
python -m venv .venv
```

## 仮想環境の有効化方法

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

Codex などで activate が維持されない場合は、仮想環境内の Python を直接使います。

Windows:

```bash
.venv\Scripts\python
```

macOS / Linux:

```bash
.venv/bin/python
```

## 依存関係のインストール方法

```bash
python -m pip install -r requirements.txt
```

## マイグレーション実行方法

```bash
python manage.py migrate
```

## サーバー起動方法

```bash
python manage.py runserver
```

起動後、以下にアクセスします。

```txt
http://127.0.0.1:8000/
```

## API一覧

| Method | URL | 認証 | 説明 |
| --- | --- | --- | --- |
| GET | `/api/health/` | 不要 | API の稼働確認 |
| POST | `/api/auth/register/` | 不要 | ユーザー登録とトークン発行 |
| POST | `/api/auth/login/` | 不要 | ログインとトークン発行 |
| POST | `/api/auth/logout/` | 必要 | ログアウト。現在のトークンを削除 |
| GET | `/api/auth/me/` | 必要 | ログイン中ユーザーの情報を返す |
| GET | `/api/tasks/` | 必要 | 自分のタスク一覧を返す |
| POST | `/api/tasks/` | 必要 | 自分のタスクを作成する |
| GET | `/api/tasks/<id>/` | 必要 | 自分のタスク詳細を返す |
| PUT | `/api/tasks/<id>/` | 必要 | 自分のタスクを全更新する |
| PATCH | `/api/tasks/<id>/` | 必要 | 自分のタスクを部分更新する |
| DELETE | `/api/tasks/<id>/` | 必要 | 自分のタスクを削除する |

## 認証方法

登録またはログインすると、以下のようなレスポンスで `token` が返ります。

```json
{
  "token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com"
  }
}
```

認証が必要なAPIでは、HTTPヘッダーにトークンを付けます。

```txt
Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## リクエスト例

ユーザー登録:

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"alice\",\"email\":\"alice@example.com\",\"password\":\"strong-pass-123\"}"
```

タスク作成:

```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -d "{\"title\":\"Learn Django REST Framework\"}"
```

タスク一覧:

```bash
curl http://127.0.0.1:8000/api/tasks/ \
  -H "Authorization: Token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

## テスト実行方法

```bash
python manage.py test
```

## 次に学ぶ予定

- ViewSet / Router
- Pagination / Filtering
- 権限クラスのカスタマイズ
- 本番用設定
