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
      <button @click.prevent="goHome" class="nav-button home-btn" type="button">
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
      <button @click.prevent="handleLogout" class="nav-button logout-btn" type="button">
        <span>🚪</span>
        退出登录
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

export default {
  name: 'NavigationBarSafe',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    // 当前视图角色
    const currentViewRole = ref('')
    
    // 安全的用户信息获取
    const safeUserInfo = computed(() => {
      try {
        const info = userStore.userInfo
        return info && typeof info === 'object' ? info : null
      } catch (error) {
        console.warn('获取用户信息失败:', error)
        return null
      }
    })
    
    // 获取角色显示名称
    const getRoleDisplayName = (role) => {
      const roleMap = {
        'student': '学生',
        'parent': '家长', 
        'teacher': '教师',
        'institution': '机构管理员',
        'super_admin': '超级管理员'
      }
      return roleMap[role] || role || '未知'
    }
    
    // 返回首页
    const goHome = () => {
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
        
        router.push(targetPath).catch(error => {
          console.error('路由跳转失败:', error)
          window.location.href = targetPath
        })
      } catch (error) {
        console.error('导航错误:', error)
        window.location.href = '/dashboard'
      }
    }
    
    // 角色切换
    const switchRole = () => {
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
        
        router.push(targetPath).catch(error => {
          console.error('角色切换失败:', error)
          window.location.href = targetPath
        })
      } catch (error) {
        console.error('角色切换错误:', error)
        window.location.href = '/admin/home'
      }
    }
    
    // 退出登录
    const handleLogout = () => {
      try {
        console.log('开始退出登录...')
        
        userStore.logout()
        console.log('用户store logout完成')
        
        // 直接使用window.location进行跳转，避免路由问题
        window.location.href = '/login'
        
      } catch (error) {
        console.error('退出登录失败:', error)
        // 强制跳转
        window.location.href = '/login'
      }
    }
    
    // 初始化
    onMounted(() => {
      try {
        currentViewRole.value = safeUserInfo.value?.role || ''
      } catch (error) {
        console.warn('NavigationBar初始化警告:', error)
        currentViewRole.value = ''
      }
    })
    
    return {
      currentViewRole,
      safeUserInfo,
      getRoleDisplayName,
      goHome,
      switchRole,
      handleLogout
    }
  }
}
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
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.app-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.user-info {
  font-size: 14px;
  opacity: 0.9;
  background: rgba(255, 255, 255, 0.1);
  padding: 4px 12px;
  border-radius: 16px;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 12px;
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
  }
  
  .nav-button {
    font-size: 12px;
    padding: 6px 12px;
  }
}
</style>