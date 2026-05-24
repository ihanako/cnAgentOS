from app.models.db import get_connection

class ModelConfigRepository:
    @staticmethod
    def get_model_list(page=1, page_size=20, keyword=""):
        offset = (page - 1) * page_size
        with get_connection() as conn:
            if keyword:
                count_row = conn.execute(
                    "SELECT COUNT(*) as total FROM ai_models WHERE name LIKE ? OR code LIKE ? OR model_name LIKE ?",
                    (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
                ).fetchone()
                total = count_row["total"]
                rows = conn.execute(
                    "SELECT * FROM ai_models WHERE name LIKE ? OR code LIKE ? OR model_name LIKE ? ORDER BY sort ASC, id DESC LIMIT ? OFFSET ?",
                    (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", page_size, offset)
                ).fetchall()
            else:
                count_row = conn.execute("SELECT COUNT(*) as total FROM ai_models").fetchone()
                total = count_row["total"]
                rows = conn.execute(
                    "SELECT * FROM ai_models ORDER BY sort ASC, id DESC LIMIT ? OFFSET ?",
                    (page_size, offset)
                ).fetchall()
        return {"data": [dict(r) for r in rows], "total": total, "page": page, "page_size": page_size}
    
    @staticmethod
    def get_model_by_id(model_id):
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM ai_models WHERE id=?", (model_id,)).fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def create_model(name, code, base_url, api_key, model_name, description="", status=1, is_default=0, sort=0):
        try:
            with get_connection() as conn:
                if is_default:
                    conn.execute("UPDATE ai_models SET is_default=0")
                conn.execute(
                    "INSERT INTO ai_models(name, code, base_url, api_key, model_name, description, status, is_default, sort) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (name, code, base_url, api_key, model_name, description, status, is_default, sort)
                )
            return True
        except Exception:
            return False
    
    @staticmethod
    def update_model(model_id, name=None, base_url=None, api_key=None, model_name=None, description=None, status=None, is_default=None, sort=None):
        with get_connection() as conn:
            model = conn.execute("SELECT * FROM ai_models WHERE id=?", (model_id,)).fetchone()
            if not model:
                return False
            
            updates, params = [], []
            if name is not None:
                updates.append("name=?"); params.append(name)
            if base_url is not None:
                updates.append("base_url=?"); params.append(base_url)
            if api_key is not None:
                updates.append("api_key=?"); params.append(api_key)
            if model_name is not None:
                updates.append("model_name=?"); params.append(model_name)
            if description is not None:
                updates.append("description=?"); params.append(description)
            if status is not None:
                updates.append("status=?"); params.append(status)
            if sort is not None:
                updates.append("sort=?"); params.append(sort)
            if is_default is not None and is_default:
                conn.execute("UPDATE ai_models SET is_default=0 WHERE id!=?", (model_id,))
                updates.append("is_default=?"); params.append(is_default)
            
            if not updates:
                return True
            params.append(model_id)
            try:
                conn.execute(f"UPDATE ai_models SET {','.join(updates)} WHERE id=?", params)
                return True
            except Exception:
                return False
    
    @staticmethod
    def delete_model(model_id):
        with get_connection() as conn:
            cursor = conn.execute("DELETE FROM ai_models WHERE id=?", (model_id,))
            return cursor.rowcount > 0
    
    @staticmethod
    def increment_stats(model_id, tokens_used):
        with get_connection() as conn:
            conn.execute(
                "UPDATE ai_models SET total_tokens = total_tokens + ?, total_calls = total_calls + 1 WHERE id=?",
                (tokens_used, model_id)
            )
    
    @staticmethod
    def get_default_model():
        with get_connection() as conn:
            row = conn.execute("SELECT * FROM ai_models WHERE is_default=1 AND status=1 LIMIT 1").fetchone()
            return dict(row) if row else None
    
    @staticmethod
    def set_default_model(model_id):
        with get_connection() as conn:
            conn.execute("UPDATE ai_models SET is_default=0")
            conn.execute("UPDATE ai_models SET is_default=1 WHERE id=?", (model_id,))
            return True
