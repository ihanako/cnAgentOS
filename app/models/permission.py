from app.models.db import get_connection

class PermissionRepository:
    @staticmethod
    def get_role_menus(role_id):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT m.*, rm.id as rm_id FROM menus m LEFT JOIN role_menu rm ON m.id = rm.menu_id AND rm.role_id = ? ORDER BY m.parent_id ASC, m.sort ASC",
                (role_id,)
            ).fetchall()
            return [dict(r) for r in rows]
    
    @staticmethod
    def save_role_menus(role_id, menu_ids):
        with get_connection() as conn:
            conn.execute("DELETE FROM role_menu WHERE role_id=?", (role_id,))
            if menu_ids:
                for mid in menu_ids:
                    conn.execute(
                        "INSERT INTO role_menu(role_id, menu_id) VALUES (?, ?)",
                        (role_id, mid)
                    )
            return True
    
    @staticmethod
    def get_role_menu_ids(role_id):
        with get_connection() as conn:
            rows = conn.execute("SELECT menu_id FROM role_menu WHERE role_id=?", (role_id,)).fetchall()
            return [r["menu_id"] for r in rows]
    
    @staticmethod
    def get_menu_ids_by_role(role_id):
        return PermissionRepository.get_role_menu_ids(role_id)
    
    @staticmethod
    def check_permission(role_id, menu_url):
        if not role_id:
            return False
        with get_connection() as conn:
            role = conn.execute("SELECT * FROM roles WHERE id=?", (role_id,)).fetchone()
            if role and role["is_system"]:
                return True
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM role_menu rm JOIN menus m ON rm.menu_id = m.id WHERE rm.role_id=? AND m.url=?",
                (role_id, menu_url)
            ).fetchone()
            return row["cnt"] > 0
