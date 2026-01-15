#!/usr/bin/env python3
"""
FastAPI应用入口
DDL转换与数据同步配置生成工具
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import settings
from app.core.logger import logger

app = FastAPI(
    title="DDL转换与数据同步配置生成工具",
    description="将源数据库DDL转换为Doris DDL，并生成DataX/SeaTunnel同步配置",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    """根路径健康检查"""
    return JSONResponse(
        status_code=200,
        content={
            "message": "DDL转换与数据同步配置生成工具 API",
            "version": "1.0.0",
            "status": "running",
            "docs": "/docs"
        }
    )


@app.get("/health")
async def health():
    """健康检查接口"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
