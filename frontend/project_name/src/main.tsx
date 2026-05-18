import { StrictMode } from 'react'
import { createRoot, type Root } from 'react-dom/client'
import { FrontendI18nProvider } from './i18n/provider'
import { islandRegistry, type ReactIslandProps } from './islands/registry'

const islandRoots = new WeakMap<HTMLElement, Root>()

function getOrCreateRoot(element: HTMLElement): Root {
  const existingRoot = islandRoots.get(element)
  if (existingRoot) {
    return existingRoot
  }

  const root = createRoot(element)
  islandRoots.set(element, root)
  return root
}

function getIslandProps(element: HTMLElement): ReactIslandProps {
  const rawProps = element.dataset.reactProps
  if (!rawProps) {
    return {}
  }

  try {
    return JSON.parse(rawProps) as ReactIslandProps
  } catch (error) {
    console.warn('Invalid data-react-props for React island', {
      element,
      error,
      rawProps,
    })
    return {}
  }
}

export function mountReactIslands() {
  const elements = document.querySelectorAll<HTMLElement>('[data-react-island]')

  for (const element of elements) {
    const islandName = element.dataset.reactIsland
    if (!islandName) {
      continue
    }

    const IslandComponent = islandRegistry[islandName]
    if (!IslandComponent) {
      console.warn(`Unknown React island: ${islandName}`)
      continue
    }

    const root = getOrCreateRoot(element)
    root.render(
      <StrictMode>
        <FrontendI18nProvider>
          <IslandComponent {...getIslandProps(element)} />
        </FrontendI18nProvider>
      </StrictMode>,
    )
  }
}

mountReactIslands()
