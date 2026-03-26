# SecuCert-Monitor

安全证书监控系统，定时巡检证书过期时间并通知管理员。

![QQ20260326-221953](images/QQ20260326-221953.png)

![QQ20260326-222008](images/QQ20260326-222008.png)

## 项目结构

```
SecuCert-Monitor/
├── backend/           # 后端 API (Flask)
│   ├── app/
│   │   ├── api/      # RESTful API
│   │   ├── models/   # 数据模型
│   │   └── services/ # 业务逻辑
│   ├── scripts/       # 脚本（初始化、假数据）
│   └── tests/
├── frontend/          # 前端 (Vue 3 + TypeScript)
│   ├── src/
│   │   ├── views/    # 页面
│   │   ├── components/ # 组件
│   │   ├── api/      # API 接口
│   │   ├── stores/   # Pinia 状态管理
│   │   └── utils/
│   └── public/
├── docs/             # 设计文档
└── sql/              # 数据库脚本
```

## 技术栈

### 后端
- Python 3.9+
- Flask 2.2+
- Flask-SQLAlchemy
- SQLite / MySQL（双数据库支持）
- uv (推荐) 或 pip
- Faker（假数据生成）

### 前端
- Vue 3 (Composition API)
- Vite 5
- TypeScript
- ECharts 5
- Pinia
- Vue Router
- Axios
- SCSS

**UI 风格：** macOS 风格（浅蓝 + 白色，毛玻璃效果）

## 快速开始

### 后端启动

```bash
cd backend

# 使用 uv (推荐)
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# 或使用 pip
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py

# 生成假数据 (50条)
python scripts/seed.py 50

# 运行服务
python run.py
```

后端 API 运行在 http://localhost:5000

### 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 开发模式（代理到后端 5000 端口）
npm run dev

# 构建
npm run build
```

前端运行在 http://localhost:5173

## 配置说明

### 后端配置

在 `backend/.env` 中配置：

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
# SQLite (默认)
DATABASE_URL=sqlite:///./certificates.db
# 或 MySQL
# DATABASE_URL=mysql+pymysql://user:password@localhost:3306/certificate
```

### 前端配置

开发环境已配置代理，`/api` 请求会转发到 `http://localhost:5000/api`

## API 端点

### 证书管理

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/certificates` | 获取证书列表（分页、筛选、搜索） |
| GET | `/api/certificates/:id` | 获取单个证书详情 |
| POST | `/api/certificates` | 创建证书 |
| PUT | `/api/certificates/:id` | 更新证书 |
| DELETE | `/api/certificates/:id` | 删除证书 |

### 统计数据

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/stats/overview` | 概览统计 |
| GET | `/api/stats/by-type` | 按类型统计 |
| GET | `/api/stats/expiring` | 即将过期列表 |

### 健康检查

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/health` | 服务健康状态 |

## 功能特性

- ✅ 双数据库支持（SQLite / MySQL）
- ✅ RESTful API 设计
- ✅ 证书 CRUD 管理
- ✅ 按状态筛选（已过期/紧急/正常）
- ✅ 可视化统计图表（ECharts）
- ✅ macOS 风格 UI
- ✅ 假数据生成脚本

## 数据模型

### ExpirationMonitor（证书表）

| 字段 | 类型 | 描述 |
|------|------|------|
| id | Integer | 主键 |
| service_name | String | 证书/服务名称 |
| use_deploy | String | 使用部门 |
| deployA | String | 管理部门A |
| deployB | String | 管理部门B |
| product | String | 使用产品 |
| scene | Text | 功能场景 |
| organ | String | 颁发机构 |
| manage | String | 管理类型 |
| manage_id | String | 合同编号 |
| issuance_date | DateTime | 生效日期 |
| expiration_date | DateTime | 过期日期 |
| header | String | 合同经办人 |
| tech | String | 技术对接人 |
| yumwei | String | 巡检人员 |
| yumwei_time | String | 巡检频率 |
| manager | String | 关联主管 |
| type | String | 类型 |
| remark | Text | 备注 |

## 开发说明

- 后端使用 Flask 工厂模式创建应用
- 前端使用 Vue 3 Composition API + `<script setup>`
- 前后端分离开发，通过代理连接
