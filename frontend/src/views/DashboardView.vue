<template>
  <div class="dashboard">
    <h2 class="page-title">仪表盘</h2>

    <div class="stats-cards" v-if="overview">
      <div class="stat-card total">
        <div class="stat-icon"><i class="pi pi-shield"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.total }}</div>
          <div class="stat-label">证书总数</div>
        </div>
      </div>
      <div class="stat-card urgent">
        <div class="stat-icon"><i class="pi pi-exclamation-triangle"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.urgent }}</div>
          <div class="stat-label">即将过期 (&lt;30天)</div>
        </div>
      </div>
      <div class="stat-card warning">
        <div class="stat-icon"><i class="pi pi-clock"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.warning }}</div>
          <div class="stat-label">需要关注 (30-90天)</div>
        </div>
      </div>
      <div class="stat-card expired">
        <div class="stat-icon"><i class="pi pi-times-circle"></i></div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.expired }}</div>
          <div class="stat-label">已过期</div>
        </div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="chart-card">
        <h3>按类型分布</h3>
        <div class="type-list">
          <div v-for="item in typeStats" :key="item.type" class="type-item">
            <span class="type-name">{{ item.type }}</span>
            <span class="type-count">{{ item.count }}</span>
          </div>
        </div>
      </div>
      <div class="chart-card">
        <h3>即将过期 Top 10</h3>
        <div class="expiring-list">
          <div v-for="item in expiring" :key="item.id" class="expiring-item">
            <div class="expiring-info">
              <div class="expiring-name">{{ item.service_name }}</div>
              <div class="expiring-meta">{{ item.type }} · {{ formatDate(item.expiration_date) }}</div>
            </div>
            <span class="days-badge urgent">{{ item.day_validity }} 天</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useCertificateStore } from '@/stores/certificate'
import { statsApi } from '@/api/stats'
import type { OverviewStats, TypeStats, Certificate } from '@/types/certificate'

const store = useCertificateStore()

const overview = ref<OverviewStats | null>(null)
const typeStats = ref<TypeStats[]>([])
const expiring = ref<Certificate[]>([])

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-'
  return dateStr.split('T')[0]
}

const loadData = async () => {
  try {
    store.setLoading(true)
    const [overviewRes, typeRes, expiringRes] = await Promise.all([
      statsApi.getOverview(),
      statsApi.getByType(),
      statsApi.getExpiring()
    ])
    overview.value = overviewRes.data
    typeStats.value = typeRes.data
    expiring.value = expiringRes.data
    store.setOverview(overviewRes.data)
    store.setTypeStats(typeRes.data)
    store.setExpiring(expiringRes.data)
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    store.setLoading(false)
  }
}

onMounted(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
.dashboard {
  .page-title {
    margin-bottom: 1.5rem;
    color: #1e3a5f;
  }
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  &.total {
    border-left: 4px solid #3b82f6;
    .stat-icon {
      background: linear-gradient(135deg, #3b82f6, #60a5fa);
    }
  }

  &.urgent {
    border-left: 4px solid #ef4444;
    .stat-icon {
      background: linear-gradient(135deg, #ef4444, #f87171);
    }
  }

  &.warning {
    border-left: 4px solid #f59e0b;
    .stat-icon {
      background: linear-gradient(135deg, #f59e0b, #fbbf24);
    }
  }

  &.expired {
    border-left: 4px solid #6b7280;
    .stat-icon {
      background: linear-gradient(135deg, #6b7280, #9ca3af);
    }
  }
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.stat-content {
  .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #1e3a5f;
    line-height: 1;
  }

  .stat-label {
    font-size: 0.875rem;
    color: #64748b;
    margin-top: 0.25rem;
  }
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
}

.chart-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  h3 {
    margin: 0 0 1rem 0;
    color: #1e3a5f;
    font-size: 1.125rem;
  }
}

.type-list {
  .type-item {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid #f3f4f6;

    &:last-child {
      border-bottom: none;
    }
  }

  .type-name {
    color: #374151;
  }

  .type-count {
    font-weight: 600;
    color: #1e3a5f;
  }
}

.expiring-list {
  .expiring-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 0;
    border-bottom: 1px solid #f3f4f6;

    &:last-child {
      border-bottom: none;
    }
  }

  .expiring-info {
    .expiring-name {
      font-weight: 500;
      color: #1e3a5f;
    }

    .expiring-meta {
      font-size: 0.875rem;
      color: #6b7280;
      margin-top: 0.25rem;
    }
  }
}

.days-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-weight: 600;
  font-size: 0.875rem;

  &.urgent {
    background: #fef2f2;
    color: #dc2626;
  }
}
</style>
