<template>
  <div class="app-container">
    <div class="app-header">
      <div class="header-left">
        <div class="traffic-lights">
          <span class="light red"></span>
          <span class="light yellow"></span>
          <span class="light green"></span>
        </div>
        <h1><i class="pi pi-shield"></i> SecuCert Monitor</h1>
      </div>
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
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--mac-border);
  padding: 0 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 52px;

  .header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  h1 {
    font-size: 14px;
    font-weight: 500;
    margin: 0;
    color: var(--mac-text);
    display: flex;
    align-items: center;
    gap: 0.5rem;

    i {
      color: var(--mac-blue);
    }
  }
}

.traffic-lights {
  display: flex;
  gap: 8px;

  .light {
    width: 12px;
    height: 12px;
    border-radius: 50%;

    &.red {
      background: #ff5f57;
    }

    &.yellow {
      background: #febc2e;
    }

    &.green {
      background: #28c840;
    }
  }
}

.nav-links {
  display: flex;
  gap: 0.5rem;
}

.nav-link {
  color: var(--mac-gray);
  text-decoration: none;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 0.4rem;

  &:hover {
    color: var(--mac-text);
    background: rgba(0, 122, 255, 0.05);
  }

  &.active {
    color: var(--mac-blue);
    background: rgba(0, 122, 255, 0.1);
  }
}

.app-content {
  flex: 1;
  padding: 1.5rem;
}
</style>
