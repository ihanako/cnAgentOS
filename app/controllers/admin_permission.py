import json
import tornado.web
from app.controllers.admin_home import AdminBaseHandler
from app.models.permission import PermissionRepository
from app.models.menu import MenuRepository
from app.models.role import RoleRepository

class AdminPermissionListHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/permission/list.html", title="权限管理", username=self.current_user)

class AdminPermissionDataHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        role_id = int(self.get_argument("role_id", 0))
        if not role_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "请选择角色"}, ensure_ascii=False))
        menus = MenuRepository.get_menu_tree()
        checked_ids = PermissionRepository.get_role_menu_ids(role_id)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "data": {"menus": menus, "checked_ids": checked_ids}}, ensure_ascii=False))

class AdminPermissionSaveHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        role_id = int(self.get_body_argument("role_id", 0))
        menu_ids_str = self.get_body_argument("menu_ids", "")
        if not role_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "请选择角色"}, ensure_ascii=False))
        menu_ids = [int(x) for x in menu_ids_str.split(",") if x.strip()] if menu_ids_str else []
        success = PermissionRepository.save_role_menus(role_id, menu_ids)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0 if success else 1, "msg": "保存成功" if success else "保存失败"}, ensure_ascii=False))

class AdminPermissionRoleMenusHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        role_id = int(self.get_argument("role_id", 0))
        menus = MenuRepository.get_menu_tree()
        checked_ids = PermissionRepository.get_role_menu_ids(role_id)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "data": {"menus": menus, "checked_ids": checked_ids}}, ensure_ascii=False))
