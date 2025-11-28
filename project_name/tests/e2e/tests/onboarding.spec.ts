import { test, expect } from '@playwright/test'

test.describe('Marketing pages', () => {
  test('homepage renders hero content', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible()
  })
})

