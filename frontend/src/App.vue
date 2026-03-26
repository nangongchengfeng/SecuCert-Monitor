<template>
  <div class="app-container">
    <div class="app-header">
      <h1><i class="pi pi-shield"></i> SecuCert Monitor</h1>
      <div class="nav-links">
        <router-link to="/" class="nav-link" :class="{ active: $route.path === '/' }">
          <i class="pi pi-chart-line"></i> 仪表盘
        </router-link>
        <router-link to="/certificates" class="nav-link" :class="{ active: $route.path === '/certificates' }">
          <i class="pi pi-list"></i> 证书列表
        </router-link>
      </div>
    </div>
    <div class="app-content">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style lang="scss" scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
  color: white;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

  h1 {
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &:hover {
    color: white;
    background: rgba(255, 255, 255, 0.1);
  }

  &.active {
    color: white;
    background: rgba(255, 255, 255, 0.2);
  }
}

.app-content {
  flex: 1;
  padding: 2rem;
  background: #f5f7fa;
}
</style>
