<template>
  <div class="certificate-list">
    <div class="page-header">
      <h2 class="page-title">证书列表</h2>
      <Button label="新增证书" icon="pi pi-plus" @click="showCreateDialog = true" />
    </div>

    <div class="filter-bar">
      <InputText
        v-model="searchQuery"
        placeholder="搜索证书名称..."
        class="search-input"
        @input="onSearch"
      >
        <template #prefix>
          <i class="pi pi-search"></i>
        </template>
      </InputText>
      <Select
        v-model="statusFilter"
        :options="statusOptions"
        placeholder="筛选状态"
        class="status-select"
        @change="loadCertificates"
        clearable
      />
    </div>

    <div class="table-card">
      <DataTable
        :value="certificates"
        :loading="loading"
        :paginator="true"
        :rows="perPage"
        :totalRecords="total"
        :lazy="true"
        @page="onPage"
        stripedRows
      >
        <Column field="service_name" header="证书名称" sortable>
          <template #body="slotProps">
            <div class="service-name">
              <i class="pi pi-shield"></i>
              {{ slotProps.data.service_name || '-' }}
            </div>
          </template>
        </Column>
        <Column field="type" header="类型" sortable />
        <Column field="organ" header="颁发机构" sortable />
        <Column field="expiration_date" header="过期日期" sortable>
          <template #body="slotProps">
            {{ formatDate(slotProps.data.expiration_date) }}
          </template>
        </Column>
        <Column field="day_validity" header="剩余天数" sortable>
          <template #body="slotProps">
            <StatusBadge :days="slotProps.data.day_validity" />
          </template>
        </Column>
        <Column field="use_deploy" header="使用部门" sortable />
        <Column header="操作" style="width: 150px">
          <template #body="slotProps">
            <Button
              icon="pi pi-eye"
              class="p-button-text p-button-rounded"
              @click="viewDetail(slotProps.data.id)"
            />
            <Button
              icon="pi pi-pencil"
              class="p-button-text p-button-rounded"
              @click="editCertificate(slotProps.data.id)"
            />
            <Button
              icon="pi pi-trash"
              class="p-button-text p-button-rounded p-button-danger"
              @click="confirmDelete(slotProps.data)"
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <Dialog
      v-model:visible="showDeleteDialog"
      header="确认删除"
      :modal="true"
      class="delete-dialog"
    >
      <p>确定要删除证书 "{{ deletingCertificate?.service_name }}" 吗？</p>
      <template #footer>
        <Button label="取消" icon="pi pi-times" @click="showDeleteDialog = false" />
        <Button label="删除" icon="pi pi-trash" class="p-button-danger" @click="doDelete" :loading="deleting" />
      </template>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Dialog from 'primevue/dialog'
import Toast from 'primevue/toast'
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

const onPage = (event: any) => {
  loadCertificates(event.page + 1)
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

const showCreateDialog = ref(false)

onMounted(() => {
  loadCertificates()
})
</script>

<style lang="scss" scoped>
.certificate-list {
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;

    .page-title {
      margin: 0;
      color: #1e3a5f;
    }
  }
}

.filter-bar {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;

  .search-input {
    flex: 1;
    max-width: 400px;
  }

  .status-select {
    width: 200px;
  }
}

.table-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.service-name {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #1e3a5f;
  font-weight: 500;

  i {
    color: #3b82f6;
  }
}
</style>
