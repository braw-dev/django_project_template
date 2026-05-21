import { expect, test } from '@playwright/test'

test.describe('design foundation', () => {
  test('homepage exposes skip link, theme toggle, and legal footer links', async ({ page }) => {
    await page.goto('/')

    await expect(page.locator('.ui-skip-link')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Toggle color theme' })).toBeVisible()
    await expect(page.getByRole('link', { name: 'Privacy' }).first()).toBeVisible()
    await expect(page.getByRole('link', { name: 'Terms' }).first()).toBeVisible()
    await expect(page.getByRole('link', { name: 'Cookies' }).first()).toBeVisible()
  })

  test('theme toggle updates and persists document theme', async ({ page }) => {
    await page.goto('/')

    const html = page.locator('html')
    const toggle = page.getByRole('button', { name: 'Toggle color theme' })
    const initialTheme = await html.getAttribute('data-theme')

    await toggle.click()

    const toggledTheme = await html.getAttribute('data-theme')
    expect(toggledTheme).not.toBe(initialTheme)

    await page.reload()
    await expect(html).toHaveAttribute('data-theme', toggledTheme ?? 'dark')

    const storedTheme = await page.evaluate(() => window.localStorage.getItem('theme-preference'))
    expect(storedTheme).toBe(toggledTheme)
  })

  test('login page renders auth shell brand slot', async ({ page }) => {
    await page.goto('/accounts/login/')

    await expect(page.locator('.ui-auth-panel .ui-brand')).toBeVisible()
    await expect(page.getByRole('heading', { name: 'Sign In' })).toBeVisible()
  })
})
