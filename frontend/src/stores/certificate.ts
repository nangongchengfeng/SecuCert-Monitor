import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Certificate, OverviewStats, TypeStats } from '@/types/certificate'

export const useCertificateStore = defineStore('certificate', () => {
  const certificates = ref<Certificate[]>([])
  const overview = ref<OverviewStats | null>(null)
  const typeStats = ref<TypeStats[]>([])
  const expiring = ref<Certificate[]>([])
  const loading = ref(false)

  const setCertificates = (data: Certificate[]) => {
    certificates.value = data
  }

  const setOverview = (data: OverviewStats) => {
    overview.value = data
  }

  const setTypeStats = (data: TypeStats[]) => {
    typeStats.value = data
  }

  const setExpiring = (data: Certificate[]) => {
    expiring.value = data
  }

  const setLoading = (state: boolean) => {
    loading.value = state
  }

  return {
    certificates,
    overview,
    typeStats,
    expiring,
    loading,
    setCertificates,
    setOverview,
    setTypeStats,
    setExpiring,
    setLoading
  }
})
