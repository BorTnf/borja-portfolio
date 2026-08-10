export function isLinkedInUrl(url: string): boolean {
  return /linkedin\.com/i.test(url.trim());
}
