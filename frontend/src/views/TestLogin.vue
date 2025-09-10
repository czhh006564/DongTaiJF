<template>
  <div class="test-login">
    <h1>系统测试页面</h1>
    
    <div class="test-section">
      <h2>用户注册测试</h2>
      <form @submit.prevent="testRegister">
        <input v-model="registerForm.username" placeholder="用户名" required />
        <input v-model="registerForm.real_name" placeholder="真实姓名" required />
        <input v-model="registerForm.email" placeholder="邮箱" type="email" required />
        <input v-model="registerForm.password" placeholder="密码" type="password" required />
        <select v-model="registerForm.role" required>
          <option value="">选择角色</option>
          <option value="student">学生</option>
          <option value="parent">家长</option>
          <option value="teacher">教师</option>
        </select>
        <button type="submit" :disabled="loading">{{ loading ? '注册中...' : '测试注册' }}</button>
      </form>
      <div v-if="registerResult" class="result">
        注册结果: {{ registerResult }}
      </div>
    </div>

    <div class="test-section">
      <h2>用户登录测试</h2>
      <form @submit.prevent="testLogin">
        <input v-model="loginForm.username" placeholder="用户名" required />
        <input v-model="loginForm.password" placeholder="密码" type="password" required />
        <button type="submit" :disabled="loading">{{ loading ? '登录中...' : '测试登录' }}</button>
      </form>
      <div v-if="loginResult" class="result">
        登录结果: {{ loginResult }}
      </div>
    </div>

    <div class="test-section">
      <h2>API连接测试</h2>
      <button @click="testApiConnection" :disabled="loading">测试API连接</button>
      <div v-if="apiResult" class="result">
        API测试结果: {{ apiResult }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const loading = ref(false)
const registerResult = ref('')
const loginResult = ref('')
const apiResult = ref('')

const registerForm = ref({
  username: '',
  real_name: '',
  email: '',
  password: '',
  role: ''
})

const loginForm = ref({
  username: '',
  password: ''
})

const testRegister = async () => {
  loading.value = true
  registerResult.value = ''
  
  try {
    const response = await axios.post('/api/auth/register', registerForm.value)
    registerResult.value = `成功: ${JSON.stringify(response.data)}`
  } catch (error) {
    registerResult.value = `失败: ${error.response?.data?.detail || error.message}`
  } finally {
    loading.value = false
  }
}

const testLogin = async () => {
  loading.value = true
  loginResult.value = ''
  
  try {
    const response = await axios.post('/api/auth/login', loginForm.value)
    loginResult.value = `成功: ${JSON.stringify(response.data)}`
  } catch (error) {
    loginResult.value = `失败: ${error.response?.data?.detail || error.message}`
  } finally {
    loading.value = false
  }
}

const testApiConnection = async () => {
  loading.value = true
  apiResult.value = ''
  
  try {
    const response = await axios.get('/api/health')
    apiResult.value = `成功: ${JSON.stringify(response.data)}`
  } catch (error) {
    apiResult.value = `失败: ${error.response?.data?.detail || error.message}`
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.test-login {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.test-section {
  margin-bottom: 3rem;
  padding: 2rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.test-section h2 {
  margin-bottom: 1rem;
  color: #333;
}

.test-section form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1rem;
}

.test-section input,
.test-section select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.test-section button {
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.test-section button:hover:not(:disabled) {
  background-color: #0056b3;
}

.test-section button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.result {
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  word-break: break-all;
  font-family: monospace;
  font-size: 0.9rem;
}
</style>