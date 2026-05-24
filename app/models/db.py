import sqlite3
import os
import hashlib
import secrets

def _project_root():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_connection():
    db_dir = os.path.join(_project_root(), "database")
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, "app.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

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
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS roles(
                id integer PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                code TEXT NOT NULL UNIQUE,
                description TEXT DEFAULT '',
                status INTEGER NOT NULL DEFAULT 1,
                is_system INTEGER NOT NULL DEFAULT 0,
                create_at TEXT NOT NULL DEFAULT(datetime('now')),
                update_at TEXT NOT NULL DEFAULT(datetime('now'))
            )
        ''')
        
        conn.execute('''
            CREATE TRIGGER IF NOT EXISTS update_roles_timestamp
            AFTER UPDATE ON roles
            BEGIN
                UPDATE roles SET update_at = datetime('now') WHERE id = NEW.id;
            END
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS menus(
                id integer PRIMARY KEY AUTOINCREMENT,
                parent_id INTEGER NOT NULL DEFAULT 0,
                name TEXT NOT NULL,
                icon TEXT DEFAULT '',
                url TEXT DEFAULT '',
                sort INTEGER NOT NULL DEFAULT 0,
                status INTEGER NOT NULL DEFAULT 1,
                code TEXT DEFAULT '',
                create_at TEXT NOT NULL DEFAULT(datetime('now'))
            )
        ''')
        
        try:
            conn.execute('''ALTER TABLE menus ADD COLUMN code TEXT DEFAULT '' ''')
        except Exception:
            pass
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS role_menu(
                id integer PRIMARY KEY AUTOINCREMENT,
                role_id INTEGER NOT NULL,
                menu_id INTEGER NOT NULL,
                UNIQUE(role_id, menu_id)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS user_role(
                id integer PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                UNIQUE(user_id, role_id)
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS ai_models(
                id integer PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                code TEXT NOT NULL UNIQUE,
                base_url TEXT NOT NULL,
                api_key TEXT NOT NULL,
                model_name TEXT NOT NULL,
                description TEXT DEFAULT '',
                status INTEGER NOT NULL DEFAULT 1,
                is_default INTEGER NOT NULL DEFAULT 0,
                sort INTEGER NOT NULL DEFAULT 0,
                total_tokens INTEGER NOT NULL DEFAULT 0,
                total_calls INTEGER NOT NULL DEFAULT 0,
                create_at TEXT NOT NULL DEFAULT(datetime('now')),
                update_at TEXT NOT NULL DEFAULT(datetime('now'))
            )
        ''')
        
        conn.execute('''
            CREATE TRIGGER IF NOT EXISTS update_ai_models_timestamp
            AFTER UPDATE ON ai_models
            BEGIN
                UPDATE ai_models SET update_at = datetime('now') WHERE id = NEW.id;
            END
        ''')
        
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
        
        super_role = conn.execute("SELECT id FROM roles WHERE code='super_admin'").fetchone()
        if not super_role:
            try:
                conn.execute(
                    "INSERT INTO roles(name, code, description, is_system) VALUES (?, ?, ?, ?)",
                    ('超级管理员', 'super_admin', '系统内置超级管理员角色，拥有所有权限', 1)
                )
                print("默认超级管理员角色已创建")
            except Exception:
                pass
        
        top_menu = conn.execute("SELECT id FROM menus WHERE code='dashboard'").fetchone()
        if not top_menu:
            try:
                default_menus = [
                    (0, '首页', 'fas fa-home', '/admin/welcome', 1, 'dashboard'),
                    (0, '用户管理', 'fas fa-users', '', 2, 'user_mgmt'),
                    (2, '用户列表', 'fas fa-list', '/admin/user/list', 1, 'user_list'),
                    (0, '系统管理', 'fas fa-cogs', '', 3, 'system_mgmt'),
                    (4, '功能管理', 'fas fa-th-list', '/admin/menu/list', 1, 'menu_list'),
                    (4, '角色管理', 'fas fa-user-shield', '/admin/role/list', 2, 'role_list'),
                    (4, '权限管理', 'fas fa-key', '/admin/permission/list', 3, 'permission_list'),
                ]
                for parent_id, name, icon, url, sort, code in default_menus:
                    conn.execute(
                        "INSERT INTO menus(parent_id, name, icon, url, sort, code) VALUES (?, ?, ?, ?, ?, ?)",
                        (parent_id, name, icon, url, sort, code)
                    )
                print("默认菜单数据已创建")
            except Exception:
                pass
        
        default_model = conn.execute("SELECT id FROM ai_models WHERE code='default_deepseek'").fetchone()
        if not default_model:
            try:
                conn.execute(
                    "INSERT INTO ai_models(name, code, base_url, api_key, model_name, description, is_default, sort) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    ('DeepSeek-V3', 'default_deepseek', 'https://aigc-api.aitoolcore.com/api/v1', 'sk-aigc-11db9b6d2bfcc7223c2e546e7388981f11169a4a', 'deepseek-v3', 'DeepSeek V3 默认模型', 1, 1)
                )
                print("默认AI模型已创建: DeepSeek-V3")
            except Exception:
                pass
        
        admin_user = conn.execute("SELECT id FROM users WHERE username='admin' AND is_admin=1").fetchone()
        super_role = conn.execute("SELECT id FROM roles WHERE code='super_admin'").fetchone()
        if admin_user and super_role:
            existing = conn.execute("SELECT id FROM user_role WHERE user_id=? AND role_id=?", (admin_user["id"], super_role["id"])).fetchone()
            if not existing:
                conn.execute("INSERT INTO user_role(user_id, role_id) VALUES (?, ?)", (admin_user["id"], super_role["id"]))
                print("admin用户已绑定超级管理员角色")
