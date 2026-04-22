# 登录状态缓存使用说明

## 功能说明

测试框架支持将登录状态保存到本地文件，之后的测试可以直接使用保存的登录状态，无需每次都执行登录操作。

**优点：**
- ✅ 节省测试时间（跳过登录和医生选择步骤）
- ✅ 减少服务器压力
- ✅ 提高测试稳定性

## 使用方法

### 方法一：首次运行测试自动生成

1. 首次运行测试时，如果不存在登录状态文件，会自动执行登录并保存状态：
   ```bash
   pytest tests/test_cases/test_online_consultation.py::TestOnlineConsultation::test_enter_online_consultation_page --headed
   ```

2. 登录状态会保存到：`tests/storage_state.json`

3. 之后运行测试时会自动使用保存的状态：
   ```bash
   pytest tests/test_cases/test_online_consultation.py -m P0 --headed
   ```

### 方法二：手动生成登录状态（推荐）

运行专门的脚本生成登录状态：

```bash
# 生成登录状态
python scripts/generate_login_state.py

# 验证已保存的登录状态
python scripts/generate_login_state.py --verify

# 删除已保存的登录状态（强制重新登录）
python scripts/generate_login_state.py --delete
```

## 配置

登录凭据在 `.env` 文件中配置：

```env
GST_USERNAME=17671792742
GST_PASSWORD=123456
GST_DOCTOR_NAME=罗慧
GST_BASE_URL=https://doc-online-test.gstyun.cn/webClinic
```

## 工作原理

1. **首次登录：**
   - 打开浏览器 → 输入账号密码 → 点击登录 → 选择医生 → 保存状态

2. **后续测试：**
   - 直接加载保存的状态 → 跳过登录步骤 → 直接进入主页面

3. **状态更新：**
   - 删除 `storage_state.json` 文件
   - 重新运行测试或生成脚本

## 文件位置

- 登录状态文件：`tests/storage_state.json`
- 生成脚本：`scripts/generate_login_state.py`

## 故障排除

### Q: 测试仍然要求登录？
A: 删除 `tests/storage_state.json` 文件，重新生成。

### Q: 登录状态过期？
A: 运行 `python scripts/generate_login_state.py` 重新生成。

### Q: 多个账号如何切换？
A: 修改 `.env` 文件中的 `GST_USERNAME`，然后重新生成登录状态。
