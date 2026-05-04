import axios from 'axios'
import type {
  ConvertRequest,
  ConvertResponse,
  SupportedDB
} from '@/types'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    return Promise.reject(error)
  }
)

// 获取支持的数据库列表
export const getSupportedDB = async (): Promise<SupportedDB> => {
  const response = await api.get<SupportedDB>('/supported-db')
  return response as unknown as SupportedDB
}

// 转换DDL
export const convertDDL = async (request: ConvertRequest): Promise<ConvertResponse> => {
  const response = await api.post<ConvertResponse>('/convert', request)
  return response as unknown as ConvertResponse
}
