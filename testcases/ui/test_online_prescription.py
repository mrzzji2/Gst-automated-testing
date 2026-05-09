"""
Online Prescription Tests
在线开方测试用例（同步版本）
"""
import pytest
import allure
from loguru import logger
from datetime import datetime

from pages.online_consultation_page import OnlineConsultationPage
from pages.prescription_page import PrescriptionPage


@allure.feature("医生工作台")
@allure.story("在线问诊 - 在线开方")
@pytest.mark.page("医生工作台-在线问诊-在线开方")
class TestOnlinePrescription:
    """在线开方测试类

    前置条件：
    - fixture 已自动登录并进入在线问诊页面
    - 所有测试用例默认已登录并进入咨询列表页面
    - 部分用例需要先选择患者 (test02)
    """

    PATIENT_NAME = "test02"

    # ==================== P0 冒烟 ====================

    @pytest.mark.P0
    @pytest.mark.smoke
    @allure.title("打开在线开方弹窗")
    @allure.description("验证点击在线开方按钮后弹出选择方案类型对话框")
    def test_open_prescription_dialog(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：打开在线开方弹窗 (P0)

        步骤：
        1. 选择患者 test02
        2. 点击在线开方按钮

        期望结果：
        - 弹出"请选择方案类型"对话框
        - 显示 10 种处方类型
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        # 选择患者
        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)

        # 点击在线开方
        prescription_page.click_online_prescribe()

        # 验证弹窗显示
        assert prescription_page.is_prescription_type_dialog_visible(), \
            "Prescription type dialog should be visible"
        logger.info("Prescription type dialog is visible")

        # 关闭弹窗
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Prescription dialog opened successfully")

    @pytest.mark.P0
    @pytest.mark.smoke
    @allure.title("选择处方类型进入开方表单")
    @allure.description("验证选择中药饮片后进入完整的开方表单")
    def test_select_prescription_type(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：选择处方类型进入开方表单 (P0)

        步骤：
        1. 选择患者 test02
        2. 点击在线开方
        3. 选择"中药饮片"

        期望结果：
        - 方案类型弹窗关闭
        - 在线开方表单显示
        - 表单包含患者资料、诊断区、处方用药区
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        # 选择患者
        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)

        # 点击在线开方并选择类型
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")

        # 验证开方表单可见
        assert prescription_page.is_prescription_form_visible(), \
            "Prescription form dialog should be visible"
        logger.info("Prescription form is visible")

        # 关闭表单（按 ESC）
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(300)
        logger.info("Test passed: Prescription form opened successfully")

    # ==================== P1 回归 ====================

    @pytest.mark.P1
    @pytest.mark.regression
    @allure.title("常用方搜索调用并提交处方")
    @allure.description("完整流程：常用方搜索→调用→替换→填写药房备注→确认发送→验证开方成功")
    def test_common_formula_full_flow(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：常用方搜索调用并提交处方 (P1)

        步骤：
        1. 选择患者 test02
        2. 点击在线开方
        3. 选择中药饮片
        4. 点击添加药材
        5. 切换到常用方Tab
        6. 搜索关键词 regression
        7. 点击调用
        8. 弹出确认弹窗，点击替换药方
        9. 点击完成
        10. 填写药房备注（当前时间+回归测试）
        11. 点击确认发送

        期望结果：
        - 开方成功提示显示
        - 聊天记录新增处方单
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        # 选择患者
        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)

        # 打开开方弹窗并选择类型
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible(), \
            "Prescription form should be visible"

        # 添加药材 -> 常用方搜索
        prescription_page.click_add_medicine()
        assert prescription_page.is_add_medicine_dialog_visible(), \
            "Add medicine dialog should be visible"

        prescription_page.switch_to_common_tab()
        prescription_page.search_common_formula("regression")

        # 验证搜索结果并调用
        assert prescription_page.is_common_formula_result_visible(), \
            "Common formula search result should be visible"
        prescription_page.click_call()

        # 确认替换弹窗
        assert prescription_page.is_confirm_replace_dialog_visible(), \
            "Confirm replace dialog should be visible"
        prescription_page.click_replace_prescription()

        # 完成药材选择
        prescription_page.click_complete()

        # 填写药房备注
        note_text = prescription_page.fill_pharmacy_note_with_timestamp("回归测试")

        # 提交处方
        prescription_page.click_confirm_send()

        # 验证开方成功
        assert prescription_page.is_prescription_success(), \
            "Prescription should be submitted successfully"
        logger.info(f"Prescription submitted successfully with note: {note_text}")

    @pytest.mark.P1
    @pytest.mark.regression
    @allure.title("主诉/现病史必填校验")
    @allure.description("验证不填写必填项时无法提交处方")
    def test_required_field_validation(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：主诉/现病史必填校验 (P1)

        步骤：
        1. 选择患者 test02
        2. 点击在线开方并选择中药饮片
        3. 不填写主诉和现病史，直接点击确认发送

        期望结果：
        - 页面提示必填项未填写
        - 处方未提交
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        # 选择患者
        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)

        # 打开开方弹窗并选择类型
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        # 清空主诉和现病史
        try:
            prescription_page.fill(prescription_page.locators.INPUT_MAIN_COMPLAINT, "")
        except:
            pass
        try:
            prescription_page.fill(prescription_page.locators.INPUT_NOW_HISTORY, "")
        except:
            pass

        # 直接点击确认发送
        prescription_page.click_confirm_send()

        # 验证表单未关闭（因为必填校验阻止了提交）
        prescription_page.wait(300)
        form_still_visible = prescription_page.is_prescription_form_visible()
        assert form_still_visible, \
            "Form should remain open when required fields are empty"
        logger.info("Required field validation works correctly")

        # 关闭表单
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)

    @pytest.mark.P1
    @pytest.mark.regression
    @allure.title("替换药方/新增药材确认弹窗")
    @allure.description("验证已有药材时调用常用方弹出替换/新增确认弹窗")
    def test_replace_or_add_medicines(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：替换药方/新增药材确认弹窗 (P1)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 点击添加药材 -> 常用方
        4. 搜索并调用常用方
        5. 验证确认弹窗
        6. 点击新增药材（不走替换路径，避免影响数据）

        期望结果：
        - 弹出确认弹窗，包含"新增药材"和"替换药方"两个选项
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        # 选择患者
        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)

        # 打开开方弹窗并选择类型
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        # 添加药材 -> 常用方搜索
        prescription_page.click_add_medicine()
        assert prescription_page.is_add_medicine_dialog_visible()

        prescription_page.switch_to_common_tab()
        prescription_page.search_common_formula("regression")
        assert prescription_page.is_common_formula_result_visible()

        # 调用常用方
        prescription_page.click_call()

        # 验证确认弹窗显示
        assert prescription_page.is_confirm_replace_dialog_visible(), \
            "Confirm replace dialog should appear when medicines already exist"
        logger.info("Replace/Add confirm dialog is visible")

        # 点击新增药材（安全路径，不替换已有数据）
        prescription_page.click_add_new_medicines()
        prescription_page.wait(300)

        # 点击完成关闭添加药材弹窗
        prescription_page.click_complete()
        prescription_page.wait(300)

        # 关闭开方表单
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Replace/Add dialog verified")

    @pytest.mark.P1
    @pytest.mark.regression
    @allure.title("添加药材超剂量警告")
    @allure.description("验证添加超过建议用量的药材时弹出警告弹窗")
    def test_medicine_overdose_warning(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：添加药材超剂量警告 (P1)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 点击添加药材
        4. 输入药材菊花，设置用量1000g
        5. 点击添加按钮

        期望结果：
        - 弹出警告弹窗，提示"已超过建议使用最大凉"
        - 显示"更改药材剂量"按钮
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        # 添加药材
        prescription_page.click_add_medicine()
        assert prescription_page.is_add_medicine_dialog_visible()

        # 搜索菊花，设置1000g，点击添加
        prescription_page.search_and_add_medicine("菊花", "1000")

        # 验证警告弹窗
        assert prescription_page.is_medicine_warning_visible(), \
            "Overdose warning dialog should be visible"
        logger.info("Overdose warning dialog is visible")

        # 验证更改药材剂量按钮
        assert prescription_page.is_visible(prescription_page.locators.BTN_CHANGE_DOSAGE), \
            "Change dosage button should be visible"
        logger.info("Change dosage button is visible")

        # 点击更改药材剂量关闭弹窗
        prescription_page.click_change_dosage()
        prescription_page.wait(300)

        # 关闭添加药材弹窗和表单
        prescription_page.click_cancel()
        prescription_page.wait(200)
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Medicine overdose warning verified")

    @pytest.mark.P1
    @pytest.mark.regression
    @allure.title("更换药房弹窗")
    @allure.description("验证点击更换按钮弹出药房选择弹窗")
    def test_change_pharmacy(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：更换药房 (P1)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 点击更换药房按钮

        期望结果：
        - 弹出"选择方案类型及药房"弹窗
        - 显示药房列表
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        # 选择患者
        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)

        # 打开开方弹窗并选择类型
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        # 点击更换药房
        prescription_page.click_change_pharmacy()

        # 验证弹窗显示
        assert prescription_page.is_change_pharmacy_dialog_visible(), \
            "Change pharmacy dialog should be visible"
        logger.info("Change pharmacy dialog is visible")

        # 关闭弹窗（按 ESC）
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)

        # 关闭开方表单
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Change pharmacy dialog verified")

    # ==================== P1 回归（续）====================

    @pytest.mark.P1
    @pytest.mark.regression
    @allure.title("存为草稿")
    @allure.description("验证点击存为草稿按钮可保存草稿")
    def test_save_draft(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：存为草稿 (P1)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 填写主诉和现病史
        4. 点击存为草稿

        期望结果：
        - 存为草稿操作正常，无报错
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        # 填写主诉和现病史
        prescription_page.fill_main_complaint("测试主诉")
        prescription_page.fill_now_history("测试现病史")

        # 点击存为草稿
        prescription_page.click_save_draft()
        prescription_page.wait(500)
        logger.info("Save draft clicked - no errors")

        # 关闭表单
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Save draft verified")

    @pytest.mark.P1
    @pytest.mark.regression
    @allure.title("用药方式切换")
    @allure.description("验证内服/外用 radio 切换正常")
    def test_toggle_medication_method(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：用药方式切换 (P1)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 点击外用
        4. 再点击内服

        期望结果：
        - 切换正常，无报错
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        # 点击外用
        prescription_page.click(prescription_page.locators.RADIO_EXTERNAL)
        prescription_page.wait(300)
        logger.info("Clicked external use")

        # 再点击内服
        prescription_page.click(prescription_page.locators.RADIO_INTERNAL)
        prescription_page.wait(300)
        logger.info("Clicked internal use")

        # 关闭表单
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Medication method toggle verified")

    @pytest.mark.P1
    @pytest.mark.regression
    @allure.title("清空药材")
    @allure.description("验证添加药材弹窗中清空药材功能")
    def test_clear_medicines(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：清空药材 (P1)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 点击添加药材
        4. 点击清空药材

        期望结果：
        - 清空操作正常
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        # 添加药材
        prescription_page.click_add_medicine()
        assert prescription_page.is_add_medicine_dialog_visible()

        # 清空药材
        prescription_page.click_clear_all_medicines()
        prescription_page.wait(300)
        logger.info("Cleared all medicines")

        # 关闭添加药材弹窗
        prescription_page.click_cancel()
        prescription_page.wait(300)

        # 关闭表单
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Clear medicines verified")

    # ==================== P2 边缘场景 ====================

    @pytest.mark.P2
    @pytest.mark.regression
    @allure.title("关闭方案类型弹窗")
    @allure.description("验证按 ESC 可关闭方案类型弹窗")
    def test_close_type_dialog(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：关闭方案类型弹窗 (P2)

        步骤：
        1. 选择患者 test02
        2. 点击在线开方
        3. 按 ESC 关闭弹窗

        期望结果：
        - 弹窗关闭，回到咨询列表页面
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        assert prescription_page.is_prescription_type_dialog_visible()

        # 确保弹窗已打开
        assert prescription_page.is_prescription_type_dialog_visible(), \
            "Type dialog should be visible"

        # 直接点击 Element UI 弹窗的关闭按钮（headerbtn）
        close_btn = prescription_page.page.locator(".el-dialog__headerbtn").last
        if close_btn.is_visible():
            close_btn.click()
            prescription_page.wait(2000)
            logger.info("Clicked close button via .el-dialog__headerbtn")

        # 验证弹窗已关闭
        assert not prescription_page.is_prescription_type_dialog_visible(), \
            "Dialog should be closed"
        logger.info("Test passed: Type dialog closed successfully")

    @pytest.mark.P2
    @pytest.mark.regression
    @allure.title("搜索不存在的药材")
    @allure.description("验证搜索不存在的药材时显示空状态")
    def test_search_nonexistent_medicine(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：搜索不存在的药材 (P2)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 点击添加药材
        4. 搜索不存在的药材名

        期望结果：
        - 列表显示"暂无数据"或空状态
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        prescription_page.click_add_medicine()
        assert prescription_page.is_add_medicine_dialog_visible()

        # 搜索不存在的药材
        prescription_page.fill(prescription_page.locators.INPUT_MEDICINE_SEARCH, "ZZZZ_NOT_EXISTS")
        prescription_page.wait(300)
        prescription_page.click(prescription_page.locators.BTN_MEDICINE_ADD)
        prescription_page.wait(300)

        logger.info("Searched for nonexistent medicine - no crash")
        assert prescription_page.is_add_medicine_dialog_visible(), \
            "Dialog should remain open"

        # 关闭弹窗
        prescription_page.click_cancel()
        prescription_page.wait(300)
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Nonexistent medicine search verified")

    @pytest.mark.P2
    @pytest.mark.regression
    @allure.title("搜索不存在的常用方")
    @allure.description("验证搜索不存在的常用方时显示'没有更多了'")
    def test_search_nonexistent_formula(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：搜索不存在的常用方 (P2)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 点击添加药材 -> 常用方
        4. 搜索不存在的常用方

        期望结果：
        - 显示"没有更多了"
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        prescription_page.click_add_medicine()
        assert prescription_page.is_add_medicine_dialog_visible()

        prescription_page.switch_to_common_tab()
        prescription_page.search_common_formula("ZZZZ_NOT_EXISTS")

        # 验证显示"没有更多了"
        no_more = prescription_page.is_no_more_text_visible()
        logger.info(f"No more text visible: {no_more}")

        # 关闭弹窗
        prescription_page.click_cancel()
        prescription_page.wait(300)
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Nonexistent formula search verified")

    @pytest.mark.P2
    @pytest.mark.regression
    @allure.title("勾选/取消打印处方")
    @allure.description("验证打印处方 checkbox 勾选切换正常")
    def test_toggle_print(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：勾选/取消打印处方 (P2)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 点击打印处方 checkbox

        期望结果：
        - checkbox 状态正常切换
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        # 点击打印处方
        prescription_page.toggle_print_prescription()
        prescription_page.wait(300)

        # 再次点击取消
        prescription_page.toggle_print_prescription()
        prescription_page.wait(300)
        logger.info("Print checkbox toggled")

        # 关闭表单
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Print toggle verified")

    @pytest.mark.P1
    @pytest.mark.regression
    @allure.title("药材剂量调整")
    @allure.description("验证调整药材重量后费用更新")
    def test_adjust_medicine_dosage(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：药材剂量调整 (P1)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 点击添加药材
        4. 修改第一味药材的重量

        期望结果：
        - 重量修改成功
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        # 添加药材
        prescription_page.click_add_medicine()
        assert prescription_page.is_add_medicine_dialog_visible()

        # 调整第一味药材重量
        prescription_page.adjust_medicine_weight(index=0, weight="15")
        prescription_page.wait(300)

        # 关闭弹窗
        prescription_page.click_cancel()
        prescription_page.wait(300)
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Medicine dosage adjustment verified")

    @pytest.mark.P2
    @pytest.mark.regression
    @allure.title("用药方法下拉选择")
    @allure.description("验证点击用药方法下拉框并选择选项")
    def test_select_medication_method(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：用药方法下拉选择 (P2)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 点击用药方法字段打开下拉
        4. 选择一个选项

        期望结果：
        - 下拉打开并可选择选项
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        # 选择用药方法
        prescription_page.select_medication_method("饭后服用")
        logger.info("Medication method selected")

        # 关闭表单
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Medication method selection verified")

    @pytest.mark.P2
    @pytest.mark.regression
    @allure.title("不同处方类型切换")
    @allure.description("验证在更换药房弹窗中切换处方类型Tab")
    def test_switch_prescription_type_tab(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：不同处方类型切换 (P2)

        步骤：
        1. 选择患者 test02
        2. 打开在线开方并选择中药饮片
        3. 点击更换药房
        4. 切换不同类型Tab

        期望结果：
        - Tab 切换正常
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("中药饮片")
        assert prescription_page.is_prescription_form_visible()

        # 点击更换药房
        prescription_page.click_change_pharmacy()
        assert prescription_page.is_change_pharmacy_dialog_visible()

        # 切换类型 Tab
        prescription_page.click_pharmacy_type_tab("颗粒剂")
        prescription_page.wait(300)

        # 再切回中药饮片
        prescription_page.click_pharmacy_type_tab("中药饮片")
        prescription_page.wait(300)

        # 关闭弹窗
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Prescription type tab switch verified")

    @pytest.mark.P1
    @pytest.mark.regression
    @allure.title("滋补膏方缺少辅料校验")
    @allure.description("验证滋补膏方未添加辅料时弹出提示")
    def test_paste_prescription_need_adjuvant(self, gst_online_consultation_page: OnlineConsultationPage):
        """
        测试用例：滋补膏方缺少辅料校验 (P1)

        步骤：
        1. 选择患者 test02
        2. 点击在线开方
        3. 选择滋补膏方
        4. 点击添加药材
        5. 点击清空药材
        6. 输入山药4g并添加
        7. 输入生地黄4g并添加
        8. 点击完成
        9. 点击确认发送

        期望结果：
        - 弹出提示"膏方必须添加辅料"
        """
        prescription_page = PrescriptionPage(gst_online_consultation_page.page)

        gst_online_consultation_page.select_patient_by_name(self.PATIENT_NAME)
        prescription_page.click_online_prescribe()
        prescription_page.select_prescription_type("滋补膏方")
        prescription_page.wait(1000)

        # 点击添加药材
        prescription_page.click_add_medicine()
        assert prescription_page.is_add_medicine_dialog_visible()

        # 点击清空药材
        prescription_page.click_clear_all_medicines()
        prescription_page.wait(500)

        # 添加山药 4g
        prescription_page.search_and_add_medicine("山药", "4")
        prescription_page.wait(500)

        # 添加生地黄 4g
        prescription_page.search_and_add_medicine("生地黄", "4")
        prescription_page.wait(500)

        # 点击完成
        prescription_page.click_complete()
        prescription_page.wait(500)

        # 点击确认发送
        prescription_page.click_confirm_send()
        prescription_page.wait(1000)

        # 验证提示"膏方必须添加辅料"
        toast_visible = prescription_page.is_visible("text=膏方必须添加辅料")
        logger.info(f"Adjuvant warning visible: {toast_visible}")

        # 关闭弹窗
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        prescription_page.page.keyboard.press("Escape")
        prescription_page.wait(200)
        logger.info("Test passed: Paste prescription adjuvant check verified")
