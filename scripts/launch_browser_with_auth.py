"""
Launch browser with saved authentication state
用于手动调试时启动已登录的浏览器
"""
import asyncio
import sys
from pathlib import Path
from playwright.async_api import async_playwright

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

async def launch_browser():
    """启动带登录状态的浏览器（保持打开）"""
    storage_state_file = project_root / "tests" / "storage_state.json"

    if not storage_state_file.exists():
        print(f"❌ 登录状态文件不存在: {storage_state_file}")
        print("请先运行测试用例以生成登录状态")
        return

    print(f"📂 加载登录状态: {storage_state_file}")
    print(f"🌐 启动浏览器，导航到在线问诊页面...")
    print("💡 浏览器将保持打开，您可以手动调试")
    print("💡 按 Ctrl+C 关闭浏览器")

    async with async_playwright() as p:
        # 使用保存的登录状态启动浏览器
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=project_root / ".playwright" / "user_data",
            headless=False,
            channel="chrome",
            storage_state=str(storage_state_file),
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )

        # 创建新页面并导航
        page = await browser.new_page()
        await page.goto("https://doc-online-test.gstyun.cn/webClinic/index.html#/home")

        # 等待页面加载
        await page.wait_for_timeout(3000)

        # 检查是否还需要登录
        if "#/login" in page.url:
            print("⚠️  登录状态已过期，需要重新登录")
            print("请运行一次测试用例来刷新登录状态")
            await browser.close()
            return

        print("✅ 浏览器已启动并登录成功！")
        print(f"📍 当前页面: {page.url}")
        print("💡 您现在可以手动调试页面")
        print("💡 按 Ctrl+C 退出")

        # 保持浏览器打开，直到用户按 Ctrl+C
        try:
            # 无限等待，直到用户中断
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("\n👋 关闭浏览器...")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(launch_browser())
