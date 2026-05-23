# 数据库链接与建表
import os
import sqlite3

# 获得项目根路径的方法
def _project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,os.pardir))

DB_PATH = os.path.join(_project_root(),"database","app.db")

# 获得数据库连接
def get_connection():
    os.makedirs(os.path.dirname(DB_PATH),exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# 初始化数据库表
def init_db():
    with get_connection() as conn:
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS users(
                id integer PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                email TEXT DEFAULT '',
                phone TEXT DEFAULT '',
                status INTEGER NOT NULL DEFAULT 1,
                is_admin INTEGER NOT NULL DEFAULT 0,
                create_at TEXT NOT NULL DEFAULT(datetime('now')),
                update_at TEXT NOT NULL DEFAULT(datetime('now'))
            )
            '''
        )
        
        try:
            conn.execute('''ALTER TABLE users ADD COLUMN email TEXT DEFAULT '' ''')
        except Exception:
            pass
        try:
            conn.execute('''ALTER TABLE users ADD COLUMN phone TEXT DEFAULT '' ''')
        except Exception:
            pass
        try:
            conn.execute('''ALTER TABLE users ADD COLUMN status INTEGER NOT NULL DEFAULT 1 ''')
        except Exception:
            pass
        try:
            conn.execute('''ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0 ''')
        except Exception:
            pass
        try:
            conn.execute('''ALTER TABLE users ADD COLUMN update_at TEXT NOT NULL DEFAULT(datetime('now')) ''')
        except Exception:
            pass
        
        conn.execute('''
            CREATE TRIGGER IF NOT EXISTS update_users_timestamp
            AFTER UPDATE ON users
            BEGIN
                UPDATE users SET update_at = datetime('now') WHERE id = NEW.id;
            END
        ''')
        
        import hashlib
        import secrets
        existing_admin = conn.execute("SELECT id FROM users WHERE username='admin' AND is_admin=1").fetchone()
        if not existing_admin:
            salt = secrets.token_bytes(16)
            dk = hashlib.pbkdf2_hmac('sha256', 'admin888'.encode('utf-8'), salt, 100_000)
            password_hash = dk.hex()
            try:
                conn.execute(
                    "INSERT INTO users(username, password_hash, salt, is_admin, email) VALUES (?, ?, ?, ?, ?)",
                    ('admin', password_hash, salt.hex(), 1, 'admin@cnagentos.com')
                )
                print("默认管理员账号已创建: admin/admin888")
            except Exception:
                pass