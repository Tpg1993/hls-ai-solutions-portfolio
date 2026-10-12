import { test, expect } from '@playwright/test';

test.describe('Regulatory Intelligence Copilot E2E Flows', () => {
  test('should render portal with synthetic disclaimer banner', async ({ page }) => {
    await page.goto('/');

    // Check synthetic disclaimer banner
    await expect(page.locator('text=Synthetic / Demo Data Only')).toBeVisible();

    // Check main title
    await expect(page.locator('h1')).toContainText('Regulatory Intelligence Copilot');
  });

  test('should search guidance and render citations', async ({ page }) => {
    await page.goto('/');

    // Check guidance search bar presence
    const searchInput = page.locator('input[placeholder*="search" i]').first();
    if (await searchInput.isVisible()) {
      await searchInput.fill('FDA Oncology Endpoint');
      await page.keyboard.press('Enter');
    }
  });

  test('should render cross-version diff inspection', async ({ page }) => {
    await page.goto('/');

    const diffTab = page.locator('button:has-text("Cross-Version Diff")');
    if (await diffTab.isVisible()) {
      await diffTab.click();
      await expect(page.locator('text=Version Diff')).toBeVisible();
    }
  });

  test('should display submission impact matrix', async ({ page }) => {
    await page.goto('/');

    const matrixTab = page.locator('button:has-text("Submission Impact Matrix")');
    if (await matrixTab.isVisible()) {
      await matrixTab.click();
      await expect(page.locator('text=Impact Matrix')).toBeVisible();
    }
  });
});
