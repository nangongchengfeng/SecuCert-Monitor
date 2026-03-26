import client from './client'
import type { APIResponse, OverviewStats, TypeStats, Certificate } from '@/types/certificate'

export const statsApi = {
  getOverview(): Promise<APIResponse<OverviewStats>> {
    return client.get('/stats/overview').then(res => res.data)
  },

  getByType(): Promise<APIResponse<TypeStats[]>> {
    return client.get('/stats/by-type').then(res => res.data)
  },

  getExpiring(): Promise<APIResponse<Certificate[]>> {
    return client.get('/stats/expiring').then(res => res.data)
  }
}
