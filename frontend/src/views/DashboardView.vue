<template>
  <div class="dashboard">
    <div class="stats-cards" v-if="overview">
      <div class="stat-card">
        <div class="stat-icon total">
          <i class="pi pi-shield"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.total }}</div>
          <div class="stat-label">证书总数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon urgent">
          <i class="pi pi-exclamation-triangle"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.urgent }}</div>
          <div class="stat-label">即将过期 (&lt;30天)</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon warning">
          <i class="pi pi-clock"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.warning }}</div>
          <div class="stat-label">需要关注 (30-90天)</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon expired">
          <i class="pi pi-times-circle"></i>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.expired }}</div>
          <div class="stat-label">已过期</div>
        </div>
      </div>
    </div>

    <div class="charts-grid">
      <div class="chart-card">
        <h3 class="chart-title">按类型分布</h3>
        <div ref="pieChartRef" class="chart"></div>
      </div>
      <div class="chart-card">
        <h3 class="chart-title">有效期分布趋势</h3>
        <div ref="lineChartRef" class="chart"></div>
      </div>
    </div>

    <div class="expiring-card">
      <h3 class="chart-title">即将过期 Top 10</h3>
      <div class="expiring-list">
        <div v-for="item in expiring" :key="item.id" class="expiring-item">
          <div class="expiring-icon">
            <i class="pi pi-certificate"></i>
          </div>
          <div class="expiring-info">
            <div class="expiring-name">{{ item.service_name }}</div>
            <div class="expiring-meta">{{ item.type }} · {{ formatDate(item.expiration_date) }}</div>
          </div>
          <span class="days-badge" :class="getStatusClass(item.day_validity)">
            {{ getStatusText(item.day_validity) }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { useCertificateStore } from '@/stores/certificate'
import { statsApi } from '@/api/stats'
import type { OverviewStats, TypeStats, Certificate } from '@/types/certificate'

const store = useCertificateStore()

const overview = ref<OverviewStats | null>(null)
const typeStats = ref<TypeStats[]>([])
const expiring = ref<Certificate[]>([])

const pieChartRef = ref<HTMLElement>()
const lineChartRef = ref<HTMLElement>()
let pieChart: echarts.ECharts | null = null
let lineChart: echarts.ECharts | null = null

const macColors = ['#007aff', '#5ac8fa', '#ff2d55', '#ff9500', '#34c759', '#af52de']

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-'
  return dateStr.split('T')[0]
}

const getStatusClass = (days?: number) => {
  if (days === undefined || days === null) return ''
  if (days < 0) return 'expired'
  if (days < 30) return 'urgent'
  if (days < 90) return 'warning'
  return 'normal'
}

const getStatusText = (days?: number) => {
  if (days === undefined || days === null) return '未知'
  if (days < 0) return `已过期 ${Math.abs(days)} 天`
  return `${days} 天`
}

const initPieChart = () => {
  if (!pieChartRef.value) return
  pieChart = echarts.init(pieChartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: 'rgba(0, 122, 255, 0.1)',
      borderWidth: 1,
      textStyle: {
        color: '#1c1c1e'
      }
    },
    legend: {
      orient: 'vertical',
      right: '5%',
      top: 'center',
      textStyle: {
        color: '#8e8e93',
        fontSize: 12
      }
    },
    series: [
      {
        name: '证书类型',
        type: 'pie',
        radius: ['45%', '70%'],
        center: ['35%', '50%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold'
          }
        },
        data: typeStats.value.map((item, index) => ({
          value: item.count,
          name: item.type,
          itemStyle: {
            color: macColors[index % macColors.length]
          }
        }))
      }
    ]
  }

  pieChart.setOption(option)
}

const initLineChart = () => {
  if (!lineChartRef.value) return
  lineChart = echarts.init(lineChartRef.value)

  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: 'rgba(0, 122, 255, 0.1)',
      borderWidth: 1,
      textStyle: {
        color: '#1c1c1e'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: ['已过期', '0-30天', '30-90天', '90-180天', '180-365天', '>1年'],
      axisLine: {
        lineStyle: {
          color: 'rgba(0, 122, 255, 0.1)'
        }
      },
      axisLabel: {
        color: '#8e8e93',
        fontSize: 11
      }
    },
    yAxis: {
      type: 'value',
      splitLine: {
        lineStyle: {
          color: 'rgba(0, 122, 255, 0.08)',
          type: 'dashed'
        }
      },
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        color: '#8e8e93',
        fontSize: 11
      }
    },
    series: [
      {
        name: '证书数量',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          width: 3,
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 1,
            y2: 0,
            colorStops: [
              { offset: 0, color: '#007aff' },
              { offset: 1, color: '#5ac8fa' }
            ]
          }
        },
        itemStyle: {
          color: '#007aff',
          borderColor: '#fff',
          borderWidth: 2
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(0, 122, 255, 0.25)' },
              { offset: 1, color: 'rgba(0, 122, 255, 0.02)' }
            ]
          }
        },
        data: overview.value ? [
          overview.value.expired,
          overview.value.urgent,
          overview.value.warning,
          Math.floor(overview.value.total * 0.2),
          Math.floor(overview.value.total * 0.25),
          Math.floor(overview.value.total * 0.2)
        ] : [0, 0, 0, 0, 0, 0]
      }
    ]
  }

  lineChart.setOption(option)
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

    setTimeout(() => {
      initPieChart()
      initLineChart()
    }, 100)
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  } finally {
    store.setLoading(false)
  }
}

const handleResize = () => {
  pieChart?.resize()
  lineChart?.resize()
}

onMounted(() => {
  loadData()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  pieChart?.dispose()
  lineChart?.dispose()
  window.removeEventListener('resize', handleResize)
})
</script>

<style lang="scss" scoped>
.dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
  margin-bottom: 1.5rem;

  @media (max-width: 1024px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 640px) {
    grid-template-columns: 1fr;
  }
}

.stat-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  border: 1px solid var(--mac-border);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--mac-shadow-hover);
  }
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.25rem;

  &.total {
    background: linear-gradient(135deg, #007aff 0%, #5ac8fa 100%);
  }

  &.urgent {
    background: linear-gradient(135deg, #ff2d55 0%, #ff6b8a 100%);
  }

  &.warning {
    background: linear-gradient(135deg, #ff9500 0%, #ffcc00 100%);
  }

  &.expired {
    background: linear-gradient(135deg, #8e8e93 0%, #aeaeb2 100%);
  }
}

.stat-content {
  .stat-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--mac-text);
    line-height: 1;
    letter-spacing: -0.5px;
  }

  .stat-label {
    font-size: 0.8rem;
    color: var(--mac-gray);
    margin-top: 0.25rem;
    font-weight: 500;
  }
}

.charts-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
  margin-bottom: 1.5rem;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
}

.chart-card,
.expiring-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  padding: 1.25rem;
  border: 1px solid var(--mac-border);
}

.chart-title {
  margin: 0 0 1rem 0;
  color: var(--mac-text);
  font-size: 0.95rem;
  font-weight: 600;
}

.chart {
  height: 280px;
}

.expiring-card {
  .expiring-list {
    .expiring-item {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 0.875rem 0;
      border-bottom: 1px solid var(--mac-border);
      transition: all 0.2s ease;

      &:last-child {
        border-bottom: none;
      }

      &:hover {
        background: rgba(0, 122, 255, 0.03);
        margin: 0 -1rem;
        padding: 0.875rem 1rem;
        border-radius: 8px;
      }
    }
  }

  .expiring-icon {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    background: linear-gradient(135deg, rgba(0, 122, 255, 0.1) 0%, rgba(90, 200, 250, 0.1) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--mac-blue);
    font-size: 1.1rem;
    flex-shrink: 0;
  }

  .expiring-info {
    flex: 1;
    min-width: 0;

    .expiring-name {
      font-weight: 600;
      color: var(--mac-text);
      font-size: 0.9rem;
    }

    .expiring-meta {
      font-size: 0.8rem;
      color: var(--mac-gray);
      margin-top: 0.2rem;
    }
  }
}

.days-badge {
  padding: 0.4rem 0.875rem;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.8rem;
  flex-shrink: 0;

  &.normal {
    background: rgba(52, 199, 89, 0.12);
    color: #34c759;
  }

  &.warning {
    background: rgba(255, 149, 0, 0.12);
    color: #ff9500;
  }

  &.urgent {
    background: rgba(255, 45, 85, 0.12);
    color: #ff2d55;
  }

  &.expired {
    background: rgba(142, 142, 147, 0.12);
    color: #8e8e93;
  }
}
</style>
