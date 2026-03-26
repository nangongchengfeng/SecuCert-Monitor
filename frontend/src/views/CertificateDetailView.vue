<template>
  <div class="certificate-detail">
    <div class="page-header">
      <button class="back-button" @click="goBack">
        <i class="pi pi-chevron-left"></i>
      </button>
      <h2 class="page-title">{{ isNew ? '新增证书' : '证书详情' }}</h2>
      <div class="header-actions">
        <template v-if="!editing && !isNew">
          <button class="action-button secondary" @click="goBack">取消</button>
          <button class="action-button primary" @click="startEdit">
            <i class="pi pi-pencil"></i> 编辑
          </button>
        </template>
        <template v-else>
          <button class="action-button secondary" @click="cancelEdit">取消</button>
          <button class="action-button primary" @click="save" :disabled="saving">
            <i class="pi pi-check" v-if="!saving"></i>
            <i class="pi pi-spin pi-spinner" v-else></i>
            {{ saving ? '保存中...' : '保存' }}
          </button>
        </template>
      </div>
    </div>

    <div class="detail-card">
      <div class="detail-header" v-if="!isNew && certificate">
        <div class="header-main">
          <div class="header-icon">
            <i class="pi pi-shield"></i>
          </div>
          <div>
            <h3>{{ certificate.service_name }}</h3>
            <p class="header-meta">{{ certificate.type }} · {{ certificate.organ || '未知颁发机构' }}</p>
          </div>
        </div>
        <StatusBadge :days="certificate.day_validity" large />
      </div>

      <div class="form-section">
        <div class="form-grid">
          <div class="form-row">
            <label class="form-label">证书名称</label>
            <input
              v-model="form.service_name"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入证书名称"
            />
          </div>
          <div class="form-row">
            <label class="form-label">类型</label>
            <input
              v-model="form.type"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入类型"
            />
          </div>
          <div class="form-row">
            <label class="form-label">颁发机构</label>
            <input
              v-model="form.organ"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入颁发机构"
            />
          </div>
          <div class="form-row">
            <label class="form-label">合同编号</label>
            <input
              v-model="form.manage_id"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入合同编号"
            />
          </div>
          <div class="form-row">
            <label class="form-label">生效日期</label>
            <input
              v-model="form.issuance_date"
              :disabled="!editing"
              type="date"
              class="form-input"
            />
          </div>
          <div class="form-row">
            <label class="form-label">过期日期</label>
            <input
              v-model="form.expiration_date"
              :disabled="!editing"
              type="date"
              class="form-input"
            />
          </div>
          <div class="form-row">
            <label class="form-label">使用部门</label>
            <input
              v-model="form.use_deploy"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入使用部门"
            />
          </div>
          <div class="form-row">
            <label class="form-label">管理部门A</label>
            <input
              v-model="form.deployA"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入管理部门A"
            />
          </div>
          <div class="form-row">
            <label class="form-label">管理部门B</label>
            <input
              v-model="form.deployB"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入管理部门B"
            />
          </div>
          <div class="form-row">
            <label class="form-label">使用产品</label>
            <input
              v-model="form.product"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入使用产品"
            />
          </div>
          <div class="form-row">
            <label class="form-label">合同经办人</label>
            <input
              v-model="form.header"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入合同经办人"
            />
          </div>
          <div class="form-row">
            <label class="form-label">技术对接人</label>
            <input
              v-model="form.tech"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入技术对接人"
            />
          </div>
          <div class="form-row">
            <label class="form-label">巡检人员</label>
            <input
              v-model="form.yumwei"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入巡检人员"
            />
          </div>
          <div class="form-row">
            <label class="form-label">巡检频率</label>
            <input
              v-model="form.yumwei_time"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入巡检频率"
            />
          </div>
          <div class="form-row">
            <label class="form-label">关联主管</label>
            <input
              v-model="form.manager"
              :disabled="!editing"
              class="form-input"
              placeholder="请输入关联主管"
            />
          </div>
          <div class="form-row full-width">
            <label class="form-label">功能场景</label>
            <textarea
              v-model="form.scene"
              :disabled="!editing"
              class="form-textarea"
              placeholder="请输入功能场景"
              rows="3"
            ></textarea>
          </div>
          <div class="form-row full-width">
            <label class="form-label">备注</label>
            <textarea
              v-model="form.remark"
              :disabled="!editing"
              class="form-textarea"
              placeholder="请输入备注"
              rows="3"
            ></textarea>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useToast } from 'primevue/usetoast'
import StatusBadge from '@/components/StatusBadge.vue'
import { certificateApi } from '@/api/certificates'
import type { Certificate, CertificateForm } from '@/types/certificate'

const router = useRouter()
const route = useRoute()
const toast = useToast()

const certificate = ref<Certificate | null>(null)
const loading = ref(false)
const saving = ref(false)
const editing = ref(false)
const originalForm = ref<CertificateForm | null>(null)

const form = ref<CertificateForm>({
  service_name: '',
  use_deploy: '',
  deployA: '',
  deployB: '',
  product: '',
  scene: '',
  organ: '',
  manage: '',
  manage_id: '',
  issuance_date: '',
  expiration_date: '',
  header: '',
  tech: '',
  yumwei: '',
  yumwei_time: '',
  manager: '',
  type: '证书',
  remark: ''
})

const formatDateForInput = (dateStr?: string) => {
  if (!dateStr) return ''
  return dateStr.split('T')[0]
}

const isNew = computed(() => !route.params.id || route.params.id === 'new')

const goBack = () => {
  router.push('/certificates')
}

const loadCertificate = async (id: number) => {
  try {
    loading.value = true
    const res = await certificateApi.getCertificate(id)
    certificate.value = res.data
    const data = { ...res.data }
    data.issuance_date = formatDateForInput(data.issuance_date)
    data.expiration_date = formatDateForInput(data.expiration_date)
    form.value = data
    originalForm.value = { ...data }
  } catch (error) {
    toast.add({ severity: 'error', summary: '错误', detail: '加载证书详情失败' })
  } finally {
    loading.value = false
  }
}

const startEdit = () => {
  editing.value = true
}

const cancelEdit = () => {
  if (isNew.value) {
    goBack()
  } else {
    editing.value = false
    if (originalForm.value) {
      form.value = { ...originalForm.value }
    }
  }
}

const save = async () => {
  try {
    saving.value = true
    if (isNew.value) {
      await certificateApi.createCertificate(form.value)
      toast.add({ severity: 'success', summary: '成功', detail: '创建成功' })
    } else {
      await certificateApi.updateCertificate(certificate.value!.id, form.value)
      toast.add({ severity: 'success', summary: '成功', detail: '保存成功' })
      editing.value = false
    }
    if (isNew.value) {
      goBack()
    } else {
      loadCertificate(certificate.value!.id)
    }
  } catch (error) {
    toast.add({ severity: 'error', summary: '错误', detail: '保存失败' })
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  const id = route.params.id
  if (id && id !== 'new') {
    loadCertificate(Number(id))
    editing.value = route.query.edit === 'true'
  } else {
    editing.value = true
  }
})
</script>

<style lang="scss" scoped>
.certificate-detail {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;

  .page-title {
    flex: 1;
    margin: 0;
    color: var(--mac-text);
    font-size: 1.5rem;
    font-weight: 700;
  }

  .header-actions {
    display: flex;
    gap: 0.75rem;
  }
}

.back-button {
  width: 36px;
  height: 36px;
  border: 1px solid var(--mac-border);
  background: rgba(255, 255, 255, 0.9);
  color: var(--mac-text);
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    background: rgba(0, 122, 255, 0.05);
    border-color: var(--mac-blue);
    color: var(--mac-blue);
  }
}

.action-button {
  padding: 0.6rem 1.25rem;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: flex;
  align-items: center;
  gap: 0.4rem;

  &.secondary {
    background: rgba(142, 142, 147, 0.12);
    color: var(--mac-text);

    &:hover {
      background: rgba(142, 142, 147, 0.2);
    }
  }

  &.primary {
    background: linear-gradient(135deg, #007aff 0%, #5ac8fa 100%);
    color: white;

    &:hover:not(:disabled) {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
    }

    &:disabled {
      opacity: 0.7;
      cursor: not-allowed;
      transform: none;
      box-shadow: none;
    }
  }
}

.detail-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid var(--mac-border);
  overflow: hidden;
}

.detail-header {
  background: linear-gradient(135deg, rgba(0, 122, 255, 0.1) 0%, rgba(90, 200, 250, 0.1) 100%);
  padding: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--mac-border);

  .header-main {
    display: flex;
    align-items: center;
    gap: 1.25rem;
  }

  .header-icon {
    width: 56px;
    height: 56px;
    border-radius: 16px;
    background: linear-gradient(135deg, #007aff 0%, #5ac8fa 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.75rem;
  }

  h3 {
    margin: 0;
    font-size: 1.35rem;
    color: var(--mac-text);
    font-weight: 700;
  }

  .header-meta {
    margin: 0.5rem 0 0 0;
    color: var(--mac-gray);
    font-size: 0.95rem;
  }
}

.form-section {
  padding: 2rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;

  .form-row {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;

    &.full-width {
      grid-column: 1 / -1;
    }
  }

  .form-label {
    font-weight: 600;
    color: var(--mac-text);
    font-size: 0.85rem;
  }

  .form-input,
  .form-textarea {
    width: 100%;
    padding: 0.75rem 1rem;
    border: 1px solid var(--mac-border);
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.9);
    font-size: 0.95rem;
    color: var(--mac-text);
    outline: none;
    transition: all 0.2s ease;
    font-family: inherit;

    &:focus:not(:disabled) {
      border-color: var(--mac-blue);
      box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
    }

    &:disabled {
      background: rgba(142, 142, 147, 0.08);
      color: var(--mac-gray);
      cursor: not-allowed;
    }

    &::placeholder {
      color: rgba(142, 142, 147, 0.5);
    }
  }

  .form-textarea {
    resize: vertical;
  }
}
</style>
