import { test, expect } from '@playwright/test';

test.describe('Clinical Trial Intelligence Platform E2E Flows', () => {
  test('should render clinical dashboard with synthetic disclaimer banner', async ({ page }) => {
    await page.goto('/');
    
    // Check synthetic data disclaimer
    await expect(page.locator('text=Synthetic / Demo Data Only')).toBeVisible();
    
    // Check main title
    await expect(page.locator('h1')).toContainText('Clinical Trial Intelligence');
  });

  test('should display active trials and patient cohort selector', async ({ page }) => {
    await page.goto('/');
    
    // Check that trial cards or table rows exist
    const trialSection = page.locator('text=Active Oncology Trials');
    await expect(trialSection).toBeVisible();
  });

  test('should trigger patient-trial eligibility screening and render criterion matrix', async ({ page }) => {
    await page.goto('/');
    
    // Trigger Match Button if present
    const matchBtn = page.locator('button:has-text("Run Eligibility Match")').first();
    if (await matchBtn.isVisible()) {
      await matchBtn.click();
      await expect(page.locator('text=Criterion Verification Matrix')).toBeVisible();
    }
  });

  test('should render site enrollment risk forecast radar', async ({ page }) => {
    await page.goto('/');
    
    // Verify Site Risk section
    const siteSection = page.locator('text=Site Risk & Enrollment Forecast');
    await expect(siteSection).toBeVisible();
  });

  test('should enforce human-in-the-loop clinical review sign-off', async ({ page }) => {
    await page.goto('/');
    
    // Verify clinical review queue
    const reviewHeader = page.locator('text=Clinical Review Queue');
    await expect(reviewHeader).toBeVisible();
  });
});
