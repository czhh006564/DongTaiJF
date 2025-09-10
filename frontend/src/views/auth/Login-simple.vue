<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>精准动态教辅</h1>
        <p>个性化AI教育辅助平台</p>
      </div>
      
      <form class="login-form" @submit.prevent="handleLogin">
        <div class="form-group">
          <input
            v-model="loginForm.username"
            type="text"
            placeholder="请输入用户名"
            required
            class="form-input"
          />
        </div>
        
        <div class="form-group">
          <input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            required
            class="form-input"
            @keyup.enter="handleLogin"
          />
        </div>
        
        <div class="form-group">
          <button
            type="submit"
            :disabled="loading"
            class="login-button"
          >
            {{ loading ? '登录中...' : '登录' }}
          </button>
        </div>
      </form>
      
      <div class="login-footer">
        <span>还没有账号？</span>
        <router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 加载状态
const loading = ref(false)

// 处理登录
const handleLogin = async () => {
  if (!loginForm.username || !loginForm.password) {
    alert('请填写用户名和密码')
    return
  }
  
  try {
    loading.value = true
    
    const result = await userStore.login({
      username: loginForm.username,
      password: loginForm.password
    })
    
    if (result.success) {
      alert('登录成功')
      
      // 根据用户角色跳转到对应页面
      const userRole = result.data.user_info.role
      switch (userRole) {
        case 'student':
          router.push('/student/home')
          break
        case 'parent':
          router.push('/parent/home')
          break
        case 'teacher':
          router.push('/teacher/home')
          break
        case 'institution':
          router.push('/institution/home')
          break
        case 'super_admin':
          router.push('/admin/home')
          break
        default:
          router.push('/dashboard')
      }
    } else {
      alert(result.message || '登录失败')
    }
  } catch (error) {
    console.error('登录错误:', error)
    alert('登录失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-header h1 {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 8px;
}

.login-header p {
  color: #909399;
  font-size: 14px;
}

.login-form {
  width: 100%;
}

.form-group {
  margin-bottom: 24px;
}

.form-input {
  width: 100%;
  height: 48px;
  padding: 0 16px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #409eff;
}

.login-button {
  width: 100%;
  height: 48px;
  background-color: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover:not(:disabled) {
  background-color: #337ecc;
}

.login-button:disabled {
  background-color: #c0c4cc;
  cursor: not-allowed;
}

.login-footer {
  text-align: center;
  margin-top: 24px;
  color: #909399;
  font-size: 14px;
}

.login-footer a {
  color: #409eff;
  text-decoration: none;
  margin-left: 4px;
}

.login-footer a:hover {
  text-decoration: underline;
}

@media (max-width: 480px) {
  .login-card {
    padding: 24px;
  }
  
  .login-header h1 {
    font-size: 24px;
  }
}
</style>