import { expect, test, type Page } from '@playwright/test'

const sessionKey = process.env.E2E_SESSION_KEY
const teamSlug = process.env.E2E_TEAM_SLUG
const baseURL = process.env.E2E_BASE_URL

async function signInWithSeededSession(page: Page) {
  if (!sessionKey || !baseURL) {
    throw new Error('E2E_SESSION_KEY and E2E_BASE_URL are required for authenticated app-shell checks')
  }

  await page.context().addCookies([
    {
      name: 'sessionid',
      value: sessionKey,
      url: baseURL,
    },
  ])
}

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

  test('authenticated app shell exposes mobile navigation and account controls', async ({ page }) => {
    test.skip(!teamSlug, 'E2E_TEAM_SLUG is required for authenticated app-shell checks')
    await signInWithSeededSession(page)
    await page.setViewportSize({ width: 390, height: 844 })

    await page.goto(`/t/${teamSlug}/dashboard`)

    const mobileNav = page.getByTestId('app-mobile-nav')
    await expect(mobileNav).toBeVisible()
    await mobileNav.locator('summary').first().click()
    await expect(mobileNav.getByTestId('team-switcher')).toBeVisible()
    await expect(page.getByTestId('account-menu')).toBeVisible()
  })

  test('server-rendered error messages use the shared toast surface', async ({ page }) => {
    await signInWithSeededSession(page)

    await page.goto('/teams/invitations/accept/invalid-token/')

    await expect(page.locator('.ui-toast-stack')).toBeVisible()
    await expect(page.locator('.ui-toast--error')).toBeVisible()
  })

  test('login form shows error summary on invalid credentials', async ({ page }) => {
    await page.goto('/accounts/login/')

    await page.locator('input[name="login"]').fill('wrong@example.com')
    await page.locator('input[name="password"]').fill('wrongpassword')
    await page.locator('form.allauth-form button[type="submit"]').first().click()

    await expect(page.getByTestId('form-error-summary')).toBeVisible()
  })
})
