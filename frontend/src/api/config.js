import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 配置类型 API
export const configTypeApi = {
  list: (params) => api.get('/types/', { params }),
  get: (name) => api.get(`/types/${name}/`),
  create: (data) => api.post('/types/', data),
  update: (name, data) => api.put(`/types/${name}/`, data),
  delete: (name) => api.delete(`/types/${name}/`),
  instances: (name) => api.get(`/types/${name}/instances/`)
}

// 配置实例 API
export const configInstanceApi = {
  list: (params) => api.get('/instances/', { params }),
  get: (id) => api.get(`/instances/${id}/`),
  create: (data) => api.post('/instances/', data),
  update: (id, data) => api.put(`/instances/${id}/`, data),
  delete: (id) => api.delete(`/instances/${id}/`),
  versions: (id) => api.get(`/instances/${id}/versions/`),
  rollback: (id, version) => api.post(`/instances/${id}/rollback/`, { version }),
  content: (id, format) => api.get(`/instances/${id}/content/`, { params: { format } })
}

export default api
