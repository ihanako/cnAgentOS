from app.models.db import get_connection

class UserRoleRepository:
    @staticmethod
    def get_user_roles(user_id):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT r.* FROM roles r JOIN user_role ur ON r.id = ur.role_id WHERE ur.user_id = ? ORDER BY r.id ASC",
                (user_id,)
            ).fetchall()
            return [dict(r) for r in rows]
    
    @staticmethod
    def get_user_role_ids(user_id):
        with get_connection() as conn:
            rows = conn.execute("SELECT role_id FROM user_role WHERE user_id = ?", (user_id,)).fetchall()
            return [r["role_id"] for r in rows]
    
    @staticmethod
    def set_user_roles(user_id, role_ids):
        with get_connection() as conn:
            conn.execute("DELETE FROM user_role WHERE user_id = ?", (user_id,))
            if role_ids:
                for rid in role_ids:
                    conn.execute("INSERT INTO user_role(user_id, role_id) VALUES (?, ?)", (user_id, rid))
            return True
    
    @staticmethod
    def get_users_with_roles(user_ids):
        if not user_ids:
            return {}
        placeholders = ",".join("?" for _ in user_ids)
        with get_connection() as conn:
            rows = conn.execute(
                f"SELECT ur.user_id, r.name, r.code FROM user_role ur JOIN roles r ON ur.role_id = r.id WHERE ur.user_id IN ({placeholders})",
                user_ids
            ).fetchall()
        result = {}
        for r in rows:
            uid = r["user_id"]
            if uid not in result:
                result[uid] = []
            result[uid].append(r["name"])
        return result
