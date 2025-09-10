<template>
  <div class="register-container">
    <div class="register-form">
      <h2>用户注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">用户名</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            placeholder="请输入用户名"
          />
        </div>
        
        <div class="form-group">
          <label for="real_name">真实姓名</label>
          <input
            id="real_name"
            v-model="form.real_name"
            type="text"
            required
            placeholder="请输入真实姓名"
          />
        </div>
        
        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            required
            placeholder="请输入邮箱"
          />
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            placeholder="请输入密码"
          />
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            required
            placeholder="请确认密码"
          />
        </div>
        
        <div class="form-group">
          <label for="role">用户角色</label>
          <select id="role" v-model="form.role" required>
            <option value="">请选择角色</option>
            <option value="student">学生</option>
            <option value="parent">家长</option>
            <option value="teacher">教师</option>
            <option value="institution">机构</option>
          </select>
        </div>
        
        <button type="submit" :disabled="loading" class="register-btn">
          {{ loading ? '注册中...' : '注册' }}
        </button>
      </form>
      
      <div class="login-link">
        已有账号？<router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

export default {
  name: 'Register',
  setup() {
    const router = useRouter()
    const userStore = useUserStore()
    
    const form = ref({
      username: '',
      real_name: '',
      email: '',
      password: '',
      confirmPassword: '',
      role: ''
    })
    
    const loading = ref(false)
    
    const handleRegister = async () => {
      if (form.value.password !== form.value.confirmPassword) {
        alert('两次输入的密码不一致')
        return
      }
      
      loading.value = true
      
      try {
        await userStore.register(form.value)
        alert('注册成功！')
        router.push('/login')
      } catch (error) {
        alert('注册失败：' + error.message)
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      loading,
      handleRegister
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.register-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.register-form h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007bff;
}

.register-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.register-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

.register-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 1rem;
  color: #666;
}

.login-link a {
  color: #007bff;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>