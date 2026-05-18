import { DEFAULT_LOCALE, SUPPORTED_LOCALES, type SupportedLocale } from './resources'

const supportedLocales = new Set<string>(SUPPORTED_LOCALES)

export function normalizeLocale(value: string | null | undefined): SupportedLocale {
  if (!value) {
    return DEFAULT_LOCALE
  }

  const normalizedValue = value.trim().toLowerCase().replace('_', '-')
  const [languageCode] = normalizedValue.split('-')

  if (supportedLocales.has(normalizedValue)) {
    return normalizedValue as SupportedLocale
  }

  if (languageCode && supportedLocales.has(languageCode)) {
    return languageCode as SupportedLocale
  }

  return DEFAULT_LOCALE
}

export function getDocumentLocale(): SupportedLocale {
  if (typeof document === 'undefined') {
    return DEFAULT_LOCALE
  }

  return normalizeLocale(document.documentElement.lang)
}

export function getDocumentDirection(): 'ltr' | 'rtl' {
  if (typeof document === 'undefined') {
    return 'ltr'
  }

  return document.documentElement.dir === 'rtl' ? 'rtl' : 'ltr'
}
