---
name: Backend Design
description: SecuCert-Monitor 后端 API 重写设计文档
type: project
---

# Backend Design - SecuCert-Monitor

## 概述

彻底重写后端 API，使用 uv 环境管理，支持双数据库（SQLite/MySQL），统一 RESTful API 设计。

## 目录结构

```
backend/
├── .python-version          # uv Python 版本锁定
├── pyproject.toml           # uv 项目配置
├── requirements.txt         # 兼容旧方式的依赖
├── .env                     # 环境变量
├── .env.example             # 环境变量示例
├── run.py                   # 应用入口
├── app/
│   ├── __init__.py          # 工厂模式创建 app
│   ├── config.py            # 配置（双数据库支持）
│   ├── extensions.py        # Flask 扩展初始化
│   ├── models/              # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   └── certificate.py   # 证书模型
│   ├── api/                 # RESTful API
│   │   ├── __init__.py
│   │   ├── certificates.py
│   │   ├── stats.py
│   │   ├── health.py
│   │   └── schemas.py       # Pydantic 响应/请求模型
│   ├── services/            # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── certificate_service.py
│   │   └── notification_service.py
│   └── tasks/               # 定时任务
│       ├── __init__.py
│       └── scheduler.py
├── scripts/
│   ├── seed.py              # faker 假数据生成脚本
│   └── init_db.py           # 数据库初始化
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_api.py
```

## 技术栈

- **Python 3.9+**
- **uv** - 环境和依赖管理
- **Flask 2.2+** - Web 框架
- **Flask-SQLAlchemy** - ORM
- **Flask-CORS** - 跨域支持
- **APScheduler** - 定时任务
- **Pydantic** - 数据验证
- **Faker** - 假数据生成
- **pytest** - 测试框架

### 双数据库支持

- **默认**: SQLite (`sqlite:///./certificates.db`)
- **可选**: MySQL (通过 `DATABASE_URL` 环境变量切换)
- 统一的 SQLAlchemy 模型，不区分数据库

### 环境配置

`.env` 示例:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///./certificates.db
# DATABASE_URL=mysql+pymysql://user:pass@host:3306/db
```

## API 设计

### 统一响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

### API 端点

#### 证书管理

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/certificates` | 获取证书列表（支持分页、筛选、排序） |
| GET | `/api/certificates/:id` | 获取单个证书详情 |
| POST | `/api/certificates` | 创建证书 |
| PUT | `/api/certificates/:id` | 更新证书 |
| DELETE | `/api/certificates/:id` | 删除证书 |

#### 统计数据

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/stats/overview` | 概览统计（即将过期、总数等） |
| GET | `/api/stats/by-type` | 按类型统计 |
| GET | `/api/stats/expiring` | 即将过期证书列表（<30天） |

#### 健康检查

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/health` | 服务健康状态 |

## 数据模型

保持现有 `ExpirationMonitor` 模型字段不变：

- `id` - 主键
- `service_name` - 关键服务/插件/证书名称
- `use_deploy` - 使用部门
- `deployA` - 管理部门A
- `deployB` - 管理部门B
- `product` - 使用产品
- `scene` - 功能场景
- `organ` - 合作方名字
- `manage` - 管理类型
- `manage_id` - 合同编号
- `issuance_date` - 有效期开始时间
- `expiration_date` - 有效期结束时间
- `header` - 合同经办人
- `tech` - 技术对接人
- `yumwei` - 巡检人员
- `yumwei_time` - 巡检频率
- `manager` - 关联主管
- `type` - 类型
- `remark` - 备注

## 假数据生成

使用 `Faker` 库生成中文假数据：

- 生成 50-100 条证书记录
- 包含各种过期状态（已过期、即将过期、正常）
- 支持通过命令行参数控制生成数量
- 脚本位置: `scripts/seed.py`

## 开发配置

- 后端运行端口: `5000`
- 允许 CORS 来自前端 dev server (`http://localhost:5173`)
- 调试模式: `FLASK_ENV=development`
