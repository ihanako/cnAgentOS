import json
import tornado.web
import tornado.gen
from tornado.iostream import StreamClosedError
from app.controllers.admin_home import AdminBaseHandler
from app.models.model_config import ModelConfigRepository
from app.models.ai_client import chat_completion

class AdminModelListHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/model/list.html", title="模型引擎", username=self.current_user)

class AdminModelDataHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        page = int(self.get_argument("page", 1))
        limit = int(self.get_argument("limit", 20))
        keyword = (self.get_argument("keyword", "") or "").strip()
        result = ModelConfigRepository.get_model_list(page=page, page_size=limit, keyword=keyword)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "msg": "", "count": result["total"], "data": result["data"]}, ensure_ascii=False))

class AdminModelAddHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        name = (self.get_body_argument("name", "") or "").strip()
        code = (self.get_body_argument("code", "") or "").strip()
        base_url = (self.get_body_argument("base_url", "") or "").strip()
        api_key = (self.get_body_argument("api_key", "") or "").strip()
        model_name = (self.get_body_argument("model_name", "") or "").strip()
        description = (self.get_body_argument("description", "") or "").strip()
        status = int(self.get_body_argument("status", 1))
        is_default = int(self.get_body_argument("is_default", 0))
        sort = int(self.get_body_argument("sort", 0))
        if not all([name, code, base_url, api_key, model_name]):
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "必填项不能为空"}, ensure_ascii=False))
        success = ModelConfigRepository.create_model(name=name, code=code, base_url=base_url, api_key=api_key, model_name=model_name, description=description, status=status, is_default=is_default, sort=sort)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0 if success else 1, "msg": "新增成功" if success else "模型编码已存在"}, ensure_ascii=False))

class AdminModelEditHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        model_id = int(self.get_argument("id", 0))
        if not model_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        model = ModelConfigRepository.get_model_by_id(model_id)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0, "data": model if model else {}}, ensure_ascii=False))
    
    @tornado.web.authenticated
    def post(self):
        model_id = int(self.get_body_argument("id", 0))
        name = (self.get_body_argument("name", "") or "").strip()
        base_url = (self.get_body_argument("base_url", "") or "").strip()
        api_key = (self.get_body_argument("api_key", "") or "").strip()
        model_name = (self.get_body_argument("model_name", "") or "").strip()
        description = (self.get_body_argument("description", "") or "").strip()
        status = int(self.get_body_argument("status", 1))
        is_default = int(self.get_body_argument("is_default", 0))
        sort = int(self.get_body_argument("sort", 0))
        if not model_id or not name:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        success = ModelConfigRepository.update_model(model_id=model_id, name=name, base_url=base_url, api_key=api_key, model_name=model_name, description=description, status=status, is_default=is_default, sort=sort)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0 if success else 1, "msg": "修改成功" if success else "修改失败"}, ensure_ascii=False))

class AdminModelDeleteHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        model_id = int(self.get_body_argument("id", 0))
        if not model_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        success = ModelConfigRepository.delete_model(model_id)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0 if success else 1, "msg": "删除成功" if success else "删除失败"}, ensure_ascii=False))

class AdminModelTestHandler(AdminBaseHandler):
    @tornado.web.authenticated
    async def post(self):
        model_id = int(self.get_body_argument("model_id", 0))
        message = (self.get_body_argument("message", "") or "").strip()
        if not model_id or not message:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        
        model = ModelConfigRepository.get_model_by_id(model_id)
        if not model:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "模型不存在"}, ensure_ascii=False))
        
        try:
            content, tokens = chat_completion(
                base_url=model["base_url"],
                api_key=model["api_key"],
                model_name=model["model_name"],
                messages=[{"role": "user", "content": message}]
            )
            ModelConfigRepository.increment_stats(model_id, tokens)
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(json.dumps({"code": 0, "msg": "测试成功", "data": {"content": content, "tokens": tokens}}, ensure_ascii=False))
        except Exception as e:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            self.write(json.dumps({"code": 1, "msg": f"调用失败: {str(e)}"}, ensure_ascii=False))

class AdminModelSetDefaultHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        model_id = int(self.get_body_argument("id", 0))
        if not model_id:
            self.set_header("Content-Type", "application/json; charset=utf-8")
            return self.write(json.dumps({"code": 1, "msg": "参数错误"}, ensure_ascii=False))
        success = ModelConfigRepository.set_default_model(model_id)
        self.set_header("Content-Type", "application/json; charset=utf-8")
        self.write(json.dumps({"code": 0 if success else 1, "msg": "设置成功" if success else "设置失败"}, ensure_ascii=False))
