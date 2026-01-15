// 数据库类型
export type SourceDBType = 'mysql' | 'postgresql' | 'oracle' | 'sqlserver'
export type TargetDBType = 'doris'
export type SyncToolType = 'datax' | 'seatunnel'

// 数据库选项
export interface DatabaseOption {
  value: string
  label: string
}

// 支持的数据库信息
export interface SupportedDB {
  source_databases: DatabaseOption[]
  target_databases: DatabaseOption[]
  sync_tools: DatabaseOption[]
}

// 列信息
export interface ColumnInfo {
  name: string
  source_type: string
  target_type: string
  comment?: string
  is_primary: boolean
}

// 表信息
export interface TableInfo {
  table_name: string
  columns: ColumnInfo[]
  comment?: string
}

// 转换请求
export interface ConvertRequest {
  source_db_type: SourceDBType
  ddl: string
  target_db_type: TargetDBType
  sync_tool: SyncToolType
}

// 转换响应
export interface ConvertResponse {
  success: boolean
  message: string
  converted_ddl?: string
  sync_config?: string
  table_info?: TableInfo
  errors: string[]
}
