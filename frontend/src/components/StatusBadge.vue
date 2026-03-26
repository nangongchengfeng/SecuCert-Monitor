<template>
  <span :class="badgeClass">
    <i :class="iconClass" v-if="large"></i>
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
  gap: 0.3rem;
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.78rem;
  font-weight: 600;

  &.status-normal {
    background: rgba(52, 199, 89, 0.12);
    color: #34c759;
  }

  &.status-warning {
    background: rgba(255, 149, 0, 0.12);
    color: #ff9500;
  }

  &.status-urgent {
    background: rgba(255, 45, 85, 0.12);
    color: #ff2d55;
  }

  &.status-expired {
    background: rgba(142, 142, 147, 0.12);
    color: #8e8e93;
  }

  &.status-unknown {
    background: rgba(142, 142, 147, 0.1);
    color: #8e8e93;
  }
}

.status-badge-large {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;

  i {
    font-size: 0.95rem;
  }

  &.status-normal {
    background: rgba(52, 199, 89, 0.12);
    color: #34c759;
  }

  &.status-warning {
    background: rgba(255, 149, 0, 0.12);
    color: #ff9500;
  }

  &.status-urgent {
    background: rgba(255, 45, 85, 0.12);
    color: #ff2d55;
  }

  &.status-expired {
    background: rgba(142, 142, 147, 0.12);
    color: #8e8e93;
  }

  &.status-unknown {
    background: rgba(142, 142, 147, 0.1);
    color: #8e8e93;
  }
}
</style>
