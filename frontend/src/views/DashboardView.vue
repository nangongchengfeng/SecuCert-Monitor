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
        <v-chart :option="pieOption" class="chart" autoresize />
      </div>
      <div class="chart-card">
        <h3>即将过期 Top 10</h3>
        <DataTable :value="expiring" stripedRows size="small" class="expiring-table">
          <Column field="service_name" header="证书名称" />
          <Column field="type" header="类型" />
          <Column field="expiration_date" header="过期日期">
            <template #body="slotProps">
              {{ formatDate(slotProps.data.expiration_date) }}
            </template>
          </Column>
          <Column field="day_validity" header="剩余天数">
            <template #body="slotProps">
              <span class="days-badge urgent">{{ slotProps.data.day_validity }} 天</span>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { use } from 'echarts/core'
import { PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import VChart from 'vue-echarts'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { useCertificateStore } from '@/stores/certificate'
import { statsApi } from '@/api/stats'
import type { OverviewStats, TypeStats, Certificate } from '@/types/certificate'

use([PieChart, TitleComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const router = useRouter()
const store = useCertificateStore()

const overview = ref<OverviewStats | null>(null)
const typeStats = ref<TypeStats[]>([])
const expiring = ref<Certificate[]>([])

const pieOption = computed(() => ({
  tooltip: {
    trigger: 'item'
  },
  legend: {
    orient: 'vertical',
    left: 'left'
  },
  series: [
    {
      name: '证书类型',
      type: 'pie',
      radius: '60%',
      data: typeStats.value.map(item => ({
        value: item.count,
        name: item.type
      })),
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
}))

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

.chart {
  height: 300px;
}

.expiring-table {
  font-size: 0.875rem;
}

.days-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-weight: 600;

  &.urgent {
    background: #fef2f2;
    color: #dc2626;
  }
}
</style>
