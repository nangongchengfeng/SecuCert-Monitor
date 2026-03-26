export function formatDate(dateStr?: string): string {
  if (!dateStr) return '-'
  return dateStr.split('T')[0]
}

export function getDayValidity(expirationDateStr?: string): number | null {
  if (!expirationDateStr) return null
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  const expDate = new Date(expirationDateStr)
  expDate.setHours(0, 0, 0, 0)
  const diff = expDate.getTime() - today.getTime()
  return Math.floor(diff / (1000 * 60 * 60 * 24))
}
