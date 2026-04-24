"""
Online Consultation Page Locators
在线问诊页元素定位器
"""


class OnlineConsultationLocators:
    """在线问诊页元素定位器"""

    # ==================== 页面标题 ====================
    # 页面标题可能在title标签或其他元素中
    PAGE_TITLE = "title:has-text('固生堂')"
    DOCTOR_NAME = ".doctor-name, [class*='doctor']"

    # ==================== 顶部导航 ====================
    NAV_AI_CLINIC = "a:has-text('AI诊室')"
    NAV_DOCTOR_WORKBENCH = "a:has-text('医生工作台')"
    NAV_HEALTH_EDUCATION = "a:has-text('患教文章')"
    NAV_MEDICAL_CASE = "a:has-text('医案分享')"
    NAV_QUESTIONNAIRE = "a:has-text('问诊单')"

    # ==================== 左侧菜单 ====================
    MENU_ONLINE_CONSULTATION = "text=在线问诊"
    MENU_STORE_VISIT = "text=门店出诊"
    MENU_ALL_PRESCRIPTIONS = "text=全部处方"
    MENU_COMMON_PRESCRIPTIONS = "text=常用方"
    MENU_CONSULTATION_LIST = "text=咨询列表"
    MENU_TODAY_SCAN = "text=今日扫码"
    MENU_ALL_PATIENTS = "text=全部患者"

    # 看诊数量徽章
    BADGE_PHONE_CONSULTATION = "text=电话看诊 >> nth=0 >> .."  # 主菜单第一个电话看诊项
    BADGE_VIDEO_CONSULTATION = "text=视频看诊 >> nth=0 >> .."  # 主菜单第一个视频看诊项

    # ==================== 患者搜索 ====================
    PATIENT_SEARCH_INPUT = "textbox:has-text('请输入患者名称搜索'), input[placeholder*='患者' i], input[placeholder*='搜索' i]"

    # ==================== 患者列表 ====================
    PATIENT_LIST = "#consultList"
    PATIENT_LIST_ITEM = "#consultList li"
    PATIENT_AVATAR = ".patient-avatar, img[src*='avatar']"
    PATIENT_NAME = ".name"
    PATIENT_TIME = ".patient-time, [class*='time']"

    # 患者状态标签
    STATUS_ENDED = "text=已结束"
    STATUS_FILLED_QUESTIONNAIRE = "text=填写问诊单"
    STATUS_QUESTIONNAIRE_PENDING = "text=共 *题"

    # ==================== 右侧操作区 ====================
    # 快捷回复
    BUTTON_QUICK_REPLY = "text=快捷回复"
    BUTTON_SEND_QUESTIONNAIRE = "text=发问诊单"

    # 在线开方
    BUTTON_ONLINE_PRESCRIBE = "text=在线开方"

    # 视频看诊（有二级菜单）
    BUTTON_VIDEO_CONSULTATION = "text=视频看诊"
    SUBMENU_VIDEO_CONSULTATION = "text=视频看诊"
    SUBMENU_AUDIO_CONSULTATION = "text=语音问诊"

    # 电话看诊（有二级菜单）
    BUTTON_PHONE_CONSULTATION = "text=电话看诊"
    SUBMENU_PHONE_CONSULTATION = "text=电话问诊"
    SUBMENU_AUDIO_CONSULTATION_PHONE = "text=语音问诊"

    # 结束问诊
    BUTTON_END_CONSULTATION = "text=结束问诊"

    # 消息输入区
    MESSAGE_INPUT = "textarea:has-text('请输入内容'), textarea[placeholder*='内容' i], [contenteditable='true']"
    BUTTON_SEND = "button:has-text('发送')"
    HINT_SEND_BY_ENTER = "text=回车发送/Ctrl+Enter换行"

    # ==================== 患者详情区 ====================
    PATIENT_INFO_PANEL = "text=电话:"
    PATIENT_DETAIL_NAME = ".name"
    PATIENT_GENDER = "text=男, text=女"
    PATIENT_AGE = "text=22岁, .patient-age"
    PATIENT_HEIGHT = ".patient-height"
    PATIENT_WEIGHT = ".patient-weight"
    PATIENT_WECHAT = "text=微信:"
    PATIENT_PHONE = "text=电话:"

    # ==================== 历史处方 ====================
    PRESCRIPTION_HISTORY = ".prescription-history, [class*='prescription-history']"
    PRESCRIPTION_ITEM = ".prescription-item, [class*='prescription-item']"
    PRESCRIPTION_DIAGNOSIS = "[class*='diagnosis']"
    PRESCRIPTION_PLAN = "[class*='plan']"
    PRESCRIPTION_STATUS = ".prescription-status, [class*='status']"

    # ==================== 问诊单 ====================
    QUESTIONNAIRE_CARD = ".questionnaire-card, [class*='questionnaire']"
    BUTTON_FILL_QUESTIONNAIRE = "text=填写问诊单, text=点击卡片填写问诊单"

    # ==================== 病历管理 ====================
    BUTTON_MEDICAL_RECORD = "text=病历管理"

    # ==================== 草稿箱 ====================
    DRAFT_BOX_HEADING = "heading:has-text('草稿箱')"
    DRAFT_COUNT_TEXT = "text=个"  # 数量后面的"个"文字
    DRAFT_ITEM = ".draft-item"

    # ==================== 开方弹窗/页面 ====================
    PRESCRIPTION_MODAL = ".dialog:has-text('请选择方案类型')"
    BUTTON_PRESCRIPTION_CLOSE = "button:has-text('Close'), button:has-text('关闭')"
    PRESCRIPTION_TYPE_HERBAL = "text=中药饮片"
    PRESCRIPTION_TYPE_GRANULE = "text=颗粒剂"
    PRESCRIPTION_TYPE_CUSTOM_PILL = "text=定制丸剂"
    PRESCRIPTION_TYPE_POWDER = "text=打粉散剂"
    PRESCRIPTION_TYPE_PASTE = "text=滋补膏方"
    PRESCRIPTION_TYPE_WESTERN = "text=中西成药"
    PRESCRIPTION_TYPE_EXPERIENCE = "text=经验方"
    PRESCRIPTION_TYPE_EXTERNAL = "text=外治项目"
    PRESCRIPTION_TYPE_HOSPITAL = "text=院内制剂"
    PRESCRIPTION_TYPE_SPECIAL = "text=特色剂型"
    LABEL_PRESCRIPTION_PENDING = "text=待发送"

    # ==================== 结束问诊确认弹窗 ====================
    END_CONSULTATION_DIALOG = ".dialog:has-text('结束本次咨询')"
    BUTTON_CONFIRM_END = "button:has-text('确认结束'), button:has-text('确认')"
    BUTTON_CANCEL_END = "button:has-text('取消'), button:has-text('关闭')"
    BUTTON_REFUND_END = "button:has-text('退号退款')"

    # ==================== 徽章数量 ====================
    VIDEO_CONSULTATION_BADGE = "text=视频看诊"
    PHONE_CONSULTATION_BADGE = "text=电话看诊"
    DRAFT_COUNT = "text=草稿箱 >> .."  # 草稿箱数量
    # 看诊数量数字
    VIDEO_CONSULTATION_COUNT = "text=视频看诊 >> .. >> :scope:text-is(/\\d+/)"
    PHONE_CONSULTATION_COUNT = "text=电话看诊 >> .. >> :scope:text-is(/\\d+/)"

    # ==================== 第一个患者姓名 ====================
    FIRST_PATIENT_NAME = "[class*='patient']:first-child"

    # ==================== 会话状态 ====================
    CONSULTATION_STATUS_ENDED = "text=已结束"
    CONSULTATION_STATUS_ONGOING = "text=进行中"

    # ==================== 通用定位器 ====================
    LOADING_SPINNER = ".loading, [class*='loading']"
    TOAST_MESSAGE = ".toast, .message, [class*='toast']"
    MODAL_OVERLAY = ".modal-overlay, [class*='modal-overlay']"

    # ==================== URL 匹配 ====================
    URL_PATTERN = "**/index.html#/home"
    URL_PATTERN_AI_CLINIC = "**/index.html#/aiHome"
