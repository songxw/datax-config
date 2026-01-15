<template>
  <div class="app-container">
    <!-- 头部 -->
    <el-header class="app-header">
      <div class="header-content">
        <el-icon class="logo-icon"><DataBoard /></el-icon>
        <h1>DDL转换与数据同步配置生成工具</h1>
      </div>
    </el-header>

    <!-- 主要内容 -->
    <el-main class="app-main">
      <div class="main-content">
        <!-- 输入区域 -->
        <DDLInput
          @convert="handleConvert"
          @loading-change="handleLoadingChange"
          ref="ddlInputRef"
        />

        <!-- 结果展示 -->
        <ResultView
          v-if="convertResult"
          :result="convertResult"
          :sync-tool="syncTool"
        />
      </div>
    </el-main>

    <!-- 页脚 -->
    <el-footer class="app-footer">
      <p>DDL转换工具 - 支持MySQL/PostgreSQL/Oracle/SQLServer到Doris的DDL转换与同步配置生成</p>
    </el-footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElLoading } from 'element-plus'
import { DataBoard } from '@element-plus/icons-vue'
import DDLInput from '@/components/DDLInput.vue'
import ResultView from '@/components/ResultView.vue'
import type { ConvertRequest, ConvertResponse } from '@/types'
import { convertDDL } from '@/services/api'

const ddlInputRef = ref<InstanceType<typeof DDLInput>>()
const convertResult = ref<ConvertResponse | null>(null)
const syncTool = ref<'datax' | 'seatunnel'>('datax')

// 处理加载状态变化
const handleLoadingChange = (loading: boolean) => {
  // syncTool会在handleConvert中从request参数获取
}

// 处理转换
const handleConvert = async (request: ConvertRequest) => {
  syncTool.value = request.sync_tool

  try {
    const result = await convertDDL(request)
    convertResult.value = result

    if (result.success) {
      ElMessage.success('转换成功！')
    } else {
      ElMessage.error('转换失败，请检查DDL语句')
    }
  } catch (error: any) {
    ElMessage.error(`转换失败: ${error.message || '未知错误'}`)
    convertResult.value = {
      success: false,
      message: '转换失败',
      errors: [error.message || '未知错误']
    }
  } finally {
    ddlInputRef.value?.setLoading(false)
  }
}
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.app-header {
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  height: 70px !important;
  display: flex;
  align-items: center;
  padding: 0 20px;
}

.header-content {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  display: flex;
  align-items: center;
}

.logo-icon {
  font-size: 32px;
  margin-right: 16px;
}

.app-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.app-main {
  flex: 1;
  padding: 30px 20px;
}

.main-content {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}

.app-footer {
  background: rgba(0, 0, 0, 0.1);
  color: white;
  text-align: center;
  height: 60px !important;
  display: flex;
  align-items: center;
  justify-content: center;
}

.app-footer p {
  margin: 0;
  font-size: 14px;
}
</style>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>
