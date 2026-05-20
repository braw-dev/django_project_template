import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import { getDocumentLocale } from './document'
import { DEFAULT_LOCALE, resources } from './resources'

let initialized = false

export function ensureI18n() {
  if (initialized) {
    return i18n
  }

  void i18n.use(initReactI18next).init({
    fallbackLng: DEFAULT_LOCALE,
    initAsync: false,
    interpolation: {
      escapeValue: false,
    },
    lng: getDocumentLocale(),
    resources,
    supportedLngs: Object.keys(resources),
  })
  initialized = true
  return i18n
}

export default ensureI18n()
