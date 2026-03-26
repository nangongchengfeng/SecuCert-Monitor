import client from './client'
import type { Certificate, CertificateForm, CertificateListResponse, APIResponse } from '@/types/certificate'

export const certificateApi = {
  getCertificates(params?: {
    page?: number
    per_page?: number
    search?: string
    status?: string
  }): Promise<APIResponse<CertificateListResponse>> {
    return client.get('/certificates', { params }).then(res => res.data)
  },

  getCertificate(id: number): Promise<APIResponse<Certificate>> {
    return client.get(`/certificates/${id}`).then(res => res.data)
  },

  createCertificate(data: CertificateForm): Promise<APIResponse<Certificate>> {
    return client.post('/certificates', data).then(res => res.data)
  },

  updateCertificate(id: number, data: Partial<CertificateForm>): Promise<APIResponse<Certificate>> {
    return client.put(`/certificates/${id}`, data).then(res => res.data)
  },

  deleteCertificate(id: number): Promise<APIResponse> {
    return client.delete(`/certificates/${id}`).then(res => res.data)
  }
}
