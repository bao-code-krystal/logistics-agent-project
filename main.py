from fastapi import FastAPI
from pydantic import BaseModel
import os
from logistics_sdk import LogisticsFreightAgent

app = FastAPI()

# 从环境变量读取 API Key，默认使用你本地测试的 Key
DIFY_API_KEY = os.getenv("DIFY_API_KEY", "app-aduwXKMmRdtfnTQX1HodA8i5")
agent = LogisticsFreightAgent(api_key=DIFY_API_KEY)

class QueryRequest(BaseModel):
    query: str

@app.post("/calculate")
def calculate(request: QueryRequest):
    result = agent.calculate(request.query)
    return {"result": result}