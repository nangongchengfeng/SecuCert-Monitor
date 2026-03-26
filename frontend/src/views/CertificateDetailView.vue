<template>
  <div class="certificate-detail">
    <div class="page-header">
      <Button icon="pi pi-arrow-left" class="p-button-text" @click="goBack" />
      <h2 class="page-title">{{ isNew ? '新增证书' : '证书详情' }}</h2>
    </div>

    <div class="detail-card">
      <div class="detail-header" v-if="!isNew && certificate">
        <div class="header-main">
          <i class="pi pi-shield header-icon"></i>
          <div>
            <h3>{{ certificate.service_name }}</h3>
            <p class="header-meta">{{ certificate.type }} · {{ certificate.organ }}</p>
          </div>
        </div>
        <StatusBadge :days="certificate.day_validity" large />
      </div>

      <div class="form-section">
        <div class="form-grid">
          <div class="form-row">
            <span class="form-label">证书名称</span>
            <InputText v-model="form.service_name" :disabled="!editing" placeholder="请输入证书名称" />
          </div>
          <div class="form-row">
            <span class="form-label">类型</span>
            <InputText v-model="form.type" :disabled="!editing" placeholder="请输入类型" />
          </div>
          <div class="form-row">
            <span class="form-label">颁发机构</span>
            <InputText v-model="form.organ" :disabled="!editing" placeholder="请输入颁发机构" />
          </div>
          <div class="form-row">
            <span class="form-label">合同编号</span>
            <InputText v-model="form.manage_id" :disabled="!editing" placeholder="请输入合同编号" />
          </div>
          <div class="form-row">
            <span class="form-label">生效日期</span>
            <Calendar v-model="form.issuance_date" :disabled="!editing" dateFormat="yy-mm-dd" />
          </div>
          <div class="form-row">
            <span class="form-label">过期日期</span>
            <Calendar v-model="form.expiration_date" :disabled="!editing" dateFormat="yy-mm-dd" />
          </div>
          <div class="form-row">
            <span class="form-label">使用部门</span>
            <InputText v-model="form.use_deploy" :disabled="!editing" placeholder="请输入使用部门" />
          </div>
          <div class="form-row">
            <span class="form-label">管理部门A</span>
            <InputText v-model="form.deployA" :disabled="!editing" placeholder="请输入管理部门A" />
          </div>
          <div class="form-row">
            <span class="form-label">管理部门B</span>
            <InputText v-model="form.deployB" :disabled="!editing" placeholder="请输入管理部门B" />
          </div>
          <div class="form-row">
            <span class="form-label">使用产品</span>
            <InputText v-model="form.product" :disabled="!editing" placeholder="请输入使用产品" />
          </div>
          <div class="form-row">
            <span class="form-label">合同经办人</span>
            <InputText v-model="form.header" :disabled="!editing" placeholder="请输入合同经办人" />
          </div>
          <div class="form-row">
            <span class="form-label">技术对接人</span>
            <InputText v-model="form.tech" :disabled="!editing" placeholder="请输入技术对接人" />
          </div>
          <div class="form-row">
            <span class="form-label">巡检人员</span>
            <InputText v-model="form.yumwei" :disabled="!editing" placeholder="请输入巡检人员" />
          </div>
          <div class="form-row">
            <span class="form-label">巡检频率</span>
            <InputText v-model="form.yumwei_time" :disabled="!editing" placeholder="请输入巡检频率" />
          </div>
          <div class="form-row">
            <span class="form-label">关联主管</span>
            <InputText v-model="form.manager" :disabled="!editing" placeholder="请输入关联主管" />
          </div>
          <div class="form-row full-width">
            <span class="form-label">功能场景</span>
            <Textarea v-model="form.scene" :disabled="!editing" placeholder="请输入功能场景" :rows="3" />
          </div>
          <div class="form-row full-width">
            <span class="form-label">备注</span>
            <Textarea v-model="form.remark" :disabled="!editing" placeholder="请输入备注" :rows="3" />
          </div>
        </div>

        <div class="form-actions" v-if="editing || isNew">
          <Button label="取消" @click="cancelEdit" />
          <Button label="保存" icon="pi pi-check" class="p-button-primary" @click="save" :loading="saving" />
        </div>
        <div class="form-actions" v-else>
          <Button label="编辑" icon="pi pi-pencil" class="p-button-primary" @click="startEdit" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Calendar from 'primevue/calendar'
import Toast from 'primevue/toast'
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

const isNew = computed(() => !route.params.id)

const goBack = () => {
  router.push('/certificates')
}

const loadCertificate = async (id: number) => {
  try {
    loading.value = true
    const res = await certificateApi.getCertificate(id)
    certificate.value = res.data
    form.value = { ...res.data }
    originalForm.value = { ...res.data }
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
  if (id) {
    loadCertificate(Number(id))
    editing.value = route.query.edit === 'true'
  } else {
    editing.value = true
  }
})
</script>

<style lang="scss" scoped>
.certificate-detail {
  .page-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;

    .page-title {
      margin: 0;
      color: #1e3a5f;
    }
  }
}

.detail-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.detail-header {
  background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
  color: white;
  padding: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .header-main {
    display: flex;
    align-items: center;
    gap: 1rem;
  }

  .header-icon {
    font-size: 2.5rem;
    opacity: 0.9;
  }

  h3 {
    margin: 0;
    font-size: 1.5rem;
  }

  .header-meta {
    margin: 0.5rem 0 0 0;
    opacity: 0.8;
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
    color: #374151;
    font-size: 0.875rem;
  }
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}
</style>
