import tornado.web

from app.controllers.base import BaseHandler
from app.models.user import UserRepository

class AdminLoginHandler(BaseHandler):
    def check_xsrf_cookie(self):
        pass
    
    def get(self):
        self.render("admin/login.html", title="后台管理登录", error=None)
        
    def post(self):
        username = (self.get_body_argument("username", "") or "").strip()
        password = self.get_body_argument("password", "")
        
        if not username or not password:
            self.set_status(400)
            return self.render("admin/login.html", title="后台管理登录", error="用户名或密码不能为空")
        
        if not UserRepository.verify_user(username, password):
            self.set_status(401)
            return self.render("admin/login.html", title="后台管理登录", error="用户名或密码错误")
        
        row = UserRepository.get_user_by_username(username)
        if not row or not row["is_admin"]:
            self.set_status(403)
            return self.render("admin/login.html", title="后台管理登录", error="您没有管理员权限")
        
        self.set_secure_cookie("admin_username", username)
        self.redirect("/admin")

class AdminLogoutHandler(BaseHandler):
    def post(self):
        self.clear_cookie("admin_username")
        self.redirect("/admin/login")
