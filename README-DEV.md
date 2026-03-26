# SecuCert-Monitor - 开发指南

## 项目结构

```
SecuCert-Monitor/
├── backend/          # 后端 API (Flask)
├── frontend/         # 前端 (Vue 3)
├── docs/             # 设计文档
└── (原有文件保留)
```

## 快速开始

### 后端设置

```bash
cd backend

# 使用 uv (推荐)
uv venv
uv pip install -r requirements.txt

# 或使用 pip
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 初始化数据库
python scripts/init_db.py

# 生成假数据
python scripts/seed.py 50

# 运行服务
python run.py
```

后端 API 运行在 http://localhost:5000

### 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 开发模式
npm run dev

# 构建
npm run build
```

前端运行在 http://localhost:5173

## API 端点

### 证书管理
- `GET /api/certificates` - 获取证书列表
- `GET /api/certificates/:id` - 获取单个证书
- `POST /api/certificates` - 创建证书
- `PUT /api/certificates/:id` - 更新证书
- `DELETE /api/certificates/:id` - 删除证书

### 统计数据
- `GET /api/stats/overview` - 概览统计
- `GET /api/stats/by-type` - 按类型统计
- `GET /api/stats/expiring` - 即将过期列表

### 健康检查
- `GET /api/health` - 服务状态
