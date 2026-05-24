import json
import tornado.web

from app.controllers.admin_home import AdminBaseHandler
from app.models.user import UserRepository
from app.models.user_role import UserRoleRepository

class AdminUserListHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/user/list.html", title="用户管理", username=self.current_user)

class AdminUserDataHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        page = int(self.get_argument("page", 1))
        limit = int(self.get_argument("limit", 20))
        keyword = (self.get_argument("keyword", "") or "").strip()
        
        result = UserRepository.get_user_list(page=page, page_size=limit, keyword=keyword)
        user_ids = [u["id"] for u in result["data"]]
        roles_map = UserRoleRepository.get_users_with_roles(user_ids)
        
        for u in result["data"]:
            u["roles"] = ",".join(roles_map.get(u["id"], []))
            u["is_default_admin"] = (u["username"] == "admin" and u["is_admin"])
        
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({
            "code": 0,
            "msg": "",
            "count": result["total"],
            "data": result["data"]
        }, ensure_ascii=False))

class AdminUserAddHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        username = (self.get_body_argument("username", "") or "").strip()
        password = self.get_body_argument("password", "")
        email = (self.get_body_argument("email", "") or "").strip()
        phone = (self.get_body_argument("phone", "") or "").strip()
        is_admin = int(self.get_body_argument("is_admin", 0))
        role_ids_str = self.get_body_argument("role_ids", "")
        role_ids = [int(x) for x in role_ids_str.split(",") if x.strip()] if role_ids_str else []
        
        if not username or not password:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "用户名和密码不能为空"}, ensure_ascii=False))
        
        if len(username) < 3 or len(username) > 20:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "用户名长度必须在3-20个字符之间"}, ensure_ascii=False))
        
        if len(password) < 6:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "密码长度不能少于6位"}, ensure_ascii=False))
        
        success = UserRepository.create_user(username=username, password=password, email=email, phone=phone, is_admin=is_admin)
        
        self.set_header("Content-Type", "application/json; charset=utf-8")
        if success:
            user = UserRepository.get_user_by_username(username)
            if user and role_ids:
                UserRoleRepository.set_user_roles(user["id"], role_ids)
            self.write(json.dumps({"code": 0, "msg": "新增成功"}, ensure_ascii=False))
        else:
            self.write(json.dumps({"code": 1, "msg": "用户名已存在"}, ensure_ascii=False))

class AdminUserEditHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_id = int(self.get_argument("id", 0))
        if not user_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        
        user = UserRepository.get_user_by_id(user_id)
        if not user:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "用户不存在"}, ensure_ascii=False))
        
        role_ids = UserRoleRepository.get_user_role_ids(user_id)
        result = dict(user)
        result["role_ids"] = ",".join(str(r) for r in role_ids)
        
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "msg": "", "data": result}, ensure_ascii=False))
    
    @tornado.web.authenticated
    def post(self):
        user_id = int(self.get_body_argument("id", 0))
        username = (self.get_body_argument("username", "") or "").strip()
        email = (self.get_body_argument("email", "") or "").strip()
        phone = (self.get_body_argument("phone", "") or "").strip()
        password = self.get_body_argument("password", "")
        status = int(self.get_body_argument("status", 1))
        is_admin = int(self.get_body_argument("is_admin", 0))
        role_ids_str = self.get_body_argument("role_ids", "")
        role_ids = [int(x) for x in role_ids_str.split(",") if x.strip()] if role_ids_str else []
        
        if not user_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        
        if not username:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "用户名不能为空"}, ensure_ascii=False))
        
        existing_user = UserRepository.get_user_by_id(user_id)
        if existing_user and existing_user["username"] == "admin" and existing_user["is_admin"]:
            if password and len(password) < 6:
                self.set_header("Content-Type", "application/json; charset=utf-8")
                return self.write(json.dumps({"code": 1, "msg": "密码长度不能少于6位"}, ensure_ascii=False))
            if password:
                UserRepository.update_user(user_id=user_id, password=password)
            if role_ids:
                UserRoleRepository.set_user_roles(user_id, role_ids)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 0, "msg": "修改成功"}, ensure_ascii=False))
        
        if password and len(password) < 6:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "密码长度不能少于6位"}, ensure_ascii=False))
        
        success = UserRepository.update_user(
            user_id=user_id,
            username=username,
            email=email,
            phone=phone,
            password=password if password else None,
            status=status,
            is_admin=is_admin
        )
        
        if success and role_ids:
            UserRoleRepository.set_user_roles(user_id, role_ids)
        
        self.set_header("Content-Type", "application/json; charset=utf-8")
        if success:
            self.write(json.dumps({"code": 0, "msg": "修改成功"}, ensure_ascii=False))
        else:
            self.write(json.dumps({"code": 1, "msg": "修改失败，用户名可能已存在"}, ensure_ascii=False))

class AdminUserDeleteHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        user_id = int(self.get_body_argument("id", 0))
        if not user_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        
        user = UserRepository.get_user_by_id(user_id)
        if user and user["username"] == "admin" and user["is_admin"]:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "默认管理员不能删除"}, ensure_ascii=False))
        
        success = UserRepository.delete_user(user_id)
        
        self.set_header("Content-Type", "application/json; charset=utf-8")
        if success:
            self.write(json.dumps({"code": 0, "msg": "删除成功"}, ensure_ascii=False))
        else:
            self.write(json.dumps({"code": 1, "msg": "删除失败"}, ensure_ascii=False))

class AdminUserBatchDeleteHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        ids_str = self.get_body_argument("ids", "")
        if not ids_str:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "请选择要删除的用户"}, ensure_ascii=False))
        
        try:
            user_ids = [int(x.strip()) for x in ids_str.split(",") if x.strip()]
        except ValueError:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数格式错误"}, ensure_ascii=False))
        
        for uid in user_ids:
            user = UserRepository.get_user_by_id(uid)
            if user and user["username"] == "admin" and user["is_admin"]:
                self.set_header("Content-Type", "application/json; charset=utf-8")
                return self.write(json.dumps({"code": 1, "msg": "默认管理员不能删除，已跳过"}, ensure_ascii=False))
        
        count = UserRepository.batch_delete_user(user_ids)
        
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "msg": f"成功删除{count}个用户"}, ensure_ascii=False))
