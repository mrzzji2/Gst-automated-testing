"""
Generate Login State Script
Run this script to generate login state file, tests can use saved state afterwards
"""
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
USERNAME = os.getenv("GST_USERNAME", "17671792742")
PASSWORD = os.getenv("GST_PASSWORD", "123456")
DOCTOR_NAME = os.getenv("GST_DOCTOR_NAME", "罗慧")
BASE_URL = os.getenv("GST_BASE_URL", "https://doc-online-test.gstyun.cn/webClinic")
STORAGE_STATE_FILE = Path(__file__).parent.parent / "tests" / "storage_state.json"


async def generate_login_state():
    """Generate login state file"""
    print(f"[INFO] Generating login state for: {USERNAME}")
    print(f"[INFO] Output file: {STORAGE_STATE_FILE}")

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(
            headless=False,
            channel="chrome",
            args=["--start-maximized"]
        )

        # Create context
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN"
        )

        # Create page
        page = await context.new_page()
        page.set_default_timeout(30000)

        try:
            # Navigate to login page
            await page.goto(f"{BASE_URL}/index.html#/home")
            print("[OK] Navigated to login page")

            # Wait for login form
            await page.wait_for_selector("input[placeholder*='手机号']", timeout=10000)
            print("[OK] Login form found")

            # Fill credentials
            await page.fill("input[placeholder*='手机号']", USERNAME)
            await page.fill("input[placeholder*='验证码']", PASSWORD)
            print(f"[OK] Credentials filled: {USERNAME}")

            # Click login button
            await page.click("button:has-text('登录')")
            print("[OK] Login button clicked")

            # Wait for page transition
            await asyncio.sleep(3)

            # Check if doctor selection dialog appears
            current_url = page.url
            print(f"[INFO] Current URL: {current_url}")

            if "#/login" in current_url:
                print("[ERROR] Login failed - still on login page")
                return False

            # Handle doctor selection
            try:
                await asyncio.sleep(2)
                radios = page.locator("radio")
                radio_count = await radios.count()

                if radio_count > 0:
                    print(f"[OK] Found {radio_count} doctor(s)")

                    # Try to find specific doctor
                    doctor_radio = page.locator(f"radio:has-text('{DOCTOR_NAME}')")
                    if await doctor_radio.count() > 0:
                        await doctor_radio.first.click()
                        print(f"[OK] Selected doctor: {DOCTOR_NAME}")
                    else:
                        await page.click("radio >> nth=0")
                        print("[OK] Selected first available doctor")

                    await asyncio.sleep(0.5)
                    await page.click("button:has-text('确认'), dialog button:visible >> nth=-1")
                    print("[OK] Confirmed doctor selection")
                    await asyncio.sleep(2)

            except Exception as e:
                print(f"[WARN] Doctor selection issue: {e}")

            # Save storage state
            print(f"[INFO] Saving login state to: {STORAGE_STATE_FILE}")
            await context.storage_state(path=str(STORAGE_STATE_FILE))
            print("[OK] Login state saved successfully!")

            # Verify
            current_url = page.url
            print(f"[INFO] Final URL: {current_url}")

            if "#/login" not in current_url:
                print("[SUCCESS] Login state generation completed!")
                return True
            else:
                print("[ERROR] Failed - still on login page")
                return False

        except Exception as e:
            print(f"[ERROR] Error: {e}")
            return False

        finally:
            await browser.close()
            print("[INFO] Browser closed")


async def verify_login_state():
    """Verify saved login state works"""
    print("\n[INFO] Verifying saved login state...")

    if not STORAGE_STATE_FILE.exists():
        print("[ERROR] No saved login state file found")
        return False

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            storage_state=str(STORAGE_STATE_FILE)
        )
        page = await context.new_page()

        try:
            await page.goto(f"{BASE_URL}/index.html#/home")
            await asyncio.sleep(2)

            current_url = page.url
            print(f"[INFO] Verification URL: {current_url}")

            if "#/login" not in current_url:
                print("[SUCCESS] Saved login state is valid!")
                return True
            else:
                print("[ERROR] Saved login state is invalid (on login page)")
                return False

        finally:
            await browser.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate or verify login state")
    parser.add_argument("--verify", action="store_true", help="Verify saved login state")
    parser.add_argument("--delete", action="store_true", help="Delete saved login state")
    args = parser.parse_args()

    if args.delete:
        if STORAGE_STATE_FILE.exists():
            STORAGE_STATE_FILE.unlink()
            print(f"[OK] Deleted: {STORAGE_STATE_FILE}")
        else:
            print("[INFO] No saved login state file found")
    elif args.verify:
        result = asyncio.run(verify_login_state())
        exit(0 if result else 1)
    else:
        result = asyncio.run(generate_login_state())
        if result:
            # Verify after generation
            verify_result = asyncio.run(verify_login_state())
            exit(0 if verify_result else 1)
        else:
            exit(1)
