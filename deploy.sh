#!/bin/bash

# DataX Config Generator 部署脚本
# 一键部署后端和前端服务

set -e

echo "🚀 开始部署 DataX Config Generator..."

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Python和Node.js
command -v python3 >/dev/null 2>&1 || { echo -e "${RED}❌ Python3 未安装${NC}"; exit 1; }
command -v node >/dev/null 2>&1 || { echo -e "${RED}❌ Node.js 未安装${NC}"; exit 1; }
command -v npm >/dev/null 2>&1 || { echo -e "${RED}❌ npm 未安装${NC}"; exit 1; }

echo -e "${GREEN}✅ 环境检查通过${NC}"

# 部署后端
echo -e "${YELLOW}📦 部署后端服务...${NC}"
cd backend

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建Python虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "安装Python依赖..."
pip install -r requirements.txt

# 启动后端服务（后台运行）
echo "启动后端服务..."
nohup python -m app.main > backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > backend.pid

echo -e "${GREEN}✅ 后端服务启动成功，PID: $BACKEND_PID${NC}"
echo -e "${GREEN}📝 后端日志: backend/backend.log${NC}"
cd ..

# 等待后端启动
sleep 3

# 部署前端
echo -e "${YELLOW}📦 部署前端服务...${NC}"
cd frontend

# 安装依赖
echo "安装npm依赖..."
npm install

# 构建前端（生产环境）
echo "构建前端应用..."
npm run build

# 启动前端服务（使用Vite预览，后台运行）
echo "启动前端服务..."
nohup npm run preview > frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > frontend.pid

echo -e "${GREEN}✅ 前端服务启动成功，PID: $FRONTEND_PID${NC}"
echo -e "${GREEN}📝 前端日志: frontend/frontend.log${NC}"
cd ..

echo -e "${GREEN}🎉 部署完成！${NC}"
echo -e "${GREEN}📱 前端地址: http://localhost:4173${NC}"
echo -e "${GREEN}🔧 后端地址: http://localhost:8000${NC}"
echo ""
echo -e "${YELLOW}📋 管理命令:${NC}"
echo "  查看后端状态: ps -p $(cat backend/backend.pid)"
echo "  查看前端状态: ps -p $(cat frontend/frontend.pid)"
echo "  停止后端: kill $(cat backend/backend.pid)"
echo "  停止前端: kill $(cat frontend/frontend.pid)"
echo ""
echo -e "${YELLOW}📝 日志查看:${NC}"
echo "  后端日志: tail -f backend/backend.log"
echo "  前端日志: tail -f frontend/frontend.log"