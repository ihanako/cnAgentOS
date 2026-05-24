import json
import tornado.web
from app.controllers.admin_home import AdminBaseHandler
from app.models.role import RoleRepository

class AdminRoleListHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/role/list.html", title="角色管理", username=self.current_user)

class AdminRoleDataHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        page = int(self.get_argument("page", 1))
        limit = int(self.get_argument("limit", 20))
        keyword = (self.get_argument("keyword", "") or "").strip()
        result = RoleRepository.get_role_list(page=page, page_size=limit, keyword=keyword)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "msg": "", "count": result["total"], "data": result["data"]}, ensure_ascii=False))

class AdminRoleAddHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        name = (self.get_body_argument("name", "") or "").strip()
        code = (self.get_body_argument("code", "") or "").strip()
        description = (self.get_body_argument("description", "") or "").strip()
        status = int(self.get_body_argument("status", 1))
        if not name or not code:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "角色名称和编码不能为空"}, ensure_ascii=False))
        success = RoleRepository.create_role(name=name, code=code, description=description, status=status)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0 if success else 1, "msg": "新增成功" if success else "角色名称或编码已存在"}, ensure_ascii=False))

class AdminRoleEditHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        role_id = int(self.get_argument("id", 0))
        if not role_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        role = RoleRepository.get_role_by_id(role_id)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "data": dict(role) if role else {}}, ensure_ascii=False))
    
    @tornado.web.authenticated
    def post(self):
        role_id = int(self.get_body_argument("id", 0))
        name = (self.get_body_argument("name", "") or "").strip()
        code = (self.get_body_argument("code", "") or "").strip()
        description = (self.get_body_argument("description", "") or "").strip()
        status = int(self.get_body_argument("status", 1))
        if not role_id or not name or not code:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        success = RoleRepository.update_role(role_id=role_id, name=name, code=code, description=description, status=status)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        if success:
            self.write(json.dumps({"code": 0, "msg": "修改成功"}, ensure_ascii=False))
        else:
            self.write(json.dumps({"code": 1, "msg": "修改失败(系统角色不可修改)"}, ensure_ascii=False))

class AdminRoleDeleteHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        role_id = int(self.get_body_argument("id", 0))
        if not role_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        success = RoleRepository.delete_role(role_id)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0 if success else 1, "msg": "删除成功" if success else "删除失败(系统角色不可删除)"}, ensure_ascii=False))

class AdminRoleAllHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        roles = RoleRepository.get_all_roles()
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "data": roles}, ensure_ascii=False))
