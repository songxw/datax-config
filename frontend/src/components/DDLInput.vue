<template>
  <el-card class="ddl-input-card">
    <template #header>
      <div class="card-header">
        <el-icon class="header-icon"><Document /></el-icon>
        <span>DDL输入</span>
      </div>
    </template>

    <el-form :model="formData" label-width="100px" label-position="top">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="源数据库类型">
            <el-select v-model="formData.source_db_type" placeholder="请选择源数据库" style="width: 100%">
              <el-option
                v-for="db in supportedDB.source_databases"
                :key="db.value"
                :label="db.label"
                :value="db.value"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="目标数据库类型">
            <el-select v-model="formData.target_db_type" placeholder="请选择目标数据库" style="width: 100%">
              <el-option
                v-for="db in supportedDB.target_databases"
                :key="db.value"
                :label="db.label"
                :value="db.value"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item label="同步工具">
        <el-radio-group v-model="formData.sync_tool">
          <el-radio value="datax">DataX</el-radio>
          <el-radio value="seatunnel">SeaTunnel</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="源数据库DDL">
        <el-input
          v-model="formData.ddl"
          type="textarea"
          :rows="12"
          placeholder="请输入源数据库的DDL语句，例如：

CREATE TABLE users (
  id INT PRIMARY KEY,
  username VARCHAR(100) NOT NULL COMMENT '用户名',
  email VARCHAR(200) COMMENT '邮箱',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
) COMMENT='用户表';"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleConvert" :loading="loading" style="width: 100%">
          <el-icon><MagicStick /></el-icon>
          转换DDL并生成配置
        </el-button>
      </el-form-item>
    </el-form>
  </el-card>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, MagicStick } from '@element-plus/icons-vue'
import type { ConvertRequest, SourceDBType, TargetDBType, SyncToolType, SupportedDB } from '@/types'
import { getSupportedDB } from '@/services/api'

const emit = defineEmits<{
  convert: [request: ConvertRequest]
  loadingChange: [loading: boolean]
}>()

const loading = ref(false)
const supportedDB = reactive<SupportedDB>({
  source_databases: [],
  target_databases: [],
  sync_tools: []
})

const formData = reactive<ConvertRequest>({
  source_db_type: 'mysql' as SourceDBType,
  ddl: '',
  target_db_type: 'doris' as TargetDBType,
  sync_tool: 'datax' as SyncToolType
})

// 加载支持的数据库列表
onMounted(async () => {
  try {
    const data = await getSupportedDB()
    supportedDB.source_databases = data.source_databases
    supportedDB.target_databases = data.target_databases
    supportedDB.sync_tools = data.sync_tools
  } catch (error) {
    ElMessage.error('加载数据库列表失败')
  }
})

// 处理转换
const handleConvert = () => {
  if (!formData.ddl.trim()) {
    ElMessage.warning('请输入DDL语句')
    return
  }

  loading.value = true
  emit('loadingChange', true)
  emit('convert', { ...formData })
}

// 暴露方法给父组件
const setLoading = (val: boolean) => {
  loading.value = val
}

defineExpose({ setLoading })
</script>

<style scoped>
.ddl-input-card {
  margin-bottom: 20px;
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

:deep(.el-textarea__inner) {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
}
</style>
