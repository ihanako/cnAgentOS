from app.models.db import get_connection

class MenuRepository:
    @staticmethod
    def get_menu_list():
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM menus ORDER BY parent_id ASC, sort ASC, id ASC").fetchall()
            return [dict(r) for r in rows]
    
    @staticmethod
    def get_menu_tree():
        menus = MenuRepository.get_menu_list()
        menu_map = {}
        tree = []
        for m in menus:
            m['children'] = []
            menu_map[m['id']] = m
        for m in menus:
            if m['parent_id'] == 0:
                tree.append(m)
            else:
                parent = menu_map.get(m['parent_id'])
                if parent:
                    parent['children'].append(m)
        return tree
    
    @staticmethod
    def get_top_menus():
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM menus WHERE parent_id=0 AND status=1 ORDER BY sort ASC, id ASC").fetchall()
            return [dict(r) for r in rows]
    
    @staticmethod
    def get_child_menus(parent_id):
        with get_connection() as conn:
            rows = conn.execute("SELECT * FROM menus WHERE parent_id=? AND status=1 ORDER BY sort ASC, id ASC", (parent_id,)).fetchall()
            return [dict(r) for r in rows]
    
    @staticmethod
    def get_all_menus():
        return MenuRepository.get_menu_list()
    
    @staticmethod
    def get_menu_by_id(menu_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM menus WHERE id=?", (menu_id,)).fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def create_menu(parent_id, name, icon="", url="", sort=0, code=""):
        try:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO menus(parent_id, name, icon, url, sort, code) VALUES (?, ?, ?, ?, ?, ?)",
                    (parent_id, name, icon, url, sort, code)
                )
            return True
        except Exception:
            return False
    
    @staticmethod
    def update_menu(menu_id, parent_id=None, name=None, icon=None, url=None, sort=None, status=None, code=None):
        with get_connection() as conn:
            menu = conn.execute("SELECT * FROM menus WHERE id=?", (menu_id,)).fetchone()
            if not menu:
                return False
            
            updates, params = [], []
            if parent_id is not None:
                updates.append("parent_id=?")
                params.append(parent_id)
            if name is not None:
                updates.append("name=?")
                params.append(name)
            if icon is not None:
                updates.append("icon=?")
                params.append(icon)
            if url is not None:
                updates.append("url=?")
                params.append(url)
            if sort is not None:
                updates.append("sort=?")
                params.append(sort)
            if status is not None:
                updates.append("status=?")
                params.append(status)
            if code is not None:
                updates.append("code=?")
                params.append(code)
            
            if not updates:
                return True
            params.append(menu_id)
            try:
                conn.execute(f"UPDATE menus SET {','.join(updates)} WHERE id=?", params)
                return True
            except Exception:
                return False
    
    @staticmethod
    def delete_menu(menu_id):
        with get_connection() as conn:
            has_children = conn.execute("SELECT COUNT(*) as cnt FROM menus WHERE parent_id=?", (menu_id,)).fetchone()
            if has_children["cnt"] > 0:
                return False
            conn.execute("DELETE FROM role_menu WHERE menu_id=?", (menu_id,))
            cursor = conn.execute("DELETE FROM menus WHERE id=?", (menu_id,))
            return cursor.rowcount > 0
