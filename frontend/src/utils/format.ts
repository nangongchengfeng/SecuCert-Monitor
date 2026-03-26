export function truncate(str: string, maxLength: number = 50): string {
  if (str.length <= maxLength) return str
  return str.slice(0, maxLength) + '...'
}
