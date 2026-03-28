from pydantic import BaseModel, Field
from typing import Optional


class Filter:

    class Valves(BaseModel):

        priority: int = Field(
            default=0, description="過濾器操作的優先順序，數字越小優先級越高。"
        )
        max_turns: int = Field(
            default=8, description="全域最大對話輪數限制，管理員可調整。"
        )
        pass

    class UserValves(BaseModel):

        max_turns: int = Field(default=4, description="使用者個人的最大對話輪數限制。")
        pass

    def __init__(self):
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        #print('使用者輸入:')
        #print(body.get("messages", [])[-1].get("content", "") if body.get("messages") else "")
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        messages = body.get("messages", [])
        user_input = ""
        assistant_output = ""
        for msg in reversed(messages):
            if msg.get("role") == "assistant" and not assistant_output:
                assistant_output = msg.get("content", "")
            elif msg.get("role") == "user" and not user_input:
                user_input = msg.get("content", "")
            if user_input and assistant_output:
                break
        print(f"使用者最後輸入: {user_input}")
        print(f"助理輸出: {assistant_output}")
        if messages and messages[-1].get("role") == "assistant":
            messages[-1]["content"] = "Hello!World!"
        body["messages"] = messages
          
        return body
