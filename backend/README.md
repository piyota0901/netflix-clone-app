# backend

Describe your project here.

## データモデル(ER図)

後で記載

## 単体テスト

FastAPIで`pytest`を使用する場合は、`async def`ではなく`def`でよい。  
[FastAPI - テスト](https://fastapi.tiangolo.com/ja/tutorial/testing/#testclient)
```plaintext
テスト関数は async def ではなく、通常の def であることに注意してください。
また、クライアントへの呼び出しも通常の呼び出しであり、await を使用しません。
これにより、煩雑にならずに、pytest を直接使用できます。
```

## SQLAlchemy

- 多対多の設定
    [Many to Many](https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many)

- Query
https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#writing-select-statements-for-orm-mapped-classes

## Alembic

- SQLAlcheymからマイグレーションファイルを自動生成する場合
    ```bash
    $ rye run alembic revision --autogenerate -m "Initialize db"
    ```

- 最新版への反映
    ```bash
    $ rye run alembic upgrade head
    ```

- 手動でマイグレーションファイルを作成する場合
    ```bash
    $ rye run alembic revision -m "マイグレーションの説明"
    ```