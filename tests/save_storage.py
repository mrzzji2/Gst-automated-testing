import asyncio
from playwright.async_api import async_playwright
import os

async def save_login_state():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN"
        )
        page = await context.new_page()
        
        # Navigate to login page
        await page.goto("https://doc-online-test.gstyun.cn/webClinic/index.html#/home")
        
        # Login
        await page.wait_for_selector("input[placeholder*='手机号']", timeout=10000)
        await page.fill("input[placeholder*='手机号']", "18500629847")
        await page.fill("input[placeholder*='验证码']", "123456")
        await page.click("button:has-text('登录')")
        await page.wait_for_timeout(3000)
        
        # Select doctor
        await page.wait_for_timeout(2000)
        radios = page.locator("input[type='radio'], [role='radio']")
        if await radios.count() > 0:
            doctor_radio = page.locator("radio:has-text('罗慧')")
            if await doctor_radio.count() > 0:
                await doctor_radio.first.click()
            else:
                await radios.first.click()
            await page.wait_for_timeout(500)
            await page.click("button:has-text('确认')")
            await page.wait_for_timeout(2000)
        
        # Navigate to online consultation
        await page.click("text=医生工作台")
        await page.wait_for_timeout(1000)
        
        # Save storage state
        storage_state_file = "d:/work/gst/tests/storage_state.json"
        await context.storage_state(path=storage_state_file)
        print(f"Login state saved to: {storage_state_file}")
        
        await page.wait_for_timeout(5000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(save_login_state())
