"""
title: Example Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1

這是一個 Open WebUI 的 Filter（過濾器）範例。
Filter 可以在訊息送入 AI 之前（inlet）或 AI 回應之後（outlet）進行攔截與處理。
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    """
    Filter 類別：Open WebUI 的過濾器主體。
    透過 inlet 和 outlet 兩個鉤子（hook）方法，
    分別在請求前與回應後對資料進行處理。
    """

    class Valves(BaseModel):
        """
        Valves（閥門）：管理員層級的全域設定。
        這些設定由系統管理員配置，對所有使用者生效。
        """
        priority: int = Field(
            default=0, description="過濾器操作的優先順序，數字越小優先級越高。"
        )
        max_turns: int = Field(
            default=8, description="全域最大對話輪數限制，管理員可調整。"
        )
        pass

    class UserValves(BaseModel):
        """
        UserValves（使用者閥門）：使用者層級的個人設定。
        每位使用者可以自行調整，但不能超過 Valves 的全域上限。
        """
        max_turns: int = Field(
            default=4, description="使用者個人的最大對話輪數限制。"
        )
        pass

    def __init__(self):
        """
        初始化 Filter 實例。
        建立 Valves 實例以管理全域設定。

        備註：若需要自訂檔案處理邏輯，可取消下方註解：
        self.file_handler = True
        啟用後，WebUI 會將檔案相關操作交由本類別的方法處理，
        而非使用預設的處理流程。
        """
        # self.file_handler = True  # 啟用自訂檔案處理（預設停用）

        # 初始化全域設定閥門
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        inlet（入口鉤子）：在請求送往 AI 之前執行的前處理方法。

        功能：
        - 驗證或修改請求內容（body）
        - 檢查對話輪數是否超過上限
        - 若超過限制則拋出例外，阻止請求繼續

        參數：
            body (dict): 包含對話訊息的請求主體，格式為 OpenAI Chat API 格式。
            __user__ (Optional[dict]): 當前使用者資訊，包含角色與個人設定。

        回傳：
            dict: 處理後的請求主體（可能已被修改）。
        """
        print(f"inlet:{__name__}")       # 印出模組名稱，用於除錯
        print(f"inlet:body:{body}")      # 印出請求主體內容
        print(f"inlet:user:{__user__}")  # 印出使用者資訊

        # 只對 "user" 和 "admin" 角色進行對話輪數檢查
        if __user__.get("role", "admin") in ["user", "admin"]:
            messages = body.get("messages", [])  # 取得對話訊息列表

            # 取使用者個人上限與全域上限的最小值，確保不超過任一限制
            max_turns = min(__user__["valves"].max_turns, self.valves.max_turns)

            # 若訊息數量超過最大輪數，拋出例外中止請求
            if len(messages) > max_turns:
                raise Exception(
                    f"已超過對話輪數限制。最大輪數：{max_turns}"
                )

        return body  # 回傳（可能已修改的）請求主體

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        outlet（出口鉤子）：在 AI 回應之後執行的後處理方法。

        功能：
        - 分析或修改 AI 的回應內容
        - 可用於記錄日誌、過濾敏感資訊或格式轉換

        參數：
            body (dict): AI 回應的主體內容。
            __user__ (Optional[dict]): 當前使用者資訊。

        回傳：
            dict: 處理後的回應主體（可能已被修改）。
        """
        print(f"outlet:{__name__}")       # 印出模組名稱，用於除錯
        print(f"outlet:body:{body}")      # 印出回應主體內容
        print(f"outlet:user:{__user__}")  # 印出使用者資訊

        return body  # 回傳（可能已修改的）回應主體
