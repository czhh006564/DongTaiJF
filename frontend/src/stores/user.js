import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))
  
  // 计算属性
  const isLoggedIn = computed(() => !!token.value && !!userInfo.value)
  const userRole = computed(() => userInfo.value?.role || '')
  
  // 方法
  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
    // 设置API默认请求头
    api.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
  }
  
  const setUserInfo = (info) => {
    userInfo.value = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  }
  
  const login = async (credentials) => {
    try {
      const response = await api.post('/auth/login', credentials)
      console.log('登录响应:', response.data)
      
      // 兼容不同的响应格式
      const { access_token, user_info, user } = response.data
      const userInfoData = user_info || user
      
      if (access_token && userInfoData) {
        setToken(access_token)
        setUserInfo(userInfoData)
        return { success: true, data: response.data }
      } else {
        throw new Error('响应数据格式错误')
      }
    } catch (error) {
      console.error('登录错误:', error)
      return { 
        success: false, 
        message: error.response?.data?.detail || error.message || '登录失败' 
      }
    }
  }
  
  const register = async (userData) => {
    try {
      const response = await api.post('/auth/register', userData)
      return { success: true, data: response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || '注册失败' 
      }
    }
  }
  
  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
    delete api.defaults.headers.common['Authorization']
  }
  
  const updateProfile = async (profileData) => {
    try {
      const response = await api.put(`/user/profile`, profileData)
      // 更新本地用户信息
      const updatedInfo = { ...userInfo.value, ...profileData }
      setUserInfo(updatedInfo)
      return { success: true, data: response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || '更新失败' 
      }
    }
  }
  
  const changePassword = async (passwordData) => {
    try {
      const response = await api.post('/auth/change-password', passwordData)
      return { success: true, data: response.data }
    } catch (error) {
      return { 
        success: false, 
        message: error.response?.data?.detail || '密码修改失败' 
      }
    }
  }
  
  const hasRole = (roles) => {
    if (!Array.isArray(roles)) {
      roles = [roles]
    }
    return roles.includes(userRole.value)
  }
  
  const getCurrentUser = async () => {
    try {
      const response = await api.get('/auth/me')
      setUserInfo(response.data)
      return { success: true, data: response.data }
    } catch (error) {
      // Token可能已过期，清除本地数据
      logout()
      return { 
        success: false, 
        message: error.response?.data?.detail || '获取用户信息失败' 
      }
    }
  }
  
  // 初始化时设置请求头
  if (token.value) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token.value}`
  }
  
  return {
    // 状态
    token,
    userInfo,
    
    // 计算属性
    isLoggedIn,
    userRole,
    
    // 方法
    setToken,
    setUserInfo,
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    hasRole,
    getCurrentUser
  }
})