<template>
  <span :class="badgeClass">
    <i :class="iconClass" v-if="showIcon"></i>
    {{ badgeText }}
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  days?: number
  large?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  large: false
})

const showIcon = computed(() => props.large)

const badgeClass = computed(() => {
  const base = props.large ? 'status-badge-large' : 'status-badge'
  if (props.days === undefined || props.days === null) {
    return `${base} status-unknown`
  }
  if (props.days < 0) {
    return `${base} status-expired`
  }
  if (props.days < 30) {
    return `${base} status-urgent`
  }
  if (props.days < 90) {
    return `${base} status-warning`
  }
  return `${base} status-normal`
})

const iconClass = computed(() => {
  if (props.days === undefined || props.days === null) {
    return 'pi pi-question-circle'
  }
  if (props.days < 0) {
    return 'pi pi-times-circle'
  }
  if (props.days < 30) {
    return 'pi pi-exclamation-triangle'
  }
  if (props.days < 90) {
    return 'pi pi-clock'
  }
  return 'pi pi-check-circle'
})

const badgeText = computed(() => {
  if (props.days === undefined || props.days === null) {
    return '未知'
  }
  if (props.days < 0) {
    return `已过期 ${Math.abs(props.days)} 天`
  }
  return `${props.days} 天`
})
</script>

<style lang="scss" scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;

  &.status-normal {
    background: #dcfce7;
    color: #166534;
  }

  &.status-warning {
    background: #fef3c7;
    color: #92400e;
  }

  &.status-urgent {
    background: #fee2e2;
    color: #991b1b;
  }

  &.status-expired {
    background: #f3f4f6;
    color: #4b5563;
  }

  &.status-unknown {
    background: #f3f4f6;
    color: #6b7280;
  }
}

.status-badge-large {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 600;

  i {
    font-size: 1rem;
  }

  &.status-normal {
    background: #dcfce7;
    color: #166534;
  }

  &.status-warning {
    background: #fef3c7;
    color: #92400e;
  }

  &.status-urgent {
    background: #fee2e2;
    color: #991b1b;
  }

  &.status-expired {
    background: #f3f4f6;
    color: #4b5563;
  }

  &.status-unknown {
    background: #f3f4f6;
    color: #6b7280;
  }
}
</style>
