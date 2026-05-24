import json
import tornado.web
from app.controllers.admin_home import AdminBaseHandler
from app.models.menu import MenuRepository

class AdminMenuListHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/menu/list.html", title="功能管理", username=self.current_user)

class AdminMenuDataHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        menus = MenuRepository.get_menu_tree()
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "msg": "", "data": menus}, ensure_ascii=False))

class AdminMenuTopHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        menus = MenuRepository.get_top_menus()
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "data": menus}, ensure_ascii=False))

class AdminMenuAddHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        parent_id = int(self.get_body_argument("parent_id", 0))
        name = (self.get_body_argument("name", "") or "").strip()
        icon = (self.get_body_argument("icon", "") or "").strip()
        url = (self.get_body_argument("url", "") or "").strip()
        sort = int(self.get_body_argument("sort", 0))
        code = (self.get_body_argument("code", "") or "").strip()
        if not name:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "菜单名称不能为空"}, ensure_ascii=False))
        success = MenuRepository.create_menu(parent_id=parent_id, name=name, icon=icon, url=url, sort=sort, code=code)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0 if success else 1, "msg": "新增成功" if success else "新增失败"}, ensure_ascii=False))

class AdminMenuEditHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        menu_id = int(self.get_argument("id", 0))
        if not menu_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        menu = MenuRepository.get_menu_by_id(menu_id)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "data": menu if menu else {}}, ensure_ascii=False))
    
    @tornado.web.authenticated
    def post(self):
        menu_id = int(self.get_body_argument("id", 0))
        parent_id = int(self.get_body_argument("parent_id", 0))
        name = (self.get_body_argument("name", "") or "").strip()
        icon = (self.get_body_argument("icon", "") or "").strip()
        url = (self.get_body_argument("url", "") or "").strip()
        sort = int(self.get_body_argument("sort", 0))
        status = int(self.get_body_argument("status", 1))
        code = (self.get_body_argument("code", "") or "").strip()
        if not menu_id or not name:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        success = MenuRepository.update_menu(menu_id=menu_id, parent_id=parent_id, name=name, icon=icon, url=url, sort=sort, status=status, code=code)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0 if success else 1, "msg": "修改成功" if success else "修改失败"}, ensure_ascii=False))

class AdminMenuDeleteHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        menu_id = int(self.get_body_argument("id", 0))
        if not menu_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        success = MenuRepository.delete_menu(menu_id)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0 if success else 1, "msg": "删除成功" if success else "删除失败(存在子菜单)"}, ensure_ascii=False))
