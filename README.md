# cnAgentOS - AI智能瞭望与智能问数系统

## 项目概述

cnAgentOS 是一个基于 **Tornado** 框架开发的 **B/S 架构** Web 应用系统,采用 **MVC (Model-View-Controller)** 三层架构设计。项目定位为 **AI智能瞭望与智能问数系统**,当前已实现基础的用户认证模块(登录/注册/退出),后续将在此基础上扩展 AI 相关的核心业务功能。

## 技术栈

| 类别 | 技术 | 版本/说明 |
|------|------|-----------|
| **后端语言** | Python | 3.13 |
| **Web框架** | Tornado | 6.5.5 - 异步非阻塞HTTP服务器 |
| **数据库** | SQLite3 | Python内置,轻量级关系型数据库 |
| **前端** | HTML5 | 页面结构 |
| **样式** | CSS | 页面样式 |
| **脚本** | JavaScript | 客户端交互逻辑 |
| **模板引擎** | Tornado Template | 服务端模板渲染 |
| **UI组件库** | Layui | 2.13.6 - 经典模块化前端UI组件库(本地化) |
| **响应式框架** | Bootstrap | 5.3.8 - 响应式移动优先前端框架(本地化) |
| **图标库** | FontAwesome | 5.15.4 - 矢量图标集(本地化) |

## 项目目录结构

```
cnAgentOS/
├── app.md                          # 项目目录结构说明文档
├── app.py                          # 程序主入口(服务器容器+应用配置)
├── test.py                         # 单元测试/临时测试脚本
├── README.md                       # 项目说明文档(本文件)
│
├── app/                            # 应用核心代码目录
│   ├── __init__.py                 # Python包初始化文件
│   │
│   ├── controllers/                # MVC - 控制层(处理HTTP请求和业务流转)
│   │   ├── __init__.py
│   │   ├── base.py                 # 基础Handler类(统一登录态处理)
│   │   ├── auth.py                 # 认证相关Handler(登录/注册/退出)
│   │   └── home.py                 # 后台首页Handler
│   │
│   ├── models/                     # MVC - 模型层(数据库操作和业务逻辑)
│   │   ├── __init__.py
│   │   ├── db.py                   # 数据库连接层(建表/连接管理)
│   │   └── user.py                 # 用户模型(用户CRUD/密码验证)
│   │
│   ├── static/                     # MVC - 视图层静态资源
│   │   ├── css/
│   │   │   └── base.css            # 全局样式文件
│   │   ├── js/
│   │   │   └── base.js             # 全局JavaScript文件
│   │   ├── layui-v2.13.6/          # Layui UI组件库(本地化)
│   │   ├── bootstrap-5.3.8-dist/   # Bootstrap响应式框架(本地化)
│   │   └── fontawesome-free-5.15.4-web/  # FontAwesome图标库(本地化)
│   │
│   └── templates/                  # MVC - 视图层HTML模板
│       ├── base.html               # 基础模板(页面骨架)
│       ├── login.html              # 登录页模板
│       ├── register.html           # 注册页模板(待实现)
│       └── index.html              # 后台首页模板
│
├── database/                       # SQLite数据库文件目录
│   └── app.db                      # 自动创建的SQLite数据库文件
│
└── venv/                           # Python虚拟环境(python -m venv venv)
```

## 架构设计详解

### MVC 架构分层

#### 1. Controller 层 (控制层)

位于 `app/controllers/` 目录,负责接收HTTP请求、处理业务逻辑流转、调用Model层、渲染View层或跳转。

##### 1.1 BaseHandler (基础控制器)

**文件**: [app/controllers/base.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/controllers/base.py)

**作用**: 所有Controller的公共基类,提供统一的登录态认证机制。

**核心功能**:
```python
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        # 从secure cookie中读取username
        # 返回用户名字符串或None
        # 配合@tornado.web.authenticated装饰器使用
```

**工作机制**:
- Tornado框架通过 `get_current_user()` 的返回值判断用户是否已登录
- 返回 `None` 时, `@tornado.web.authenticated` 装饰器会自动重定向到 `login_url` 配置的路由
- 返回有效值时,可以通过 `self.current_user` 属性获取当前登录用户名

##### 1.2 AuthHandler (认证控制器)

**文件**: [app/controllers/auth.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/controllers/auth.py)

**包含的Handler**:

| Handler | 路由 | 功能 |
|---------|------|------|
| LoginHandler | GET `/auth/login` | 渲染登录页面 |
| LoginHandler | POST `/auth/login` | 验证用户名密码,写入cookie并跳转 |
| LogoutHandler | POST `/auth/logout` | 清除cookie并跳转到登录页 |

**LoginHandler 处理流程**:
1. **GET请求**: 渲染 `login.html` 模板,显示登录表单
2. **POST请求**:
   - 接收表单参数 `username` 和 `password`
   - 校验参数非空
   - 调用 `UserRepository.verify_user()` 验证凭据
   - 验证成功后通过 `self.set_secure_cookie()` 写入加密cookie
   - 重定向到首页 `/`

**安全特性**:
- 使用 Tornado 的 `set_secure_cookie()` 加密存储用户会话
- 启用 XSRF/CSRF 防护 (`xsrf_cookies=True`)
- 表单提交包含 `{% module xsrf_form_html() %}` 令牌

##### 1.3 HomeHandler (首页控制器)

**文件**: [app/controllers/home.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/controllers/home.py)

**包含的Handler**:

| Handler | 路由 | 功能 |
|---------|------|------|
| IndexHandler | GET `/` | 渲染后台首页(需登录) |

**特点**:
- 使用 `@tornado.web.authenticated` 装饰器,强制要求登录访问
- 未登录用户访问 `/` 会自动重定向到 `/auth/login`

#### 2. Model 层 (模型层)

位于 `app/models/` 目录,负责数据库操作、数据模型定义和业务逻辑封装。

##### 2.1 Database (数据库连接层)

**文件**: [app/models/db.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/models/db.py)

**核心功能**:

| 函数 | 说明 |
|------|------|
| `_project_root()` | 获取项目根目录路径 |
| `get_connection()` | 获取SQLite数据库连接,设置 `row_factory=sqlite3.Row` 支持字典式访问 |
| `init_db()` | 初始化数据库表(使用 `CREATE TABLE IF NOT EXISTS`) |

**数据库路径**: `database/app.db` (相对于项目根目录)

**已创建的表结构 - users**:
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    create_at TEXT NOT NULL DEFAULT(datetime('now'))
)
```

**字段说明**:
- `id`: 自增主键
- `username`: 用户名(唯一约束)
- `password_hash`: PBKDF2-HMAC-SHA256 哈希后的密码
- `salt`: 16字节随机盐值(十六进制存储)
- `create_at`: 创建时间(自动记录)

##### 2.2 User (用户模型)

**文件**: [app/models/user.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/models/user.py)

**UserRepository 类提供的方法**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `create_user()` | username, password | bool | 创建新用户,用户名已存在返回False |
| `get_user_by_username()` | username | Row/None | 根据用户名查询用户记录 |
| `verify_user()` | username, password | bool | 验证用户名密码是否正确 |

**密码安全机制**:
```python
def _hash_password(password: str, salt: bytes) -> str:
    # 使用 PBKDF2-HMAC-SHA256 算法
    # 迭代次数: 100,000次
    # 输出: 十六进制字符串
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return dk.hex()
```

**安全特性**:
- 使用 `secrets.token_bytes(16)` 生成加密安全的随机盐值
- PBKDF2 密钥派生函数,抗暴力破解
- 每个用户独立盐值,防御彩虹表攻击

#### 3. View 层 (视图层)

位于 `app/templates/` 和 `app/static/` 目录,负责页面展示和用户交互。

##### 3.1 模板文件

**基础模板 - base.html**:
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="{{static_url('css/base.css')}}">
    <script src="{{static_url('js/base.js')}}"></script>
</head>
<body>
    <div class="container">
        {% block body %} {% end %}
    </div>
</body>
</html>
```

**特点**:
- 使用 Tornado 模板语法 `{{ }}` 输出变量
- `{% block body %}` 定义内容块,子模板通过 `{% extends %}` 继承
- `{{static_url()}}` 自动生成带版本号的静态文件URL

**登录页 - login.html**:
- 继承 `base.html`
- 显示错误信息 `{% if error %}`
- 包含 XSRF 令牌 `{% module xsrf_form_html() %}`

**后台首页 - index.html**:
- 继承 `base.html`
- 显示当前登录用户名 `{{username}}`
- 包含退出登录表单

##### 3.2 静态资源

**CSS - base.css**:
- 全局重置样式
- 错误信息样式 `.error { color: red; }`

**JavaScript - base.js**:
- 基础JavaScript文件(当前仅包含日志输出)

### 应用入口与配置

**文件**: [app.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app.py)

#### 路由配置

| 路由 | Handler | 方法 | 说明 |
|------|---------|------|------|
| `/` | IndexHandler | GET | 后台首页(需登录) |
| `/auth/login` | LoginHandler | GET/POST | 登录页/登录提交 |
| `/auth/logout` | LogoutHandler | POST | 退出登录 |

#### 应用配置 (settings)

```python
settings = dict(
    template_path=".../app/templates",     # 模板文件路径
    static_path=".../app/static",          # 静态文件路径
    cookie_secret="demo-cookie-secret-change-me",  # cookie加密密钥(需更换)
    login_url="/auth/login",               # 未登录重定向地址
    xsrf_cookies=True,                     # 启用XSRF防护
    debug=True,                            # 调试模式
    autoreload=True                        # 代码变更自动重启
)
```

#### 服务器配置

```python
server = HTTPServer(app)
server.bind(10086)      # 绑定端口 10086
server.start()          # 自动根据CPU核心数启动进程
```

**访问地址**: `http://localhost:10086`

## 已实现功能

### 1. 用户登录功能

**完整流程**:
1. 用户访问 `http://localhost:10086`
2. 未登录自动跳转到 `/auth/login`
3. 输入用户名和密码
4. 后端验证:
   - 参数非空校验
   - 数据库查询用户
   - PBKDF2密码哈希比对
5. 验证成功:
   - 写入加密cookie (`set_secure_cookie`)
   - 重定向到首页 `/`
6. 验证失败:
   - 显示错误信息
   - 停留在登录页

**测试验证**:
```python
# test.py 测试脚本
UserRepository.get_user_by_username("admin")     # 查询用户
UserRepository.verify_user("admin", "123456")    # 验证密码(成功)
UserRepository.verify_user("admin", "1234567")   # 验证密码(失败)
```

### 2. 会话管理

- 使用 Tornado `secure_cookie` 存储用户会话
- cookie通过 `cookie_secret` 加密签名
- 退出登录时清除cookie

### 3. 安全防护

- **XSRF/CSRF防护**: 启用 `xsrf_cookies=True`,表单包含XSRF令牌
- **密码加密**: PBKDF2-HMAC-SHA256 + 随机盐值
- **认证拦截**: `@tornado.web.authenticated` 装饰器保护需要登录的页面

### 4. 数据库自动初始化

- 启动服务前自动调用 `init_db()`
- 使用 `CREATE TABLE IF NOT EXISTS` 确保表存在
- 自动创建 `database/` 目录

## 待实现功能

### 1. 用户注册功能

- **状态**: Controller 路由未注册,模板文件 `register.html` 为空
- **已有准备**: `UserRepository.create_user()` 方法已实现
- **需要开发**:
  - 创建 `RegisterHandler` (GET渲染注册页, POST处理注册)
  - 注册路由 `/auth/register`
  - 完善 `register.html` 模板
  - 添加注册表单验证(用户名格式、密码强度等)

### 2. AI智能瞭望功能

- 实时监控/数据展示功能
- 数据可视化看板
- 异常告警机制

### 3. 智能问数功能

- 自然语言查询接口
- AI数据分析
- 结果可视化展示

### 4. 其他待完善

- `cookie_secret` 需要更换为生产环境密钥
- 关闭 `debug` 和 `autoreload` (生产环境)
- 添加更多业务模块的 Model/Controller/View
- 完善静态资源样式
- 添加单元测试框架
- 错误处理和日志系统

## 开发指南

### 环境准备

```powershell
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
venv\Scripts\activate

# 3. 安装依赖
pip install tornado==6.5.5
```

### 启动服务

```powershell
# 在项目根目录下执行
python app.py
```

服务启动后访问: `http://localhost:10086`

### 添加新模块的步骤

#### 1. 添加新的 Model

在 `app/models/` 下创建新的模型文件:

```python
# app/models/xxx.py
from app.models.db import get_connection

class XxxRepository:
    @staticmethod
    def create(data):
        with get_connection() as conn:
            conn.execute("INSERT INTO xxx ...", data)
    
    @staticmethod
    def get_by_id(id):
        with get_connection() as conn:
            return conn.execute("SELECT ... WHERE id=?", (id,)).fetchone()
```

#### 2. 添加新的 Controller

在 `app/controllers/` 下创建新的控制器:

```python
# app/controllers/xxx.py
from app.controllers.base import BaseHandler

class XxxHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("xxx.html", title="XXX页面")
    
    def post(self):
        # 处理表单提交
        pass
```

#### 3. 添加新的 View

在 `app/templates/` 下创建模板:

```html
{% extends "base.html" %}
{% block body %}
<h3>XXX页面</h3>
<!-- 页面内容 -->
{% end %}
```

#### 4. 注册路由

在 `app.py` 的 `make_app()` 函数中添加路由:

```python
return tornado.web.Application([
    (r"/", IndexHandler),
    (r"/auth/login", LoginHandler),
    (r"/auth/logout", LogoutHandler),
    (r"/xxx", XxxHandler),      # 新增路由
], **settings)
```

#### 5. 添加数据库表 (如需要)

在 `app/models/db.py` 的 `init_db()` 中添加建表SQL:

```python
def init_db():
    with get_connection() as conn:
        # 现有users表
        conn.execute('''CREATE TABLE IF NOT EXISTS users(...)''')
        
        # 新增表
        conn.execute('''CREATE TABLE IF NOT EXISTS new_table(...)''')
```

### Tornado 框架核心概念

#### RequestHandler 生命周期

1. 收到HTTP请求
2. 调用 `prepare()` (可选)
3. 根据HTTP方法调用对应方法 (`get()`, `post()`, `put()`, `delete()`)
4. 渲染模板或返回数据
5. 调用 `on_finish()` (可选)

#### 常用API

| API | 说明 |
|-----|------|
| `self.get_argument(name, default)` | 获取GET/POST参数 |
| `self.get_body_argument(name, default)` | 仅获取POST参数 |
| `self.render(template_name, **kwargs)` | 渲染模板 |
| `self.write(data)` | 直接输出数据 |
| `self.redirect(url)` | 重定向 |
| `self.set_secure_cookie(name, value)` | 设置加密cookie |
| `self.get_secure_cookie(name)` | 获取加密cookie |
| `self.clear_cookie(name)` | 清除cookie |
| `self.set_status(code)` | 设置HTTP状态码 |
| `self.xsrf_form_html()` | 生成XSRF令牌HTML |

#### Tornado 模板语法

```html
<!-- 输出变量 -->
{{ variable }}

<!-- 条件判断 -->
{% if condition %}
    ...
{% end %}

<!-- 循环 -->
{% for item in items %}
    {{ item }}
{% end %}

<!-- 继承模板 -->
{% extends "base.html" %}

<!-- 定义内容块 -->
{% block body %}
    内容
{% end %}

<!-- 包含模块 -->
{% module xsrf_form_html() %}

<!-- 静态URL -->
{{ static_url('css/style.css') }}
```

## 测试说明

**测试文件**: [test.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/test.py)

运行测试:
```powershell
python test.py
```

当前测试内容:
- 数据库初始化
- 用户查询功能
- 密码验证功能

## 注意事项

1. **cookie_secret**: 当前使用示例密钥 `demo-cookie-secret-change-me`,生产环境必须更换
2. **调试模式**: `debug=True` 和 `autoreload=True` 仅用于开发,生产环境需关闭
3. **端口配置**: 服务默认运行在 `10086` 端口,可在 `app.py` 中修改
4. **数据库备份**: SQLite数据库文件位于 `database/app.db`,注意定期备份
5. **虚拟环境**: 所有操作应在 `venv` 虚拟环境中进行

## 后续开发计划

基于当前架构,后续将开发以下核心功能:

1. **AI智能瞭望模块**
   - 数据源接入
   - 实时监控面板
   - 数据可视化图表
   - 异常检测与告警

2. **智能问数模块**
   - 自然语言处理接口
   - AI查询引擎
   - 结果展示与导出

3. **用户管理增强**
   - 完善注册功能
   - 用户权限管理
   - 密码重置

4. **系统优化**
   - 性能优化
   - 日志系统
   - 错误处理
   - 生产环境配置
