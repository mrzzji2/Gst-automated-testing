const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  // Navigate to login page
  await page.goto('https://doc-online-test.gstyun.cn/webClinic/index.html#/login');
  
  // Login
  await page.fill('input[placeholder*="手机号"]', '18500629847');
  await page.fill('input[placeholder*="验证码"]', '123456');
  await page.click('button:has-text("登录")');
  
  // Wait for doctor selection dialog
  await page.waitForTimeout(2000);
  
  // Check if doctor selection dialog appears
  const hasDialog = await page.locator('dialog, .dialog').count() > 0;
  const hasRadio = await page.locator('input[type="radio"], radio').count() > 0;
  
  if (hasDialog || hasRadio) {
    // Select doctor
    const radio = page.locator('radio:has-text("罗慧")');
    if (await radio.count() > 0) {
      await radio.first.click();
    } else {
      await page.click('radio >> nth=0');
    }
    await page.waitForTimeout(500);
    await page.click('button:has-text("确认")');
  }
  
  // Wait for page load
  await page.waitForTimeout(3000);
  
  // Save storage state
  const storage = await context.storageState();
  fs.writeFileSync('d:/work/gst/tests/storage_state.json', JSON.stringify(storage, null, 2));
  
  console.log('Storage state saved successfully');
  await browser.close();
})();
