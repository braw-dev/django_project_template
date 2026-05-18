import { useTranslation } from 'react-i18next'
import { getDocumentDirection } from './document'

export function useAppTranslation() {
  const translation = useTranslation()

  return {
    ...translation,
    direction: getDocumentDirection(),
    locale: translation.i18n.resolvedLanguage ?? translation.i18n.language,
  }
}
