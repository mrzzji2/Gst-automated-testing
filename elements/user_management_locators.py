"""
User Management Page Locators
用户管理页元素定位器
"""


class UserManagementLocators:
    """用户管理页元素定位器"""

    # 页面标题
    PAGE_TITLE = "h1:has-text('Users'), h1:has-text('User Management')"
    PAGE_HEADER = ".page-header"

    # 操作按钮
    ADD_USER_BUTTON = "button:has-text('Add User'), button:has-text('New User'), .add-user-button"
    IMPORT_USERS_BUTTON = "button:has-text('Import'), .import-button"
    EXPORT_USERS_BUTTON = "button:has-text('Export'), .export-button"
    BULK_ACTIONS_BUTTON = ".bulk-actions-button"
    DELETE_SELECTED_BUTTON = "button:has-text('Delete Selected')"

    # 搜索和筛选
    SEARCH_INPUT = ".search-input, input[placeholder*='search' i]"
    SEARCH_BUTTON = ".search-button"
    CLEAR_SEARCH_BUTTON = ".clear-search"
    FILTER_BUTTON = ".filter-button, button:has-text('Filter')"
    FILTER_DROPDOWN = ".filter-dropdown"

    # 筛选选项
    STATUS_FILTER = ".status-filter, select[name='status']"
    ROLE_FILTER = ".role-filter, select[name='role']"
    DATE_FILTER = ".date-filter, input[type='date']"

    # 用户表格
    USERS_TABLE = ".users-table, #users-table, table"
    TABLE_ROWS = "tbody tr"
    TABLE_HEADERS = "thead th"

    # 表格列
    CHECKBOX_COLUMN = "input[type='checkbox']"
    AVATAR_COLUMN = ".user-avatar, img[alt*='avatar' i]"
    NAME_COLUMN = ".user-name, td:nth-child(2)"
    EMAIL_COLUMN = ".user-email, td:nth-child(3)"
    ROLE_COLUMN = ".user-role, td:nth-child(4)"
    STATUS_COLUMN = ".user-status, td:nth-child(5)"
    ACTIONS_COLUMN = ".user-actions, td:last-child"

    # 状态标签
    STATUS_ACTIVE = ".status.active, .badge:has-text('Active')"
    STATUS_INACTIVE = ".status.inactive, .badge:has-text('Inactive')"
    STATUS_PENDING = ".status.pending, .badge:has-text('Pending')"
    STATUS_SUSPENDED = ".status.suspended, .badge:has-text('Suspended')"

    # 行操作按钮
    EDIT_USER_BUTTON = ".edit-user, button:has-text('Edit'), .action-edit"
    DELETE_USER_BUTTON = ".delete-user, button:has-text('Delete'), .action-delete"
    VIEW_USER_BUTTON = ".view-user, button:has-text('View'), .action-view"
    MORE_ACTIONS_BUTTON = ".more-actions, .action-more"

    # 分页
    PAGINATION = ".pagination"
    PREVIOUS_PAGE = ".page-item.previous, [aria-label='Previous']"
    NEXT_PAGE = ".page-item.next, [aria-label='Next']"
    PAGE_INFO = ".page-info, .pagination-info"
    PAGE_SIZE_SELECT = ".page-size-select, select[name='pageSize']"

    # 用户模态框
    USER_MODAL = ".user-modal, .modal, [role='dialog']"
    MODAL_TITLE = ".modal-title"
    MODAL_CLOSE = ".modal-close, button[aria-label='Close']"

    # 用户表单
    USERNAME_INPUT = "input[name='username'], #username"
    EMAIL_INPUT = "input[name='email'], #email"
    FIRST_NAME_INPUT = "input[name='firstName'], #firstName"
    LAST_NAME_INPUT = "input[name='lastName'], #lastName"
    ROLE_SELECT = "select[name='role'], #role"
    STATUS_SELECT = "select[name='status'], #status"
    PASSWORD_INPUT = "input[name='password'], #password"
    CONFIRM_PASSWORD_INPUT = "input[name='confirmPassword'], #confirmPassword"

    # 表单按钮
    SAVE_BUTTON = "button[type='submit'], button:has-text('Save')"
    CANCEL_BUTTON = "button:has-text('Cancel'), .cancel-button"

    # 表单验证
    ERROR_MESSAGE = ".error-message, .validation-error, .invalid-feedback"
    REQUIRED_FIELD = ".required, [required]"

    # 确认对话框
    CONFIRM_DIALOG = ".confirm-dialog, .delete-confirm-modal"
    CONFIRM_DELETE_BUTTON = "button:has-text('Confirm'), button:has-text('Delete')"
    CANCEL_DELETE_BUTTON = "button:has-text('Cancel')"

    # 通知
    SUCCESS_TOAST = ".toast.success, .notification.success"
    ERROR_TOAST = ".toast.error, .notification.error"

    # 空状态
    EMPTY_STATE = ".empty-state, .no-data"
    EMPTY_STATE_ICON = ".empty-state-icon"
    EMPTY_STATE_MESSAGE = ".empty-state-message"

    # 批量操作
    SELECT_ALL_CHECKBOX = "input[type='checkbox'].select-all, thead input[type='checkbox']"
    BULK_DELETE_BUTTON = ".bulk-delete"
    BULK_ACTIVATE_BUTTON = ".bulk-activate"
    BULK_DEACTIVATE_BUTTON = ".bulk-deactivate"

    # 角色标签
    ROLE_ADMIN = ".role.admin, .badge:has-text('Admin')"
    ROLE_USER = ".role.user, .badge:has-text('User')"
    ROLE_MODERATOR = ".role.moderator, .badge:has-text('Moderator')"
    ROLE_GUEST = ".role.guest, .badge:has-text('Guest')"
