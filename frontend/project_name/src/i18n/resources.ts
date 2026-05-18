import de from './locales/de.json'
import en from './locales/en.json'
import es from './locales/es.json'
import fr from './locales/fr.json'
import pt from './locales/pt.json'

export const DEFAULT_LOCALE = 'en'

export const resources = {
  de: { translation: de },
  en: { translation: en },
  es: { translation: es },
  fr: { translation: fr },
  pt: { translation: pt },
} as const

export type SupportedLocale = keyof typeof resources

export const SUPPORTED_LOCALES = Object.keys(resources) as SupportedLocale[]
