import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import CertificateListView from '@/views/CertificateListView.vue'
import CertificateDetailView from '@/views/CertificateDetailView.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: DashboardView
  },
  {
    path: '/certificates',
    name: 'CertificateList',
    component: CertificateListView
  },
  {
    path: '/certificates/new',
    name: 'CertificateCreate',
    component: CertificateDetailView
  },
  {
    path: '/certificates/:id',
    name: 'CertificateDetail',
    component: CertificateDetailView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
