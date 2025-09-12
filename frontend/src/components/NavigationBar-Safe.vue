<template>
  <div class="navigation-bar">
    <div class="nav-left">
      <h2 class="app-title">精准动态教辅</h2>
      <span class="user-info" v-if="safeUserInfo">
        {{ safeUserInfo.real_name || safeUserInfo.username }} ({{ getRoleDisplayName(safeUserInfo.role) }})
      </span>
    </div>
    
    <div class="nav-right">
      <!-- 返回首页 -->
      <button @click="goHome" class="nav-button home-btn" type="button">
        <span>🏠</span>
        返回首页
      </button>
      
      <!-- 角色切换 (仅超级管理员可见) -->
      <div v-if="safeUserInfo && safeUserInfo.role === 'super_admin'" class="role-switch">
        <select @change="switchRole" v-model="currentViewRole" class="role-select">
          <option value="super_admin">超级管理员视图</option>
          <option value="institution">机构管理员视图</option>
          <option value="teacher">教师视图</option>
          <option value="parent">家长视图</option>
          <option value="student">学生视图</option>
        </select>
      </div>
      
      <!-- 退出登录 -->
      <button @click="handleLogout" class="nav-button logout-btn" type="button">
        <span>🚪</span>
        退出登录
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 当前视图角色（用于超级管理员角色切换）
const currentViewRole = ref('')

// 安全的用户信息获取
const safeUserInfo = computed(() => {
  try {
    if (!userStore || typeof userStore.userInfo === 'undefined') {
      return null
    }
    return userStore.userInfo
  } catch (error) {
    console.warn('获取用户信息失败:', error)
    return null
  }
})

// 获取角色显示名称
const getRoleDisplayName = (role) => {
  if (!role) return '未知角色'
  
  const roleMap = {
    'student': '学生',
    'parent': '家长', 
    'teacher': '教师',
    'institution': '机构管理员',
    'super_admin': '超级管理员'
  }
  return roleMap[role] || role
}

// 安全的路由导航
const safeNavigate = async (path) => {
  try {
    if (!router) {
      window.location.href = path
      return
    }
    
    await nextTick()
    await router.push(path)
  } catch (error) {
    console.error('路由导航失败:', error)
    // 降级处理
    window.location.href = path
  }
}

// 返回首页
const goHome = async () => {
  try {
    const role = currentViewRole.value || safeUserInfo.value?.role
    let targetPath = '/dashboard'
    
    switch (role) {
      case 'student':
        targetPath = '/student/home'
        break
      case 'parent':
        targetPath = '/parent/home'
        break
      case 'teacher':
        targetPath = '/teacher/home'
        break
      case 'institution':
        targetPath = '/institution/home'
        break
      case 'super_admin':
        targetPath = '/admin/home'
        break
    }
    
    await safeNavigate(targetPath)
  } catch (error) {
    console.error('返回首页失败:', error)
    window.location.href = '/dashboard'
  }
}

// 角色切换（仅超级管理员）
const switchRole = async () => {
  try {
    const targetRole = currentViewRole.value
    let targetPath = '/admin/home'
    
    switch (targetRole) {
      case 'student':
        targetPath = '/student/home'
        break
      case 'parent':
        targetPath = '/parent/home'
        break
      case 'teacher':
        targetPath = '/teacher/home'
        break
      case 'institution':
        targetPath = '/institution/home'
        break
      case 'super_admin':
        targetPath = '/admin/home'
        break
    }
    
    await safeNavigate(targetPath)
  } catch (error) {
    console.error('角色切换失败:', error)
    window.location.href = '/admin/home'
  }
}

// 退出登录
const handleLogout = async () => {
  try {
    console.log('开始退出登录...')
    
    // 安全地执行退出登录
    if (userStore && typeof userStore.logout === 'function') {
      userStore.logout()
    }
    
    // 清除本地存储
    try {
      localStorage.clear()
      sessionStorage.clear()
    } catch (e) {
      console.warn('清除存储失败:', e)
    }
    
    // 强制跳转到登录页
    window.location.href = '/login'
    
  } catch (error) {
    console.error('退出登录失败:', error)
    // 即使出错也强制跳转
    window.location.href = '/login'
  }
}

// 安全的初始化
onMounted(async () => {
  try {
    await nextTick()
    
    // 等待一小段时间确保所有组件都已渲染
    setTimeout(() => {
      try {
        currentViewRole.value = safeUserInfo.value?.role || ''
      } catch (error) {
        console.warn('初始化角色失败:', error)
        currentViewRole.value = ''
      }
    }, 100)
    
  } catch (error) {
    console.warn('NavigationBar初始化失败:', error)
  }
})
</script>

<style scoped>
.navigation-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  min-height: 60px;
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.app-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  white-space: nowrap;
}

.user-info {
  font-size: 14px;
  opacity: 0.9;
  background: rgba(255, 255, 255, 0.1);
  padding: 4px 12px;
  border-radius: 16px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 200px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-shrink: 0;
}

.nav-button {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
  min-height: 36px;
}

.home-btn {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.home-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.logout-btn {
  background: rgba(220, 53, 69, 0.8);
  color: white;
}

.logout-btn:hover {
  background: rgba(220, 53, 69, 1);
}

.role-switch {
  margin: 0 8px;
}

.role-select {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.9);
  color: #333;
  font-size: 14px;
  cursor: pointer;
  min-width: 150px;
}

.role-select:focus {
  outline: none;
  background: white;
}

@media (max-width: 768px) {
  .navigation-bar {
    flex-direction: column;
    gap: 12px;
    padding: 16px;
    min-height: auto;
  }
  
  .nav-left, .nav-right {
    width: 100%;
    justify-content: center;
  }
  
  .app-title {
    font-size: 18px;
  }
  
  .user-info {
    font-size: 12px;
    max-width: none;
  }
  
  .nav-button {
    font-size: 12px;
    padding: 6px 12px;
  }
  
  .role-select {
    min-width: 120px;
  }
}

@media (max-width: 480px) {
  .nav-left {
    flex-direction: column;
    gap: 8px;
  }
  
  .nav-right {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .nav-button {
    flex: 1;
    min-width: 100px;
  }
}
</style>