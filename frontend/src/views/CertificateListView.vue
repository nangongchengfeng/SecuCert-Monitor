<template>
  <div class="certificate-list">
    <div class="page-header">
      <h2 class="page-title">证书列表</h2>
      <Button label="新增证书" icon="pi pi-plus" class="mac-button" @click="goToCreate" />
    </div>

    <div class="filter-bar">
      <div class="search-box">
        <i class="pi pi-search search-icon"></i>
        <input
          v-model="searchQuery"
          placeholder="搜索证书名称..."
          class="search-input"
          @input="onSearch"
        />
      </div>
      <Dropdown
        v-model="statusFilter"
        :options="statusOptions"
        placeholder="筛选状态"
        class="status-select"
        @change="loadCertificates"
        :showClear="true"
      />
    </div>

    <div class="table-card">
      <div class="table-header">
        <span class="table-count">共 {{ total }} 条证书</span>
      </div>
      <div class="table-container">
        <table class="mac-table">
          <thead>
            <tr>
              <th>证书名称</th>
              <th>类型</th>
              <th>颁发机构</th>
              <th>过期日期</th>
              <th>剩余天数</th>
              <th>使用部门</th>
              <th class="actions-col">操作</th>
            </tr>
          </thead>
          <tbody v-if="!loading">
            <tr v-for="cert in certificates" :key="cert.id" class="table-row">
              <td>
                <div class="service-name">
                  <div class="service-icon">
                    <i class="pi pi-shield"></i>
                  </div>
                  <span>{{ cert.service_name || '-' }}</span>
                </div>
              </td>
              <td>{{ cert.type }}</td>
              <td>{{ cert.organ || '-' }}</td>
              <td>{{ formatDate(cert.expiration_date) }}</td>
              <td>
                <StatusBadge :days="cert.day_validity" />
              </td>
              <td>{{ cert.use_deploy || '-' }}</td>
              <td class="actions-col">
                <button class="icon-button" @click="viewDetail(cert.id)" title="查看">
                  <i class="pi pi-eye"></i>
                </button>
                <button class="icon-button" @click="editCertificate(cert.id)" title="编辑">
                  <i class="pi pi-pencil"></i>
                </button>
                <button class="icon-button danger" @click="confirmDelete(cert)" title="删除">
                  <i class="pi pi-trash"></i>
                </button>
              </td>
            </tr>
            <tr v-if="certificates.length === 0">
              <td colspan="7" class="empty-state">
                <i class="pi pi-inbox empty-icon"></i>
                <p>暂无证书数据</p>
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td colspan="7" class="loading-state">
                <i class="pi pi-spin pi-spinner loading-icon"></i>
                <p>加载中...</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="pagination" v-if="total > perPage">
        <button
          class="page-button"
          :disabled="currentPage <= 1"
          @click="changePage(currentPage - 1)"
        >
          <i class="pi pi-chevron-left"></i>
        </button>
        <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
        <button
          class="page-button"
          :disabled="currentPage >= totalPages"
          @click="changePage(currentPage + 1)"
        >
          <i class="pi pi-chevron-right"></i>
        </button>
      </div>
    </div>

    <div class="dialog-overlay" v-if="showDeleteDialog" @click="showDeleteDialog = false">
      <div class="dialog" @click.stop>
        <div class="dialog-header">
          <i class="pi pi-exclamation-triangle dialog-icon warning"></i>
        </div>
        <div class="dialog-body">
          <h3>确认删除</h3>
          <p>确定要删除证书 "{{ deletingCertificate?.service_name }}" 吗？</p>
        </div>
        <div class="dialog-footer">
          <button class="dialog-button secondary" @click="showDeleteDialog = false">取消</button>
          <button class="dialog-button danger" @click="doDelete" :disabled="deleting">
            {{ deleting ? '删除中...' : '删除' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import Dropdown from 'primevue/dropdown'
import { useToast } from 'primevue/usetoast'
import StatusBadge from '@/components/StatusBadge.vue'
import { useCertificateStore } from '@/stores/certificate'
import { certificateApi } from '@/api/certificates'
import type { Certificate } from '@/types/certificate'

const router = useRouter()
const store = useCertificateStore()
const toast = useToast()

const certificates = ref<Certificate[]>([])
const loading = ref(false)
const total = ref(0)
const currentPage = ref(1)
const perPage = ref(20)
const searchQuery = ref('')
const statusFilter = ref<string | null>(null)
const searchTimeout = ref<number | null>(null)

const showDeleteDialog = ref(false)
const deletingCertificate = ref<Certificate | null>(null)
const deleting = ref(false)

const statusOptions = [
  { label: '已过期', value: 'expired' },
  { label: '紧急 (<30天)', value: 'urgent' },
  { label: '正常', value: 'normal' }
]

const totalPages = computed(() => Math.ceil(total.value / perPage.value))

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-'
  return dateStr.split('T')[0]
}

const loadCertificates = async (page = 1) => {
  try {
    loading.value = true
    currentPage.value = page
    const res = await certificateApi.getCertificates({
      page,
      per_page: perPage.value,
      search: searchQuery.value,
      status: statusFilter.value || undefined
    })
    certificates.value = res.data.items
    total.value = res.data.total
    store.setCertificates(res.data.items)
  } catch (error) {
    toast.add({ severity: 'error', summary: '错误', detail: '加载证书列表失败' })
  } finally {
    loading.value = false
  }
}

const onSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }
  searchTimeout.value = window.setTimeout(() => {
    loadCertificates(1)
  }, 300)
}

const changePage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    loadCertificates(page)
  }
}

const goToCreate = () => {
  router.push('/certificates/new')
}

const viewDetail = (id: number) => {
  router.push(`/certificates/${id}`)
}

const editCertificate = (id: number) => {
  router.push(`/certificates/${id}?edit=true`)
}

const confirmDelete = (cert: Certificate) => {
  deletingCertificate.value = cert
  showDeleteDialog.value = true
}

const doDelete = async () => {
  if (!deletingCertificate.value) return
  try {
    deleting.value = true
    await certificateApi.deleteCertificate(deletingCertificate.value.id)
    toast.add({ severity: 'success', summary: '成功', detail: '删除成功' })
    showDeleteDialog.value = false
    loadCertificates(currentPage.value)
  } catch (error) {
    toast.add({ severity: 'error', summary: '错误', detail: '删除失败' })
  } finally {
    deleting.value = false
  }
}

onMounted(() => {
  loadCertificates()
})
</script>

<style lang="scss" scoped>
.certificate-list {
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;

  .page-title {
    margin: 0;
    color: var(--mac-text);
    font-size: 1.5rem;
    font-weight: 700;
  }
}

.mac-button {
  background: linear-gradient(135deg, #007aff 0%, #5ac8fa 100%);
  border: none;
  color: white;
  padding: 0.6rem 1.25rem;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.4rem;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
  }

  &:active {
    transform: translateY(0);
  }
}

.filter-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  align-items: center;
}

.search-box {
  flex: 1;
  max-width: 400px;
  position: relative;
  display: flex;
  align-items: center;

  .search-icon {
    position: absolute;
    left: 1rem;
    color: var(--mac-gray);
    font-size: 0.9rem;
  }

  .search-input {
    width: 100%;
    padding: 0.75rem 1rem 0.75rem 2.75rem;
    border: 1px solid var(--mac-border);
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.9);
    font-size: 0.9rem;
    color: var(--mac-text);
    outline: none;
    transition: all 0.2s ease;

    &:focus {
      border-color: var(--mac-blue);
      box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
    }

    &::placeholder {
      color: var(--mac-gray);
    }
  }
}

.status-select {
  width: 180px;

  :deep(.p-dropdown) {
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid var(--mac-border);
    border-radius: 12px;
    padding: 0.35rem 0.75rem;
  }
}

.table-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid var(--mac-border);
  overflow: hidden;
}

.table-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--mac-border);

  .table-count {
    font-size: 0.85rem;
    color: var(--mac-gray);
    font-weight: 500;
  }
}

.table-container {
  overflow-x: auto;
}

.mac-table {
  width: 100%;
  border-collapse: collapse;

  thead {
    background: rgba(0, 122, 255, 0.03);

    th {
      padding: 0.875rem 1.5rem;
      text-align: left;
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--mac-gray);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      border-bottom: 1px solid var(--mac-border);
    }
  }

  .table-row {
    transition: all 0.2s ease;
    cursor: pointer;

    &:hover {
      background: rgba(0, 122, 255, 0.04);
    }

    td {
      padding: 1rem 1.5rem;
      font-size: 0.9rem;
      color: var(--mac-text);
      border-bottom: 1px solid var(--mac-border);
    }
  }

  .actions-col {
    text-align: right;
  }

  .empty-state,
  .loading-state {
    text-align: center;
    padding: 3rem 1.5rem;

    .empty-icon,
    .loading-icon {
      font-size: 2.5rem;
      color: var(--mac-gray);
      margin-bottom: 0.75rem;
    }

    p {
      color: var(--mac-gray);
      font-size: 0.95rem;
      margin: 0;
    }
  }
}

.service-name {
  display: flex;
  align-items: center;
  gap: 0.75rem;

  .service-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    background: linear-gradient(135deg, rgba(0, 122, 255, 0.1) 0%, rgba(90, 200, 250, 0.1) 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--mac-blue);
    font-size: 0.9rem;
    flex-shrink: 0;
  }
}

.icon-button {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: var(--mac-gray);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.25rem;

  &:hover {
    background: rgba(0, 122, 255, 0.1);
    color: var(--mac-blue);
  }

  &.danger:hover {
    background: rgba(255, 45, 85, 0.1);
    color: #ff2d55;
  }
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--mac-border);

  .page-button {
    width: 36px;
    height: 36px;
    border: 1px solid var(--mac-border);
    background: white;
    color: var(--mac-text);
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;

    &:hover:not(:disabled) {
      background: rgba(0, 122, 255, 0.05);
      border-color: var(--mac-blue);
      color: var(--mac-blue);
    }

    &:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }
  }

  .page-info {
    font-size: 0.85rem;
    color: var(--mac-gray);
    font-weight: 500;
  }
}

.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.dialog {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 1.5rem;
  width: 100%;
  max-width: 400px;
  border: 1px solid var(--mac-border);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  animation: dialogIn 0.2s ease;
}

@keyframes dialogIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.dialog-header {
  text-align: center;
  margin-bottom: 1rem;

  .dialog-icon {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;

    &.warning {
      background: rgba(255, 149, 0, 0.12);
      color: #ff9500;
    }
  }
}

.dialog-body {
  text-align: center;
  margin-bottom: 1.5rem;

  h3 {
    margin: 0 0 0.5rem 0;
    color: var(--mac-text);
    font-size: 1.1rem;
  }

  p {
    margin: 0;
    color: var(--mac-gray);
    font-size: 0.95rem;
  }
}

.dialog-footer {
  display: flex;
  gap: 0.75rem;
}

.dialog-button {
  flex: 1;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;

  &.secondary {
    background: rgba(142, 142, 147, 0.12);
    color: var(--mac-text);

    &:hover {
      background: rgba(142, 142, 147, 0.2);
    }
  }

  &.danger {
    background: linear-gradient(135deg, #ff2d55 0%, #ff6b8a 100%);
    color: white;

    &:hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(255, 45, 85, 0.3);
    }

    &:disabled {
      opacity: 0.7;
      cursor: not-allowed;
    }
  }
}
</style>
