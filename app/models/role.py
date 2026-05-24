import secrets
import hashlib
from app.models.db import get_connection

def _hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return dk.hex()

class RoleRepository:
    @staticmethod
    def get_role_list(page=1, page_size=20, keyword=""):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            if keyword:
                count_row = conn.execute(
                    "SELECT COUNT(*) as total FROM roles WHERE name LIKE ? OR code LIKE ?",
                    (f"%{keyword}%", f"%{keyword}%")
                ).fetchone()
                total = count_row["total"]
                rows = conn.execute(
                    "SELECT * FROM roles WHERE name LIKE ? OR code LIKE ? ORDER BY is_system DESC, id ASC LIMIT ? OFFSET ?",
                    (f"%{keyword}%", f"%{keyword}%", page_size, offset)
                ).fetchall()
            else:
                count_row = conn.execute("SELECT COUNT(*) as total FROM roles").fetchone()
                total = count_row["total"]
                rows = conn.execute(
                    "SELECT * FROM roles ORDER BY is_system DESC, id ASC LIMIT ? OFFSET ?",
                    (page_size, offset)
                ).fetchall()
        return {"data": [dict(r) for r in rows], "total": total, "page": page, "page_size": page_size}
    
    @staticmethod
    def get_role_by_id(role_id):
        with get_connection() as conn:
            return conn.execute("SELECT * FROM roles WHERE id=?", (role_id,)).fetchone()
    
    @staticmethod
    def create_role(name, code, description="", status=1):
        try:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO roles(name, code, description, status) VALUES (?, ?, ?, ?)",
                    (name, code, description, status)
                )
            return True
        except Exception:
            return False
    
    @staticmethod
    def update_role(role_id, name=None, code=None, description=None, status=None):
        with get_connection() as conn:
            role = conn.execute("SELECT * FROM roles WHERE id=?", (role_id,)).fetchone()
            if not role:
                return False
            if role["is_system"]:
                return False
            
            updates, params = [], []
            if name is not None:
                updates.append("name=?")
                params.append(name)
            if code is not None:
                updates.append("code=?")
                params.append(code)
            if description is not None:
                updates.append("description=?")
                params.append(description)
            if status is not None:
                updates.append("status=?")
                params.append(status)
            
            if not updates:
                return True
            params.append(role_id)
            try:
                conn.execute(f"UPDATE roles SET {','.join(updates)} WHERE id=?", params)
                return True
            except Exception:
                return False
    
    @staticmethod
    def delete_role(role_id):
        with get_connection() as conn:
            role = conn.execute("SELECT * FROM roles WHERE id=?", (role_id,)).fetchone()
            if not role or role["is_system"]:
                return False
            conn.execute("DELETE FROM role_menu WHERE role_id=?", (role_id,))
            cursor = conn.execute("DELETE FROM roles WHERE id=?", (role_id,))
            return cursor.rowcount > 0
    
    @staticmethod
    def get_all_roles():
        with get_connection() as conn:
            return [dict(r) for r in conn.execute("SELECT * FROM roles WHERE status=1 ORDER BY id ASC").fetchall()]
    
    @staticmethod
    def get_role_menu_ids(role_id):
        with get_connection() as conn:
            rows = conn.execute("SELECT menu_id FROM role_menu WHERE role_id=?", (role_id,)).fetchall()
            return [r["menu_id"] for r in rows]
