import hashlib
import secrets
import sqlite3

from app.models.db import get_connection

def _hash_password(password:str,salt:bytes) -> str:
    dk=hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),salt,100_000)
    return dk.hex()

class UserRepository:
    @staticmethod
    def create_user(username:str,password:str,email:str="",phone:str="",is_admin:int=0) -> bool:
        salt=secrets.token_bytes(16)
        password_hash=_hash_password(password,salt)

        try:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO users(username,password_hash,salt,email,phone,is_admin) VALUES(?,?,?,?,?,?)",
                    (username,password_hash,salt.hex(),email,phone,is_admin)
                )
            return True
        except sqlite3.IntegrityError:
            return False
    
    @staticmethod
    def get_user_by_username(username:str):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id,username,password_hash,salt,email,phone,status,is_admin,create_at,update_at FROM users WHERE username =?",
                (username,)
            ).fetchone()
        return row
    
    @staticmethod
    def verify_user(username:str,password:str) -> bool:
        row=UserRepository.get_user_by_username(username)
        if not row:
            return False
        
        salt=bytes.fromhex(row["salt"])
        return _hash_password(password,salt)==row["password_hash"]
    
    @staticmethod
    def get_user_by_id(user_id:int):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id,username,email,phone,status,is_admin,create_at,update_at FROM users WHERE id=?",
                (user_id,)
            ).fetchone()
        return row
    
    @staticmethod
    def get_user_list(page:int=1, page_size:int=20, keyword:str="") -> tuple:
        offset = (page - 1) * page_size
        with get_connection() as conn:
            if keyword:
                count_row = conn.execute(
                    "SELECT COUNT(*) as total FROM users WHERE username LIKE ? OR email LIKE ? OR phone LIKE ?",
                    (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%")
                ).fetchone()
                total = count_row["total"]
                
                rows = conn.execute(
                    "SELECT id,username,email,phone,status,is_admin,create_at,update_at FROM users WHERE username LIKE ? OR email LIKE ? OR phone LIKE ? ORDER BY id DESC LIMIT ? OFFSET ?",
                    (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", page_size, offset)
                ).fetchall()
            else:
                count_row = conn.execute("SELECT COUNT(*) as total FROM users").fetchone()
                total = count_row["total"]
                
                rows = conn.execute(
                    "SELECT id,username,email,phone,status,is_admin,create_at,update_at FROM users ORDER BY id DESC LIMIT ? OFFSET ?",
                    (page_size, offset)
                ).fetchall()
        
        return {"data": [dict(row) for row in rows], "total": total, "page": page, "page_size": page_size}
    
    @staticmethod
    def update_user(user_id:int, username:str=None, email:str=None, phone:str=None, password:str=None, status:int=None, is_admin:int=None) -> bool:
        with get_connection() as conn:
            user = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
            if not user:
                return False
            
            updates = []
            params = []
            
            if username is not None and username != user["username"]:
                updates.append("username=?")
                params.append(username)
            if email is not None:
                updates.append("email=?")
                params.append(email)
            if phone is not None:
                updates.append("phone=?")
                params.append(phone)
            if status is not None:
                updates.append("status=?")
                params.append(status)
            if is_admin is not None:
                updates.append("is_admin=?")
                params.append(is_admin)
            if password:
                salt = secrets.token_bytes(16)
                password_hash = _hash_password(password, salt)
                updates.append("password_hash=?")
                updates.append("salt=?")
                params.extend([password_hash, salt.hex()])
            
            if not updates:
                return True
            
            params.append(user_id)
            try:
                conn.execute(f"UPDATE users SET {','.join(updates)} WHERE id=?", params)
                return True
            except sqlite3.IntegrityError:
                return False
    
    @staticmethod
    def delete_user(user_id:int) -> bool:
        with get_connection() as conn:
            cursor = conn.execute("DELETE FROM users WHERE id=?", (user_id,))
            return cursor.rowcount > 0
    
    @staticmethod
    def batch_delete_user(user_ids:list) -> int:
        if not user_ids:
            return 0
        placeholders = ",".join("?" for _ in user_ids)
        with get_connection() as conn:
            cursor = conn.execute(f"DELETE FROM users WHERE id IN ({placeholders})", user_ids)
            return cursor.rowcount