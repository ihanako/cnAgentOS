import tornado.web

from app.controllers.base import BaseHandler

class AdminBaseHandler(BaseHandler):
    def get_current_user(self):
        username = self.get_secure_cookie("admin_username")
        if not username:
            return None
        return username.decode('utf-8')
    
    def check_xsrf_cookie(self):
        pass

class AdminIndexHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/index.html", title="后台管理首页", username=self.current_user)

class AdminWelcomeHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/welcome.html", title="欢迎页")
