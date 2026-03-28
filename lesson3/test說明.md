# test.py 程式說明

## 概述

`test.py` 是一個 **Open WebUI Filter（過濾器）** 的範例程式。  
Filter 是 Open WebUI 的插件機制，允許開發者在 AI 處理訊息的前後插入自訂邏輯。

---

## 架構說明

```
Filter
├── Valves（全域設定）
├── UserValves（使用者設定）
├── __init__()（初始化）
├── inlet()（請求前處理）
└── outlet()（回應後處理）
```

---

## 類別與方法說明

### `Filter` 類別

過濾器的主體類別，Open WebUI 會自動載入並呼叫其中的鉤子方法。

---

### `Valves`（全域閥門設定）

由管理員配置的全域參數，使用 Pydantic `BaseModel` 定義。

| 欄位 | 預設值 | 說明 |
|------|--------|------|
| `priority` | `0` | 過濾器優先順序，數字越小越優先 |
| `max_turns` | `8` | 全域最大對話輪數上限 |

---

### `UserValves`（使用者閥門設定）

每位使用者可自行調整的個人參數。

| 欄位 | 預設值 | 說明 |
|------|--------|------|
| `max_turns` | `4` | 使用者個人最大對話輪數 |

---

### `__init__(self)`

初始化方法，建立 `Valves` 實例。

```python
self.valves = self.Valves()
```

> 若需要自訂檔案處理，可啟用 `self.file_handler = True`，  
> WebUI 將把檔案操作交由本類別處理。

---

### `inlet(self, body, __user__)` — 請求前處理

**觸發時機**：使用者訊息送往 AI **之前**。

**處理邏輯**：
1. 取得對話訊息列表 `messages`
2. 計算有效上限：`max_turns = min(使用者上限, 全域上限)`
3. 若訊息數量超過上限，拋出 `Exception` 阻止請求

```python
max_turns = min(__user__["valves"].max_turns, self.valves.max_turns)
if len(messages) > max_turns:
    raise Exception(f"已超過對話輪數限制。最大輪數：{max_turns}")
```

**參數**：
- `body`：OpenAI Chat API 格式的請求主體
- `__user__`：使用者資訊字典，包含 `role` 和 `valves`

**回傳**：處理後的 `body`（dict）

---

### `outlet(self, body, __user__)` — 回應後處理

**觸發時機**：AI 回應產生**之後**。

**處理邏輯**：目前僅印出除錯資訊，直接回傳原始回應。  
可在此加入日誌記錄、敏感資訊過濾、格式轉換等邏輯。

**參數**：
- `body`：AI 回應的主體內容
- `__user__`：使用者資訊字典

**回傳**：處理後的 `body`（dict）

---

## 資料流程圖

```
使用者輸入訊息
      │
      ▼
  inlet() ──── 超過輪數上限？ ──→ 拋出例外，中止請求
      │ 否
      ▼
   AI 處理
      │
      ▼
  outlet()
      │
      ▼
  回傳回應給使用者
```

---

## 對話輪數限制邏輯

系統採用「取最小值」策略，確保使用者無法繞過全域限制：

```
實際上限 = min(使用者設定上限, 管理員全域上限)
         = min(UserValves.max_turns, Valves.max_turns)
         = min(4, 8)
         = 4（預設情況）
```

---

## 相依套件

| 套件 | 用途 |
|------|------|
| `pydantic` | 資料驗證與設定管理 |
| `typing` | 型別提示（`Optional`） |
