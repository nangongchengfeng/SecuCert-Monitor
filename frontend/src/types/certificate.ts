export interface Certificate {
  id: number
  service_name?: string
  use_deploy?: string
  deployA?: string
  deployB?: string
  product?: string
  scene?: string
  organ?: string
  manage?: string
  manage_id?: string
  issuance_date?: string
  expiration_date?: string
  header?: string
  tech?: string
  yumwei?: string
  yumwei_time?: string
  manager?: string
  type: string
  remark?: string
  day_validity?: number
}

export interface CertificateForm {
  service_name?: string
  use_deploy?: string
  deployA?: string
  deployB?: string
  product?: string
  scene?: string
  organ?: string
  manage?: string
  manage_id?: string
  issuance_date?: string
  expiration_date?: string
  header?: string
  tech?: string
  yumwei?: string
  yumwei_time?: string
  manager?: string
  type: string
  remark?: string
}

export interface APIResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface CertificateListResponse {
  items: Certificate[]
  total: number
  page: number
  per_page: number
  pages: number
}

export interface OverviewStats {
  total: number
  expired: number
  urgent: number
  warning: number
  normal: number
}

export interface TypeStats {
  type: string
  count: number
}
