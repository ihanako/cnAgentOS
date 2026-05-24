# cnAgentOS - AI智能瞭望与智能问数系统

## 项目概述

cnAgentOS 是一个基于 **Tornado** 框架开发的 **B/S 架构** Web 应用系统,采用 **MVC (Model-View-Controller)** 三层架构设计。项目定位为 **AI智能瞭望与智能问数系统**,当前已实现基础的用户认证模块(登录/注册/退出),后续将在此基础上扩展 AI 相关的核心业务功能。

## 技术栈

| 类别 | 技术 | 版本/说明 |
|------|------|-----------|
| **后端语言** | Python | 3.13 |
| **Web框架** | Tornado | 6.5.5 - 异步非阻塞HTTP服务器 |
| **数据库** | SQLite3 | Python内置,轻量级关系型数据库 |
| **AI客户端** | OpenAI SDK | 2.38.0 - 兼容OpenAI API范式的AI模型调用 |
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
│   │   ├── home.py                 # 后台首页Handler
│   │   ├── admin_auth.py           # 后台认证Handler
│   │   ├── admin_home.py           # 后台主页Handler
│   │   ├── admin_user.py           # 用户管理Handler
│   │   ├── admin_role.py           # 角色管理Handler
│   │   ├── admin_menu.py           # 功能管理Handler
│   │   ├── admin_permission.py     # 权限管理Handler
│   │   └── admin_model.py          # AI模型引擎Handler
│   │
│   ├── models/                     # MVC - 模型层(数据库操作和业务逻辑)
│   │   ├── __init__.py
│   │   ├── db.py                   # 数据库连接层(建表/连接管理)
│   │   ├── user.py                 # 用户模型(用户CRUD/密码验证)
│   │   ├── user_role.py            # 用户-角色映射模型
│   │   ├── role.py                 # 角色管理模型
│   │   ├── menu.py                 # 功能菜单模型
│   │   ├── permission.py           # 权限管理模型
│   │   ├── model_config.py         # AI模型配置模型
│   │   └── ai_client.py            # OpenAI API调用封装
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
        ├── base.html               # 基础模板(页面骨架)
        ├── login.html              # 登录页模板
        ├── register.html           # 注册页模板(待实现)
        ├── index.html              # 后台首页模板
        └── admin/                  # 后台管理模板
            ├── login.html          # 后台登录页
            ├── index.html          # 后台主框架页
            ├── welcome.html        # 欢迎页
            ├── user/list.html      # 用户管理页
            ├── role/list.html      # 角色管理页
            ├── menu/list.html      # 功能管理页
            ├── permission/list.html# 权限管理页
            └── model/list.html     # AI模型引擎页
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
| RegisterHandler | GET `/auth/register` | 渲染注册页面(待实现) |

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

##### 1.2.1 AdminAuthHandler (后台认证控制器)

**文件**: [app/controllers/admin_auth.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/controllers/admin_auth.py)

| Handler | 路由 | 功能 |
|---------|------|------|
| AdminLoginHandler | GET `/admin/login` | 渲染后台登录页 |
| AdminLoginHandler | POST `/admin/login` | 验证管理员凭据,写入cookie |
| AdminLogoutHandler | POST `/admin/logout` | 清除后台cookie |

**特点**:
- 后台管理独立认证,禁用 XSRF 检查
- 默认管理员: admin/admin888
- 后台 cookie 名称: `admin_user`

##### 1.2.2 AdminHomeHandler (后台主页控制器)

**文件**: [app/controllers/admin_home.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/controllers/admin_home.py)

| Handler | 路由 | 功能 |
|---------|------|------|
| AdminIndexHandler | GET `/admin/index` | 渲染后台主框架页 |
| AdminWelcomeHandler | GET `/admin/welcome` | 渲染欢迎页(统计信息) |

**AdminBaseHandler (后台基础Handler)**:
- 继承自 `BaseHandler`
- 重写 `get_current_user()` 读取 `admin_user` cookie
- 禁用 `check_xsrf_cookie()` 后台管理已有独立认证

##### 1.3 HomeHandler (首页控制器)

**文件**: [app/controllers/home.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/controllers/home.py)

**包含的Handler**:

| Handler | 路由 | 功能 |
|---------|------|------|
| IndexHandler | GET `/` | 渲染后台首页(需登录) |

**特点**:
- 使用 `@tornado.web.authenticated` 装饰器,强制要求登录访问
- 未登录用户访问 `/` 会自动重定向到 `/auth/login`

##### 1.4 后台管理控制器 (Admin Controllers)

后台管理模块包含 6 个控制器,共 40+ 个路由:

**用户管理 - admin_user.py**:
[app/controllers/admin_user.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/controllers/admin_user.py)

| Handler | 路由 | 功能 |
|---------|------|------|
| AdminUserListHandler | GET `/admin/user/list` | 用户管理列表页 |
| AdminUserDataHandler | POST `/admin/api/user/list` | 用户数据接口(分页+搜索) |
| AdminUserAddHandler | POST `/admin/api/user/add` | 新增用户 |
| AdminUserEditHandler | POST `/admin/api/user/edit` | 编辑用户(含角色分配) |
| AdminUserDeleteHandler | POST `/admin/api/user/delete` | 删除用户 |
| AdminUserBatchDeleteHandler | POST `/admin/api/user/batch-delete` | 批量删除用户 |
| AdminUserRolesHandler | POST `/admin/api/user/roles` | 设置用户角色 |

**特点**:
- Layui 表格,20条/页分页
- admin 用户保护(不可删除/不可修改基本信息)
- 支持角色分配(多对多关系)

**角色管理 - admin_role.py**:
[app/controllers/admin_role.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/controllers/admin_role.py)

| Handler | 路由 | 功能 |
|---------|------|------|
| AdminRoleListHandler | GET `/admin/role/list` | 角色管理列表页 |
| AdminRoleDataHandler | POST `/admin/api/role/list` | 角色数据接口 |
| AdminRoleAddHandler | POST `/admin/api/role/add` | 新增角色 |
| AdminRoleEditHandler | POST `/admin/api/role/edit` | 编辑角色 |
| AdminRoleDeleteHandler | POST `/admin/api/role/delete` | 删除角色 |

**特点**:
- 系统角色保护(不可修改/删除)
- 分页+关键词搜索

**功能管理 - admin_menu.py**:
[app/controllers/admin_menu.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/controllers/admin_menu.py)

| Handler | 路由 | 功能 |
|---------|------|------|
| AdminMenuListHandler | GET `/admin/menu/list` | 功能管理列表页 |
| AdminMenuDataHandler | POST `/admin/api/menu/list` | 菜单树数据接口 |
| AdminMenuAddHandler | POST `/admin/api/menu/add` | 新增菜单 |
| AdminMenuEditHandler | POST `/admin/api/menu/edit` | 编辑菜单 |
| AdminMenuDeleteHandler | POST `/admin/api/menu/delete` | 删除菜单 |

**特点**:
- 树形表格展示(父子层级)
- 支持无限层级菜单

**权限管理 - admin_permission.py**:
[app/controllers/admin_permission.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/controllers/admin_permission.py)

| Handler | 路由 | 功能 |
|---------|------|------|
| AdminPermissionListHandler | GET `/admin/permission/list` | 权限管理列表页 |
| AdminPermissionDataHandler | POST `/admin/api/permission/list` | 权限数据接口 |
| AdminPermissionSaveHandler | POST `/admin/api/permission/save` | 保存角色-菜单映射 |

**特点**:
- 左侧角色选择+右侧功能树勾选
- 二级联动(切换角色自动刷新功能树)

**AI 模型管理 - admin_model.py**:
[app/controllers/admin_model.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/controllers/admin_model.py)

| Handler | 路由 | 功能 |
|---------|------|------|
| AdminModelListHandler | GET `/admin/model/list` | 模型引擎列表页 |
| AdminModelDataHandler | POST `/admin/api/model/list` | 模型数据接口 |
| AdminModelAddHandler | POST `/admin/api/model/add` | 新增模型 |
| AdminModelEditHandler | POST `/admin/api/model/edit` | 编辑模型 |
| AdminModelDeleteHandler | POST `/admin/api/model/delete` | 删除模型 |
| AdminModelTestHandler | POST `/admin/api/model/test` | 对话测试 |
| AdminModelSetDefaultHandler | POST `/admin/api/model/default` | 设置默认模型 |

**特点**:
- 橱窗卡片风格(3列网格布局)
- 科技感深色主题 UI
- 对话测试(弹窗+AI 思考动画)
- Token 统计可视化
- 默认模型全局优先

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

**已创建的表结构**:

##### users 表 (用户表)
```sql
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    salt TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    status INTEGER NOT NULL DEFAULT 1,
    is_admin INTEGER NOT NULL DEFAULT 0,
    create_at TEXT NOT NULL DEFAULT(datetime('now')),
    update_at TEXT NOT NULL DEFAULT(datetime('now'))
)
```

**字段说明**:
- `id`: 自增主键
- `username`: 用户名(唯一约束)
- `password_hash`: PBKDF2-HMAC-SHA256 哈希后的密码
- `salt`: 16字节随机盐值(十六进制存储)
- `email`: 邮箱地址
- `phone`: 手机号码
- `status`: 用户状态(1=正常, 0=禁用)
- `is_admin`: 是否管理员(1=是, 0=否)
- `create_at`: 创建时间(自动记录)
- `update_at`: 更新时间(自动记录)

##### roles 表 (角色表)
```sql
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    code TEXT NOT NULL UNIQUE,
    description TEXT,
    is_system INTEGER NOT NULL DEFAULT 0,
    create_at TEXT NOT NULL DEFAULT(datetime('now'))
)
```

**字段说明**:
- `id`: 自增主键
- `name`: 角色名称(唯一)
- `code`: 角色编码(唯一)
- `description`: 角色描述
- `is_system`: 是否系统角色(1=系统角色不可删除, 0=普通角色)
- `create_at`: 创建时间

##### menus 表 (功能菜单表)
```sql
CREATE TABLE IF NOT EXISTS menus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    parent_id INTEGER NOT NULL DEFAULT 0,
    icon TEXT,
    url TEXT,
    sort INTEGER NOT NULL DEFAULT 0,
    status INTEGER NOT NULL DEFAULT 1,
    create_at TEXT NOT NULL DEFAULT(datetime('now'))
)
```

**字段说明**:
- `id`: 自增主键
- `name`: 菜单名称
- `code`: 菜单编码(唯一)
- `parent_id`: 父级菜单ID(0=顶级菜单)
- `icon`: 菜单图标
- `url`: 菜单链接地址
- `sort`: 排序号
- `status`: 状态(1=启用, 0=禁用)
- `create_at`: 创建时间

##### role_menu 表 (角色-菜单关联表)
```sql
CREATE TABLE IF NOT EXISTS role_menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    menu_id INTEGER NOT NULL,
    create_at TEXT NOT NULL DEFAULT(datetime('now'))
)
```

##### user_role 表 (用户-角色关联表)
```sql
CREATE TABLE IF NOT EXISTS user_role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    create_at TEXT NOT NULL DEFAULT(datetime('now'))
)
```

##### ai_models 表 (AI模型配置表)
```sql
CREATE TABLE IF NOT EXISTS ai_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    base_url TEXT NOT NULL,
    api_key TEXT NOT NULL,
    model_name TEXT NOT NULL,
    description TEXT,
    status INTEGER NOT NULL DEFAULT 1,
    is_default INTEGER NOT NULL DEFAULT 0,
    sort INTEGER NOT NULL DEFAULT 0,
    total_tokens INTEGER NOT NULL DEFAULT 0,
    total_calls INTEGER NOT NULL DEFAULT 0,
    create_at TEXT NOT NULL DEFAULT(datetime('now')),
    update_at TEXT NOT NULL DEFAULT(datetime('now'))
)
```

**字段说明**:
- `id`: 自增主键
- `name`: 模型名称(显示名)
- `code`: 模型编码(唯一标识)
- `base_url`: API 基础地址
- `api_key`: API 密钥
- `model_name`: 模型名称(传给API)
- `description`: 模型描述
- `status`: 状态(1=启用, 0=禁用)
- `is_default`: 是否默认模型(1=是, 0=否)
- `sort`: 排序号
- `total_tokens`: 累计 Token 消耗
- `total_calls`: 累计调用次数
- `create_at/update_at`: 创建/更新时间

##### 2.2 User (用户模型)

**文件**: [app/models/user.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/models/user.py)

**UserRepository 类提供的方法**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `create_user()` | username, password, email, phone | bool | 创建新用户,用户名已存在返回False |
| `get_user_by_username()` | username | Row/None | 根据用户名查询用户记录 |
| `verify_user()` | username, password | bool | 验证用户名密码是否正确 |
| `get_user_list()` | page, page_size, keyword | dict | 分页查询用户列表(20条/页) |
| `update_user()` | user_id, data | bool | 更新用户信息 |
| `delete_user()` | user_id | bool | 删除单个用户 |
| `batch_delete_users()` | user_ids | bool | 批量删除用户 |
| `batch_update_status()` | user_ids, status | bool | 批量更新用户状态 |

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

##### 2.3 UserRole (用户-角色映射模型)

**文件**: [app/models/user_role.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/models/user_role.py)

**UserRoleRepository 类提供的方法**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `get_user_roles()` | user_id | list | 获取用户的所有角色ID |
| `set_user_roles()` | user_id, role_ids | bool | 设置用户角色(先删后增) |
| `get_users_with_roles()` | user_ids | dict | 批量获取用户角色映射 |

##### 2.4 Role (角色模型)

**文件**: [app/models/role.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/models/role.py)

**RoleRepository 类提供的方法**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `get_role_list()` | page, page_size, keyword | dict | 分页查询角色列表 |
| `create_role()` | name, code, description | int | 创建新角色 |
| `update_role()` | role_id, data | bool | 更新角色信息 |
| `delete_role()` | role_id | bool | 删除角色(系统角色不可删) |

##### 2.5 Menu (功能菜单模型)

**文件**: [app/models/menu.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/models/menu.py)

**MenuRepository 类提供的方法**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `get_menu_tree()` | status | list | 获取菜单树形结构 |
| `create_menu()` | data | int | 创建新菜单 |
| `update_menu()` | menu_id, data | bool | 更新菜单信息 |
| `delete_menu()` | menu_id | bool | 删除菜单及子菜单 |

##### 2.6 Permission (权限模型)

**文件**: [app/models/permission.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/models/permission.py)

**PermissionRepository 类提供的方法**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `get_role_menus()` | role_id | list | 获取角色的所有菜单ID |
| `set_role_menus()` | role_id, menu_ids | bool | 设置角色权限(先删后增) |

##### 2.7 ModelConfig (AI模型配置模型)

**文件**: [app/models/model_config.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/models/model_config.py)

**ModelConfigRepository 类提供的方法**:

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `get_model_list()` | page, page_size, keyword | dict | 分页查询模型列表(20条/页) |
| `create_model()` | name, code, base_url, api_key... | int | 创建新模型配置 |
| `update_model()` | model_id, data | bool | 更新模型配置 |
| `delete_model()` | model_id | bool | 删除模型配置 |
| `set_default_model()` | model_id | bool | 设置默认模型 |
| `get_default_model()` | 无 | Row/None | 获取默认模型 |
| `increment_stats()` | model_id, tokens | bool | 更新Token统计 |

##### 2.8 AIClient (AI客户端封装)

**文件**: [app/models/ai_client.py](file:///c:/Users/july2/Desktop/shixun/original/day4/day4/cnAgentOS/app/models/ai_client.py)

**核心函数**:

| 函数 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `chat_completion()` | base_url, api_key, model_name, messages | content, tokens | 同步调用OpenAI API |
| `get_openai_client()` | base_url, api_key | OpenAI | 获取OpenAI客户端实例 |

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

**前台路由**:
| 路由 | Handler | 方法 | 说明 |
|------|---------|------|------|
| `/` | IndexHandler | GET | 后台首页(需登录) |
| `/auth/login` | LoginHandler | GET/POST | 登录页/登录提交 |
| `/auth/logout` | LogoutHandler | POST | 退出登录 |

**后台管理路由** (40+ 个路由):
| 路由 | Handler | 说明 |
|------|---------|------|
| `/admin/login` | AdminLoginHandler | 后台登录页 |
| `/admin/logout` | AdminLogoutHandler | 后台退出登录 |
| `/admin/index` | AdminIndexHandler | 后台主框架页 |
| `/admin/welcome` | AdminWelcomeHandler | 欢迎页 |
| `/admin/user/list` | AdminUserListHandler | 用户管理页 |
| `/admin/api/user/list` | AdminUserDataHandler | 用户数据接口 |
| `/admin/api/user/add` | AdminUserAddHandler | 新增用户 |
| `/admin/api/user/edit` | AdminUserEditHandler | 编辑用户 |
| `/admin/api/user/delete` | AdminUserDeleteHandler | 删除用户 |
| `/admin/api/user/batch-delete` | AdminUserBatchDeleteHandler | 批量删除 |
| `/admin/api/user/roles` | AdminUserRolesHandler | 设置用户角色 |
| `/admin/role/list` | AdminRoleListHandler | 角色管理页 |
| `/admin/api/role/list` | AdminRoleDataHandler | 角色数据接口 |
| `/admin/api/role/add` | AdminRoleAddHandler | 新增角色 |
| `/admin/api/role/edit` | AdminRoleEditHandler | 编辑角色 |
| `/admin/api/role/delete` | AdminRoleDeleteHandler | 删除角色 |
| `/admin/menu/list` | AdminMenuListHandler | 功能管理页 |
| `/admin/api/menu/list` | AdminMenuDataHandler | 菜单数据接口 |
| `/admin/api/menu/add` | AdminMenuAddHandler | 新增菜单 |
| `/admin/api/menu/edit` | AdminMenuEditHandler | 编辑菜单 |
| `/admin/api/menu/delete` | AdminMenuDeleteHandler | 删除菜单 |
| `/admin/permission/list` | AdminPermissionListHandler | 权限管理页 |
| `/admin/api/permission/list` | AdminPermissionDataHandler | 权限数据接口 |
| `/admin/api/permission/save` | AdminPermissionSaveHandler | 保存权限 |
| `/admin/model/list` | AdminModelListHandler | 模型引擎页 |
| `/admin/api/model/list` | AdminModelDataHandler | 模型数据接口 |
| `/admin/api/model/add` | AdminModelAddHandler | 新增模型 |
| `/admin/api/model/edit` | AdminModelEditHandler | 编辑模型 |
| `/admin/api/model/delete` | AdminModelDeleteHandler | 删除模型 |
| `/admin/api/model/test` | AdminModelTestHandler | 对话测试 |
| `/admin/api/model/default` | AdminModelSetDefaultHandler | 设置默认模型 |

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

### 5. 后台管理系统 (2026-05-24 新增)

#### 5.1 后台认证体系
- 独立后台登录页 (`/admin/login`)
- 默认管理员: admin/admin888
- 后台独立 cookie 认证 (`admin_user`)
- 后台禁用 XSRF 检查(已有独立认证)

#### 5.2 后台主框架
- Layui 经典左侧菜单+右侧 iframe 工作区布局
- 动态菜单加载(基于菜单树)
- 顶部导航栏+底部版权信息
- 欢迎页(统计卡片+系统信息)

#### 5.3 用户管理
- Layui 表格+分页(20条/页)+关键词搜索
- 用户新增(弹窗表单+验证+重名校验)
- 用户编辑(含角色复选框分配)
- 用户删除(单条+批量)
- 用户状态管理(启用/禁用)
- **admin 用户保护**: 不可删除/不可修改基本信息(只能改密码)
- 角色列显示(标签形式)

#### 5.4 角色管理
- Layui 表格+分页+关键词搜索
- 角色新增/编辑/删除
- **系统角色保护**: 超级管理员角色不可修改/删除
- 角色编码唯一性校验

#### 5.5 功能管理
- 树形表格展示(父子层级)
- 菜单新增/编辑/删除(支持无限层级)
- 菜单图标+链接+排序
- 菜单状态管理(启用/禁用)

#### 5.6 权限管理
- 左侧角色选择+右侧功能树勾选
- 二级联动(切换角色自动刷新功能树)
- 角色-菜单多对多映射
- 一键保存角色权限

#### 5.7 AI 模型引擎管理
- **橱窗卡片风格**: 3列网格布局,科技感深色主题
- 模型新增/编辑/删除(OpenAI API 范式配置)
- **对话测试**: 弹窗+AI 思考动画+实时响应
- **Token 统计**: 调用次数+Token 消耗+进度条可视化
- **默认模型**: 全局优先调用,唯一默认标记
- 支持流式/非流式响应

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

### 4. 权限拦截

- 基于角色的访问控制(RBAC)
- 权限中间件
- 路由级权限校验

### 5. 其他待完善

- `cookie_secret` 需要更换为生产环境密钥
- 关闭 `debug` 和 `autoreload` (生产环境)
- 添加更多业务模块的 Model/Controller/View
- 完善静态资源样式
- 添加单元测试框架
- 错误处理和日志系统
- 密码找回功能(U-004)
- 数字员工模块(A-030 ~ A-034)
- 瞭望源管理(A-050 ~ A-053)
- 深度采集(A-070 ~ A-072)
- 数智大屏(A-090 ~ A-093)
- 系统统计(A-110 ~ A-113)

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

### Phase 1: AI智能问数 (优先级: 高)
- AI 问答界面 (U-010)
- 自然语言解析 (U-011)
- 问答历史记录 (U-012)

### Phase 2: 用户功能完善 (优先级: 高)
- 完善用户注册功能 (U-002)
- 密码找回功能 (U-004)
- 权限拦截 (A-023)

### Phase 3: 瞭望与采集 (优先级: 中)
- 瞭望源管理 (A-050 ~ A-053)
- 深度采集 (A-070 ~ A-072)
- 数据仓库 (A-060 ~ A-062)

### Phase 4: 数字员工 (优先级: 中)
- 数据员工 (A-030)
- 天气/新闻/音乐/电影员工 (A-031 ~ A-034)

### Phase 5: 可视化大屏 (优先级: 低)
- 数智大屏 (A-090 ~ A-093)
- 系统统计 (A-110 ~ A-113)

### Phase 6: 系统优化 (优先级: 低)
- 性能优化
- 安全加固
- 生产环境部署
