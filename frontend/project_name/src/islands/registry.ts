import type { ComponentType } from 'react'

export type ReactIslandProps = Record<string, unknown>
export type ReactIslandComponent = ComponentType<ReactIslandProps>

export const islandRegistry: Record<string, ReactIslandComponent> = {}
