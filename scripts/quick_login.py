"""
Quick login script - 刷新登录状态
用于快速刷新 storage_state.json 文件
"""
import asyncio
import sys
import os
from pathlib import Path
from playwright.async_api import async_playwright

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

async def quick_login():
    """快速登录并保存状态"""
    # Get credentials
    username = os.getenv("GST_USERNAME", "18500629847")
    password = os.getenv("GST_PASSWORD", "123456")
    doctor_name = os.getenv("GST_DOCTOR_NAME", "罗慧")

    storage_state_file = project_root / "tests" / "storage_state.json"

    print(f"🔐 开始登录流程...")
    print(f"📱 用户名: {username}")
    print(f"👨‍⚕️  医生: {doctor_name}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="chrome", args=["--start-maximized"])
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )

        page = await context.new_page()

        # 导航到登录页
        await page.goto("https://doc-online-test.gstyun.cn/webClinic/index.html#/home")
        await page.wait_for_timeout(2000)

        # 检查是否在登录页
        if "#/login" not in page.url:
            print("✅ 已经是登录状态")
            # 直接保存当前状态
            await context.storage_state(path=str(storage_state_file))
            print(f"💾 登录状态已保存到: {storage_state_file}")
            await browser.close()
            return

        # 执行登录
        print("📝 填写登录信息...")
        await page.fill("input[placeholder*='手机号']", username)
        await page.fill("input[placeholder*='验证码']", password)
        await page.click("button:has-text('登录')")

        print("⏳ 等待登录...")
        await page.wait_for_timeout(5000)

        # 检查医生选择对话框
        current_url = page.url
        if "#/login" in current_url:
            print("❌ 登录失败 - 仍在登录页面")
            await browser.close()
            return

        print("✅ 登录成功，等待医生选择...")
        await page.wait_for_timeout(2000)

        # 选择医生
        try:
            doctor_radio = page.locator(f"radio:has-text('{doctor_name}')")
            if await doctor_radio.count() > 0:
                await doctor_radio.first.click()
                print(f"👨‍⚕️  选择医生: {doctor_name}")
            else:
                radios = page.locator("input[type='radio'], [role='radio']")
                await radios.first.click()
                print("👨‍⚕️  选择第一个可用医生")

            await page.wait_for_timeout(500)
            await page.click("button:has-text('确认'), button:has-text('确认切换')")
            print("✅ 确认医生选择")

            await page.wait_for_timeout(3000)

        except Exception as e:
            print(f"⚠️  医生选择过程异常: {e}")

        # 保存登录状态
        print(f"💾 保存登录状态到: {storage_state_file}")
        await context.storage_state(path=str(storage_state_file))

        # 验证保存成功
        if storage_state_file.exists():
            file_size = storage_state_file.stat().st_size
            print(f"✅ 登录状态保存成功 (文件大小: {file_size} 字节)")
        else:
            print("❌ 登录状态文件未生成")

        # 询问是否保持浏览器打开
        print("\n💡 按 Ctrl+C 关闭浏览器，或保持打开进行调试...")

        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("\n👋 关闭浏览器...")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(quick_login())