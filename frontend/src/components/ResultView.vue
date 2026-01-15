<template>
  <div v-if="result" class="result-container">
    <!-- 转换状态 -->
    <el-alert
      :type="result.success ? 'success' : 'error'"
      :title="result.message"
      :closable="false"
      style="margin-bottom: 20px"
    >
      <div v-if="result.errors.length > 0">
        <div v-for="(error, index) in result.errors" :key="index" class="error-item">
          {{ error }}
        </div>
      </div>
    </el-alert>

    <!-- 表信息概览 -->
    <el-card v-if="result.table_info" class="info-card" style="margin-bottom: 20px">
      <template #header>
        <div class="card-header">
          <el-icon><InfoFilled /></el-icon>
          <span>表信息</span>
        </div>
      </template>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="表名">
          {{ result.table_info.table_name }}
        </el-descriptions-item>
        <el-descriptions-item label="列数">
          {{ result.table_info.columns.length }}
        </el-descriptions-item>
        <el-descriptions-item label="表注释" :span="2">
          {{ result.table_info.comment || '无' }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- 转换后的DDL -->
    <el-card v-if="result.converted_ddl" class="result-card">
      <template #header>
        <div class="card-header">
          <el-icon><Document /></el-icon>
          <span>转换后的DDL</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="copyDDL">
              <el-icon><CopyDocument /></el-icon>
              复制
            </el-button>
            <el-button type="success" size="small" @click="downloadDDL">
              <el-icon><Download /></el-icon>
              下载
            </el-button>
          </div>
        </div>
      </template>
      <div class="code-container">
        <pre><code>{{ result.converted_ddl }}</code></pre>
      </div>
    </el-card>

    <!-- 同步配置文件 -->
    <el-card v-if="result.sync_config" class="result-card" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <el-icon><Setting /></el-icon>
          <span>{{ syncToolName }}同步配置</span>
          <div class="header-actions">
            <el-button type="primary" size="small" @click="copyConfig">
              <el-icon><CopyDocument /></el-icon>
              复制
            </el-button>
            <el-button type="success" size="small" @click="downloadConfig">
              <el-icon><Download /></el-icon>
              下载
            </el-button>
          </div>
        </div>
      </template>
      <div class="code-container">
        <pre><code>{{ result.sync_config }}</code></pre>
      </div>
    </el-card>

    <!-- 字段映射对比 -->
    <el-card v-if="result.table_info" class="result-card" style="margin-top: 20px">
      <template #header>
        <div class="card-header">
          <el-icon><Grid /></el-icon>
          <span>字段映射对比</span>
        </div>
      </template>
      <el-table :data="result.table_info.columns" border stripe>
        <el-table-column prop="name" label="字段名" width="150" />
        <el-table-column prop="source_type" label="源数据库类型" width="150" />
        <el-table-column prop="target_type" label="目标数据库类型" width="150" />
        <el-table-column prop="comment" label="注释" />
        <el-table-column label="主键" width="80" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.is_primary" type="success" size="small">是</el-tag>
            <span v-else>-</span>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  InfoFilled,
  Document,
  Setting,
  Grid,
  CopyDocument,
  Download
} from '@element-plus/icons-vue'
import type { ConvertResponse } from '@/types'

const props = defineProps<{
  result: ConvertResponse | null
  syncTool: 'datax' | 'seatunnel'
}>()

const syncToolName = computed(() => {
  return props.syncTool === 'datax' ? 'DataX' : 'SeaTunnel'
})

// 复制DDL
const copyDDL = () => {
  if (props.result?.converted_ddl) {
    navigator.clipboard.writeText(props.result.converted_ddl)
    ElMessage.success('DDL已复制到剪贴板')
  }
}

// 下载DDL
const downloadDDL = () => {
  if (props.result?.converted_ddl && props.result?.table_info) {
    const blob = new Blob([props.result.converted_ddl], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${props.result.table_info.table_name}.sql`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }
}

// 复制配置
const copyConfig = () => {
  if (props.result?.sync_config) {
    navigator.clipboard.writeText(props.result.sync_config)
    ElMessage.success('配置已复制到剪贴板')
  }
}

// 下载配置
const downloadConfig = () => {
  if (props.result?.sync_config && props.result?.table_info) {
    const ext = props.syncTool === 'datax' ? '.json' : '.conf'
    const blob = new Blob([props.result.sync_config], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `sync_${props.result.table_info.table_name}${ext}`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }
}
</script>

<style scoped>
.result-container {
  margin-top: 20px;
}

.info-card,
.result-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  align-items: center;
  font-weight: bold;
}

.header-icon {
  margin-right: 8px;
  font-size: 18px;
}

.header-actions {
  margin-left: auto;
  display: flex;
  gap: 8px;
}

.code-container {
  background-color: #f5f5f5;
  border-radius: 4px;
  padding: 16px;
  overflow-x: auto;
}

.code-container pre {
  margin: 0;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  line-height: 1.5;
  color: #333;
}

.error-item {
  color: #f56c6c;
  margin: 4px 0;
}
</style>
