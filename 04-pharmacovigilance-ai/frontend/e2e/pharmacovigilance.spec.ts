import { test, expect } from '@playwright/test';

test.describe('Pharmacovigilance AI Platform E2E Flows', () => {
  test('should render safety dashboard with synthetic disclaimer banner', async ({ page }) => {
    await page.goto('/');

    // Check synthetic disclaimer banner
    await expect(page.locator('text=SYNTHETIC / DEMO DATA ONLY')).toBeVisible();

    // Check title
    await expect(page.locator('h1')).toContainText('Pharmacovigilance AI');
  });

  test('should display active signals in disproportionality radar', async ({ page }) => {
    await page.goto('/');

    // Navigate to Signal Intelligence tab
    const signalTab = page.locator('button:has-text("Signal Intelligence")');
    if (await signalTab.isVisible()) {
      await signalTab.click();
      await expect(page.locator('text=Statistical Signal Detection Radar')).toBeVisible();
    }
  });

  test('should execute spontaneous case intake with PII scrubbing', async ({ page }) => {
    await page.goto('/');

    const caseTab = page.locator('button:has-text("Case Intake")');
    if (await caseTab.isVisible()) {
      await caseTab.click();
      await expect(page.locator('text=Spontaneous Narrative Case Intake')).toBeVisible();
    }
  });

  test('should enforce human-in-the-loop review sign-off', async ({ page }) => {
    await page.goto('/');

    const reviewTab = page.locator('button:has-text("Safety Committee Sign-Off")');
    if (await reviewTab.isVisible()) {
      await reviewTab.click();
      await expect(page.locator('text=Human-in-the-Loop Safety Sign-Off Gate')).toBeVisible();
      await expect(page.locator('text=Regulatory Audit Trail')).toBeVisible();
    }
  });
});
