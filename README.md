# Django 学習用 API プロジェクト

## プロジェクト概要

Django の基礎を学ぶための最小構成 API プロジェクトです。
Django REST Framework はまだ使わず、Django 標準の `JsonResponse` で API の流れを確認します。

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

| Method | URL | 説明 |
| --- | --- | --- |
| GET | `/api/health/` | API の稼働確認 |
| GET | `/api/tasks/` | 固定のタスク一覧を返す |

## 次に学ぶ予定

- Model / Migration / ORM
- Django Admin
- Django REST Framework
- Serializer
- ViewSet / Router
- 認証・認可
- APIテスト
