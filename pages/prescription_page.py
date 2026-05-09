"""
Prescription Page - Synchronous Version
在线开方页面对象 - 同步版本
"""
from datetime import datetime
from typing import List
from playwright.sync_api import Page
from loguru import logger

from pages.base_page import BasePage
from elements.prescription_locators import PrescriptionLocators


class PrescriptionPage(BasePage):
    """
    在线开方页面对象 - 同步版本
    封装在线开方相关的所有操作（选择方案类型、填写表单、添加药材、常用方调用、提交等）
    注意：开方为弹窗形式，前置条件为已登录并进入在线问诊页面且已选择患者
    """

    def __init__(self, page: Page, base_url: str = ""):
        super().__init__(page, base_url)
        self.locators = PrescriptionLocators()

    # ==================== 打开开方弹窗 ====================

    def wait_for_loading_complete(self, timeout: int = 15000):
        """等待页面加载完成（loading 遮罩消失）"""
        try:
            self.page.wait_for_selector(".el-loading-mask", state="hidden", timeout=timeout)
        except:
            pass
        logger.debug("Loading complete")

    def click_online_prescribe(self):
        """点击在线开方按钮"""
        self.click(self.locators.BTN_ONLINE_PRESCRIBE)
        # 等待弹窗加载完成
        self.wait_for_loading_complete()
        logger.info("Clicked online prescribe button")

    # ==================== 选择方案类型 ====================

    def is_prescription_type_dialog_visible(self) -> bool:
        """判断选择方案类型弹窗是否可见"""
        return self.is_visible(self.locators.PRESCRIPTION_TYPE_DIALOG)

    def get_prescription_type_count(self) -> int:
        """获取处方类型数量"""
        return self.count_elements(
            self.locators.PRESCRIPTION_TYPE_DIALOG + " >> div[class*='item'], .el-dialog__body .flex-item"
        )

    def select_prescription_type(self, type_name: str = "中药饮片"):
        """
        选择处方类型（在方案类型弹窗范围内点击）

        Args:
            type_name: 处方类型名称，如 中药饮片、颗粒剂 等
        """
        # 等待弹窗完全加载
        self.wait_for_loading_complete()
        self.page.wait_for_selector(self.locators.PRESCRIPTION_TYPE_DIALOG, state="visible", timeout=10000)
        # 限定在弹窗内点击，避免匹配到患者列表中的同名文本
        dialog_scope = self.locators.PRESCRIPTION_TYPE_DIALOG
        selector = f"{dialog_scope} >> text={type_name}"
        self.click(selector)
        logger.info(f"Selected prescription type: {type_name}")

    def close_prescription_type_dialog(self):
        """关闭选择方案类型弹窗"""
        self.click(self.locators.PRESCRIPTION_TYPE_CLOSE)
        logger.info("Closed prescription type dialog")

    # ==================== 开方表单操作 ====================

    def is_prescription_form_visible(self) -> bool:
        """判断开方表单是否可见"""
        return self.is_visible(self.locators.PRESCRIPTION_FORM_DIALOG)

    def fill_main_complaint(self, text: str):
        """填写主诉"""
        self.fill(self.locators.INPUT_MAIN_COMPLAINT, text)
        logger.info(f"Filled main complaint: {text}")

    def fill_now_history(self, text: str):
        """填写现病史"""
        self.fill(self.locators.INPUT_NOW_HISTORY, text)
        logger.info(f"Filled now history: {text}")

    def click_expand_record(self):
        """点击展开病历"""
        self.click(self.locators.BTN_EXPAND_RECORD)
        logger.info("Clicked expand record")

    def click_import_questionnaire(self):
        """点击导入问诊单"""
        self.click(self.locators.BTN_IMPORT_QUESTIONNAIRE)
        logger.info("Clicked import questionnaire")

    def click_save_draft(self):
        """点击存为草稿"""
        self.click(self.locators.BTN_SAVE_DRAFT)
        logger.info("Clicked save draft")

    # ==================== 添加药材 ====================

    def click_add_medicine(self):
        """点击添加药材按钮"""
        self.click(self.locators.BTN_ADD_MEDICINE)
        self.wait_for_loading_complete()
        logger.info("Clicked add medicine button")

    def search_and_add_medicine(self, name: str, weight: str):
        """
        在添加药材弹窗中搜索药材、设置剂量并点击添加

        Args:
            name: 药材名称
            weight: 剂量（克）
        """
        # 1. 点击搜索框激活 Vue 组件
        self.page.locator(self.locators.INPUT_MEDICINE_SEARCH).click()
        self.wait(500)

        # 2. 通过 JS 清空并设置药材名称
        self.page.evaluate("""(name) => {
            const dialogs = document.querySelectorAll('[role="dialog"]');
            let dialog = null;
            dialogs.forEach(d => {
                if (d.textContent.includes('当前选择药房')) dialog = d;
            });
            if (!dialog) return;
            const inputs = dialog.querySelectorAll('input');
            for (const input of inputs) {
                if (input.placeholder.includes('请输入药材名称')) {
                    input.removeAttribute('readonly');
                    input.focus();
                    const setter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, 'value'
                    ).set;
                    setter.call(input, '');
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    setter.call(input, name);
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('compositionend', { bubbles: true }));
                    break;
                }
            }
        }""", name)
        self.wait(2000)

        # 3. 点击搜索结果中的药材名称
        text_selector = f"{self.locators.ADD_MEDICINE_DIALOG} >> .name:has-text('{name}')"
        search_result = self.page.locator(text_selector).first
        try:
            search_result.wait_for(state="visible", timeout=5000)
            search_result.click()
        except:
            # 备选：直接点击文本
            self.page.locator(f"{self.locators.ADD_MEDICINE_DIALOG} >> text={name}").first.click()
        self.wait(300)

        # 4. 通过 JS 设置重量（input type=number 需要特殊处理）
        self.page.evaluate("""(weight) => {
            const dialogs = document.querySelectorAll('[role="dialog"]');
            let medicineDialog = null;
            dialogs.forEach(d => {
                if (d.textContent.includes('当前选择药房')) medicineDialog = d;
            });
            if (!medicineDialog) return;
            const inputs = medicineDialog.querySelectorAll('input');
            for (const input of inputs) {
                if (input.type === 'number') {
                    const setter = Object.getOwnPropertyDescriptor(
                        window.HTMLInputElement.prototype, 'value'
                    ).set;
                    setter.call(input, weight);
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    break;
                }
            }
        }""", weight)
        self.wait(300)
        logger.info(f"Set medicine '{name}' weight to {weight}g via JS")

        # 5. 点击添加
        self.click(self.locators.BTN_MEDICINE_ADD)
        self.wait(500)
        logger.info(f"Clicked add button for '{name}' with weight {weight}g")

    def is_medicine_warning_visible(self) -> bool:
        """判断药材剂量警告弹窗是否可见"""
        return self.is_visible(self.locators.MEDICINE_WARNING_DIALOG)

    def click_change_dosage(self):
        """点击更改药材剂量按钮"""
        self.click(self.locators.BTN_CHANGE_DOSAGE)
        logger.info("Clicked change dosage button")

    def is_add_medicine_dialog_visible(self) -> bool:
        """判断添加药材弹窗是否可见"""
        return self.is_visible(self.locators.ADD_MEDICINE_DIALOG)

    def click_clear_all_medicines(self):
        """点击清空药材"""
        self.click(self.locators.BTN_CLEAR_ALL)
        logger.info("Clicked clear all medicines")

    def click_complete(self):
        """点击完成按钮（关闭添加药材弹窗）"""
        self.click(self.locators.BTN_COMPLETE)
        self.wait_for_loading_complete()
        self.wait(300)
        logger.info("Clicked complete button")

    def click_cancel(self):
        """点击取消按钮"""
        self.click(self.locators.BTN_CANCEL)
        logger.info("Clicked cancel button")

    # ==================== 常用方 ====================

    def switch_to_common_tab(self):
        """切换到常用方 Tab"""
        # 等待弹窗动画完成
        self.page.wait_for_selector(self.locators.ADD_MEDICINE_DIALOG, state="visible", timeout=10000)
        self.wait(300)
        self.click(self.locators.TAB_COMMON)
        logger.info("Switched to common formula tab")

    def switch_to_history_tab(self):
        """切换到历史方 Tab"""
        self.page.wait_for_selector(self.locators.ADD_MEDICINE_DIALOG, state="visible", timeout=10000)
        self.click(self.locators.TAB_HISTORY)
        logger.info("Switched to history formula tab")

    def switch_to_classic_tab(self):
        """切换到经典方 Tab"""
        self.page.wait_for_selector(self.locators.ADD_MEDICINE_DIALOG, state="visible", timeout=10000)
        self.click(self.locators.TAB_CLASSIC)
        logger.info("Switched to classic formula tab")

    def search_common_formula(self, keyword: str):
        """
        搜索常用方

        Args:
            keyword: 搜索关键词
        """
        self.fill(self.locators.INPUT_COMMON_SEARCH, keyword)
        self.wait(200)
        self.click(self.locators.BTN_COMMON_SEARCH)
        logger.info(f"Searched common formula: {keyword}")

    def click_call(self):
        """点击调用按钮（第一个匹配的常用方）"""
        self.wait_for_loading_complete()
        self.click(self.locators.BTN_CALL)
        logger.info("Clicked call button")

    def is_common_formula_result_visible(self) -> bool:
        """判断常用方搜索结果是否可见"""
        return self.is_visible(self.locators.BTN_CALL)

    # ==================== 调用确认弹窗 ====================

    def is_confirm_replace_dialog_visible(self) -> bool:
        """判断替换确认弹窗是否可见"""
        return self.is_visible(self.locators.CONFIRM_REPLACE_DIALOG)

    def click_add_new_medicines(self):
        """点击新增药材（在已有药材基础上追加）"""
        self.click(self.locators.BTN_ADD_NEW)
        logger.info("Clicked add new medicines")

    def click_replace_prescription(self):
        """点击替换药方"""
        self.click(self.locators.BTN_REPLACE)
        logger.info("Clicked replace prescription")

    # ==================== 药房操作 ====================

    def click_change_pharmacy(self):
        """点击更换药房"""
        self.click(self.locators.BTN_CHANGE_PHARMACY)
        self.wait_for_loading_complete()
        self.wait(500)
        logger.info("Clicked change pharmacy")

    def is_change_pharmacy_dialog_visible(self) -> bool:
        """判断更换药房弹窗是否存在（在 DOM 中）"""
        try:
            self.page.wait_for_selector(self.locators.CHANGE_PHARMACY_DIALOG, state="attached", timeout=10000)
            return True
        except:
            return False

    # ==================== 药房备注 ====================

    def fill_pharmacy_note(self, text: str):
        """
        填写药房备注

        Args:
            text: 备注内容
        """
        self.fill(self.locators.INPUT_PHARMACY_NOTE, text)
        logger.info(f"Filled pharmacy note: {text}")

    def fill_pharmacy_note_with_timestamp(self, suffix: str = "回归测试"):
        """
        填写药房备注（带当前时间戳）

        Args:
            suffix: 备注文案后缀，默认"回归测试"
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        text = f"{now} {suffix}"
        self.fill_pharmacy_note(text)
        return text

    # ==================== 提交处方 ====================

    def click_confirm_send(self):
        """点击确认发送"""
        self.click(self.locators.BTN_CONFIRM_SEND)
        logger.info("Clicked confirm send")

    def is_prescription_success(self) -> bool:
        """判断开方是否成功（验证开方成功提示可见）"""
        return self.is_visible(self.locators.TOAST_SUCCESS)

    def toggle_print_prescription(self):
        """勾选/取消打印处方"""
        self.click(self.locators.CHECKBOX_PRINT)
        logger.info("Toggled print prescription")

    # ==================== 剂量调整 ====================

    def adjust_medicine_weight(self, index: int = 0, weight: str = "10"):
        """
        在添加药材弹窗中调整药材重量

        Args:
            index: 药材索引（从0开始）
            weight: 新的重量值
        """
        scope = self.locators.ADD_MEDICINE_DIALOG
        # 获取弹窗内所有重量 spinbutton
        spinbuttons = self.page.locator(f"{scope} >> spinbutton")
        count = spinbuttons.count()
        if count > index:
            spinbuttons.nth(index).fill(weight)
            spinbuttons.nth(index).press("Enter")
            logger.info(f"Adjusted medicine [{index}] weight to {weight}g")
        else:
            logger.warning(f"Only {count} spinbuttons found, cannot adjust index {index}")

    def get_single_dose_cost(self) -> str:
        """获取添加药材弹窗中的单剂费用文本"""
        try:
            cost_text = self.page.locator(f"{self.locators.ADD_MEDICINE_DIALOG} >> text=单剂费用").text_content()
            if cost_text:
                return cost_text.strip()
            return ""
        except:
            return ""

    def select_medication_method(self, option_text: str = "饭后服用"):
        """
        选择用药方法（通过 JS 点击下拉选项）

        Args:
            option_text: 选项文本
        """
        self.wait(800)

        # 通过 JS 触发 Element UI 的下拉
        self.page.evaluate("""
            () => {
                const input = document.querySelector('[placeholder="请填写（选填）"]');
                if (!input) return;
                const select = input.closest('.el-select');
                if (!select) return;
                select.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
            }
        """)
        self.wait(800)

        # 通过 JS 点击第一个可见的下拉选项
        clicked = self.page.evaluate("""() => {
            const items = document.querySelectorAll('.el-select-dropdown__item');
            for (const item of items) {
                if (item.offsetParent !== null) {
                    item.click();
                    return 'clicked: ' + item.textContent.trim();
                }
            }
            if (items.length > 0) {
                items[0].click();
                return 'clicked(force): ' + items[0].textContent.trim();
            }
            return 'no items found';
        }""")
        logger.info(f"Dropdown item clicked: {clicked}")
        self.wait(300)

    def click_pharmacy_type_tab(self, tab_name: str = "颗粒剂"):
        """
        在更换药房弹窗中点击处方类型 Tab

        Args:
            tab_name: Tab 名称，如 颗粒剂、定制丸剂 等
        """
        scope = self.locators.CHANGE_PHARMACY_DIALOG
        self.click(f"{scope} >> text={tab_name}")
        self.wait(500)
        logger.info(f"Clicked pharmacy type tab: {tab_name}")

    def is_empty_search_result(self) -> bool:
        """判断添加药材弹窗中搜索结果是否为空"""
        try:
            return self.is_visible(f"{self.locators.ADD_MEDICINE_DIALOG} >> text=暂无数据")
        except:
            return False

    def is_no_more_text_visible(self) -> bool:
        """判断常用方搜索结果是否显示'没有更多了'"""
        return self.is_visible("text=没有更多了")

    def get_draft_count(self) -> int:
        """获取草稿箱数量"""
        try:
            draft_heading = self.page.locator("heading:has-text('草稿箱')")
            if draft_heading.count() > 0:
                parent = draft_heading.locator("..")
                text = parent.text_content()
                import re
                numbers = re.findall(r'\d+', text)
                if numbers:
                    return int(numbers[0])
        except:
            pass
        return 0

    # ==================== 综合操作 ====================

    def get_medicine_count(self) -> int:
        """获取当前处方药材数量（从页面上提取）"""
        try:
            count_text = self.get_text(self.locators.MEDICINE_COUNT_TEXT)
            import re
            numbers = re.findall(r'\d+', count_text)
            if numbers:
                return int(numbers[0])
        except:
            pass
        return 0

    def get_total_price_text(self) -> str:
        """获取方案总计金额文本"""
        try:
            return self.get_text(self.locators.TOTAL_PRICE_TEXT)
        except:
            return ""
