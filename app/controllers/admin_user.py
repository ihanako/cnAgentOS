import json
import tornado.web

from app.controllers.admin_home import AdminBaseHandler
from app.models.user import UserRepository

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
        
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "msg": "", "data": dict(user)}, ensure_ascii=False))
    
    @tornado.web.authenticated
    def post(self):
        user_id = int(self.get_body_argument("id", 0))
        username = (self.get_body_argument("username", "") or "").strip()
        email = (self.get_body_argument("email", "") or "").strip()
        phone = (self.get_body_argument("phone", "") or "").strip()
        password = self.get_body_argument("password", "")
        status = int(self.get_body_argument("status", 1))
        is_admin = int(self.get_body_argument("is_admin", 0))
        
        if not user_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        
        if not username:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "用户名不能为空"}, ensure_ascii=False))
        
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
        
        count = UserRepository.batch_delete_user(user_ids)
        
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "msg": f"成功删除{count}个用户"}, ensure_ascii=False))
