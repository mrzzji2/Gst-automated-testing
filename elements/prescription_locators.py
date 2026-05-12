"""
Prescription Page Locators
在线开方页元素定位器
"""


class PrescriptionLocators:
    """在线开方页元素定位器"""

    # ==================== 在线开方入口 ====================
    BTN_ONLINE_PRESCRIBE = "text=在线开方"

    # ==================== 选择方案类型弹窗 ====================
    PRESCRIPTION_TYPE_DIALOG = "[role='dialog']:has-text('请选择方案类型')"
    # 类型选择限定在弹窗内，避免匹配到患者列表中的同名文本
    PRESCRIPTION_TYPE_HERBAL = "[role='dialog']:has-text('请选择方案类型') >> text=中药饮片"
    PRESCRIPTION_TYPE_GRANULE = "[role='dialog']:has-text('请选择方案类型') >> text=颗粒剂"
    PRESCRIPTION_TYPE_PILL = "[role='dialog']:has-text('请选择方案类型') >> text=定制丸剂"
    PRESCRIPTION_TYPE_POWDER = "[role='dialog']:has-text('请选择方案类型') >> text=打粉散剂"
    PRESCRIPTION_TYPE_PASTE = "[role='dialog']:has-text('请选择方案类型') >> text=滋补膏方"
    PRESCRIPTION_TYPE_WESTERN = "[role='dialog']:has-text('请选择方案类型') >> text=中西成药"
    PRESCRIPTION_TYPE_EXPERIENCE = "[role='dialog']:has-text('请选择方案类型') >> text=经验方"
    PRESCRIPTION_TYPE_EXTERNAL = "[role='dialog']:has-text('请选择方案类型') >> text=外治项目"
    PRESCRIPTION_TYPE_HOSPITAL = "[role='dialog']:has-text('请选择方案类型') >> text=院内制剂"
    PRESCRIPTION_TYPE_SPECIAL = "[role='dialog']:has-text('请选择方案类型') >> text=特色剂型"
    PRESCRIPTION_TYPE_CLOSE = "[role='dialog']:has-text('请选择方案类型') >> [aria-label='Close'], [role='dialog']:has-text('请选择方案类型') >> .el-dialog__headerbtn"

    # ==================== 开方表单 ====================
    PRESCRIPTION_FORM_DIALOG = "[role='dialog']:has-text('在线开方')"
    BTN_EXPAND_RECORD = "text=展开病历"
    BTN_IMPORT_QUESTIONNAIRE = "text=导入问诊单"
    BTN_SAVE_DRAFT = "[role='dialog']:has-text('在线开方') >> text=存为草稿"

    # 诊断区
    INPUT_MAIN_COMPLAINT = "[placeholder='请填写主诉病史']"
    INPUT_NOW_HISTORY = "[placeholder='请填写现病史']"
    BTN_DIAGNOSIS_DELETE = "text=头疼 >> .. >> button:has-text('')"
    INPUT_DIAGNOSIS = "textbox:has-text('中医诊断')"
    INPUT_SYNDROME = "textbox:has-text('请选择中医证型')"

    # 处方用药区
    PHARMACY_HEADING = "heading:has-text('中药饮片')"
    PHARMACY_NOTE_TEXT = "text=1111111"
    BTN_CHANGE_PHARMACY = "text=更换"
    BTN_ADD_MEDICINE = "text=添加药材"
    MEDICINE_COUNT_TEXT = "text=味药材"
    TOTAL_WEIGHT_TEXT = "text=总重"
    BTN_SAVE_COMMON = "button:has-text('存为常用方')"

    # 剂量设置
    SPIN_TOTAL_DOSES = "spinbutton:has-text('共')"
    SPIN_DAILY_DOSES = "spinbutton:has-text('每日')"
    SPIN_DAILY_TIMES = "spinbutton:has-text('次')"

    # 用药设置区（限定在开方表单内）
    DRUG_FORM_SELF = "text=自煎"
    RADIO_INTERNAL = "[role='dialog']:has-text('在线开方') >> text=内服"
    RADIO_EXTERNAL = "[role='dialog']:has-text('在线开方') >> text=外用"
    INPUT_MEDICATION_METHOD = "[placeholder='请填写（选填）']"
    SELECT_MEDICATION_METHOD = ".el-select:has([placeholder='请填写（选填）'])"
    INPUT_DOCTOR_ADVICE = "[placeholder='请填写医生嘱咐（选填）']"
    BTN_COMMON_ADVICE = "text=常用医嘱"
    INPUT_PHARMACY_NOTE = "[placeholder='请填写药房备注（选填）']"
    BTN_COMMON_NOTE = "text=常用备注"

    # 底部
    BTN_EXPAND = "button:has-text('展开')"
    TOTAL_PRICE_TEXT = "text=方案总计"
    CHECKBOX_PRINT = "[role='dialog']:has-text('在线开方') >> text=打印处方"
    BTN_CONFIRM_SEND = "button:has-text('确认发送')"

    # ==================== 用药方法下拉 ====================
    DROPDOWN_ITEM = ".el-select-dropdown__item"

    # ==================== 更换药房弹窗 ====================
    CHANGE_PHARMACY_DIALOG = ".el-dialog.pharmacys"
    PHARMACY_TYPE_TAB = ".el-dialog.pharmacys >> .el-tabs__item"

    # ==================== 添加药材弹窗 ====================
    ADD_MEDICINE_DIALOG = "[role='dialog']:has-text('当前选择药房')"
    INPUT_MEDICINE_SEARCH = f"{ADD_MEDICINE_DIALOG} >> [placeholder='请输入药材名称']"
    INPUT_MEDICINE_WEIGHT = f"{ADD_MEDICINE_DIALOG} >> [placeholder='重量'], {ADD_MEDICINE_DIALOG} >> spinbutton"
    BTN_MEDICINE_ADD = f"{ADD_MEDICINE_DIALOG} >> button:has-text('添加')"
    BTN_SMART_RECOGNIZE = "text=智能识方"
    BTN_REPLACE_MISSING = "text=缺药替换"
    BTN_CLEAR_ALL = "text=清空药材"
    BTN_CANCEL = f"{ADD_MEDICINE_DIALOG} >> button:has-text('取消')"
    BTN_COMPLETE = f"{ADD_MEDICINE_DIALOG} >> button:has-text('完成')"

    # ==================== 药材剂量警告弹窗 ====================
    MEDICINE_WARNING_DIALOG = "text=已超过建议使用最大量"
    MEDICINE_WARNING_TEXT = "text=请修改药材剂量"
    BTN_CHANGE_DOSAGE = "button:has-text('更改药材剂量')"

    # ==================== 十八反药材警告弹窗 ====================
    SHIBAFAN_WARNING_DIALOG = "text=十八反药材"
    BTN_CHANGE_MEDICINE = "button:has-text('更改药材')"
    BTN_SIGN_USE = "button:has-text('签名使用')"

    # 常用方 Tab（限定在添加药材弹窗内）
    TAB_COMMON = f"{ADD_MEDICINE_DIALOG} >> text=常用方"
    TAB_HISTORY = f"{ADD_MEDICINE_DIALOG} >> text=历史方"
    TAB_CLASSIC = f"{ADD_MEDICINE_DIALOG} >> text=经典方"
    INPUT_COMMON_SEARCH = f"{ADD_MEDICINE_DIALOG} >> [placeholder='输入常用方名称搜索']"
    BTN_COMMON_SEARCH = f"{ADD_MEDICINE_DIALOG} >> button:has-text('搜索')"
    BTN_CALL = f"{ADD_MEDICINE_DIALOG} >> button:has-text('调用')"

    # ==================== 调用确认弹窗 ====================
    CONFIRM_REPLACE_DIALOG = "text=替换现有药材"
    BTN_ADD_NEW = "button:has-text('新增药材')"
    BTN_REPLACE = "button:has-text('替换药方')"

    # ==================== 开方成功提示 ====================
    TOAST_SUCCESS = "text=开方成功"
