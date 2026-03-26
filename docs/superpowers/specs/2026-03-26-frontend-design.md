---
name: Frontend Design
description: SecuCert-Monitor 前端重写设计文档
type: project
---

# Frontend Design - SecuCert-Monitor

## 概述

使用 Vue 3 + Vite + TypeScript + PrimeVue + ECharts + SCSS 完全重写前端。

## 目录结构（按文件类型组织）

```
frontend/
├── package.json
├── vite.config.ts
├── tsconfig.json
├── .env.development
├── .env.production
├── index.html
├── src/
│   ├── main.ts                # 应用入口
│   ├── App.vue                # 根组件
│   ├── env.d.ts
│   ├── assets/                # 静态资源
│   │   └── styles/
│   │       ├── main.scss      # 全局样式
│   │       └── variables.scss # SCSS 变量
│   ├── components/            # 可复用组件
│   │   ├── CertificateTable.vue
│   │   ├── CertificateCard.vue
│   │   └── StatusBadge.vue
│   ├── views/                 # 页面组件
│   │   ├── DashboardView.vue
│   │   ├── CertificateListView.vue
│   │   └── CertificateDetailView.vue
│   ├── api/                   # API 接口
│   │   ├── client.ts          # axios 实例配置
│   │   ├── certificates.ts
│   │   └── stats.ts
│   ├── stores/                # Pinia 状态管理
│   │   └── certificate.ts
│   ├── types/                 # TypeScript 类型定义
│   │   └── certificate.ts
│   ├── utils/                 # 工具函数
│   │   ├── date.ts
│   │   └── format.ts
│   └── router/                # 路由配置
│       └── index.ts
└── public/
    └── favicon.ico
```

## 技术栈

- **Vue 3** - Composition API + `<script setup>`
- **Vite** - 构建工具
- **TypeScript** - 类型安全
- **PrimeVue** - UI 组件库（Aura 主题）
- **PrimeIcons** - 图标库
- **ECharts** - 图表库 + vue-echarts
- **Pinia** - 状态管理
- **Vue Router** - 路由
- **Axios** - HTTP 客户端
- **SCSS** - CSS 预处理器

## 页面/功能设计

### 路由配置

| 路径 | 组件 | 描述 |
|------|------|------|
| `/` | `DashboardView` | 仪表盘 |
| `/certificates` | `CertificateListView` | 证书列表 |
| `/certificates/:id` | `CertificateDetailView` | 证书详情/编辑 |

### 1. 仪表盘 (Dashboard)

功能：
- 概览统计卡片
  - 证书总数
  - 即将过期（<30天）
  - 已过期
- ECharts 图表
  - 过期趋势图（折线图）
  - 按类型分布图（饼图）
- 即将过期证书 Top 10 列表

### 2. 证书列表

功能：
- PrimeVue DataTable 展示
- 支持筛选、排序、搜索
- 状态标签（不同颜色）
  - 绿色：正常（>90天）
  - 橙色：即将过期（30-90天）
  - 红色：紧急（<30天）
  - 灰色：已过期
- 批量操作
- 分页

### 3. 证书详情/编辑

功能：
- 表单查看/编辑证书信息
- 有效期倒计时显示
- 保存/取消操作

## 开发配置

- 前端 Vite dev server 端口: `5173`
- API 代理: `/api` → `http://localhost:5000/api`
- 环境变量:
  - `VITE_API_BASE_URL` - API 基础地址

### PrimeVue 配置

- 主题: Aura
- 组件按需引入
