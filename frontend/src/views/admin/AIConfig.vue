<template>
  <div class="ai-config">
    <NavigationBar />
    
    <div class="container">
      <div class="header">
        <h1>AI模型配置管理</h1>
        <p>管理系统中的AI模型配置和API密钥</p>
      </div>

      <!-- 当前模型状态 -->
      <div class="current-status">
        <h2>当前模型状态</h2>
        <div class="status-grid">
          <div class="status-card">
            <div class="status-icon">🤖</div>
            <div class="status-info">
              <h3>默认模型</h3>
              <p>{{ defaultModel?.display_name || '未设置' }}</p>
            </div>
          </div>
          <div class="status-card">
            <div class="status-icon">📊</div>
            <div class="status-info">
              <h3>总调用次数</h3>
              <p>{{ totalUsage.toLocaleString() }}</p>
            </div>
          </div>
          <div class="status-card">
            <div class="status-icon">⚡</div>
            <div class="status-info">
              <h3>活跃模型</h3>
              <p>{{ activeModels.length }} 个</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 模型配置列表 -->
      <div class="models-section">
        <div class="section-header">
          <h2>AI模型配置</h2>
          <button @click="showAddModal = true" class="btn-add">
            ➕ 添加模型
          </button>
        </div>

        <div class="models-list">
          <div 
            v-for="model in models" 
            :key="model.id"
            class="model-card"
            :class="{ 'default': model.is_default, 'inactive': !model.is_active }"
          >
            <div class="model-header">
              <div class="model-info">
                <h3>{{ model.display_name }}</h3>
                <span class="model-name">{{ model.model_name }}</span>
              </div>
              <div class="model-badges">
                <span v-if="model.is_default" class="badge default">默认</span>
                <span v-if="model.is_active" class="badge active">活跃</span>
                <span v-else class="badge inactive">停用</span>
              </div>
            </div>

            <div class="model-details">
              <div class="detail-item">
                <span class="label">API端点:</span>
                <span class="value">{{ model.api_endpoint }}</span>
              </div>
              <div class="detail-item">
                <span class="label">使用次数:</span>
                <span class="value">{{ model.usage_count.toLocaleString() }}</span>
              </div>
              <div class="detail-item">
                <span class="label">最后使用:</span>
                <span class="value">{{ formatDate(model.last_used) }}</span>
              </div>
            </div>

            <div class="model-actions">
              <button 
                @click="editModel(model)" 
                class="btn-edit"
                title="编辑配置"
              >
                ✏️ 编辑
              </button>
              <button 
                @click="toggleModelStatus(model)" 
                class="btn-toggle"
                :class="{ 'activate': !model.is_active, 'deactivate': model.is_active }"
                :title="model.is_active ? '停用模型' : '启用模型'"
              >
                {{ model.is_active ? '🔴 停用' : '🟢 启用' }}
              </button>
              <button 
                @click="setDefaultModel(model)" 
                class="btn-default"
                :disabled="model.is_default || !model.is_active"
                title="设为默认"
              >
                ⭐ 设为默认
              </button>
              <button 
                @click="testModel(model)" 
                class="btn-test"
                :disabled="!model.is_active || testingModel === model.id"
                title="测试连接"
              >
                {{ testingModel === model.id ? '⏳ 测试中' : '🧪 测试' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 使用统计 -->
      <div class="usage-stats">
        <h2>使用统计</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <h4>今日调用</h4>
            <p class="stat-number">{{ dailyStats.calls }}</p>
          </div>
          <div class="stat-item">
            <h4>本月调用</h4>
            <p class="stat-number">{{ monthlyStats.calls }}</p>
          </div>
          <div class="stat-item">
            <h4>成功率</h4>
            <p class="stat-number">{{ successRate }}%</p>
          </div>
          <div class="stat-item">
            <h4>平均响应时间</h4>
            <p class="stat-number">{{ avgResponseTime }}ms</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加/编辑模型弹窗 -->
    <div v-if="showAddModal || editingModel" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingModel ? '编辑模型配置' : '添加新模型' }}</h3>
          <button @click="closeModal" class="btn-close">✕</button>
        </div>

        <form @submit.prevent="saveModel" class="model-form">
          <div class="form-group">
            <label for="provider">模型提供商</label>
            <select 
              id="provider" 
              v-model="modelForm.provider" 
              @change="onProviderChange"
              required
            >
              <option value="">请选择模型提供商</option>
              <option value="tongyi">通义千问</option>
              <option value="deepseek">DeepSeek</option>
              <option value="openai">OpenAI</option>
              <option value="siliconflow">硅基流动</option>
            </select>
          </div>

          <div class="form-group" v-if="modelForm.provider">
            <label for="modelName">选择模型</label>
            <select 
              id="modelName" 
              v-model="modelForm.model_name" 
              @change="onModelChange"
              required
            >
              <option value="">请选择具体模型</option>
              <option 
                v-for="model in availableModels" 
                :key="model.value" 
                :value="model.value"
              >
                {{ model.label }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="displayName">显示名称</label>
            <input 
              type="text" 
              id="displayName" 
              v-model="modelForm.display_name" 
              placeholder="例如：通义千问"
              required
            >
          </div>

          <div class="form-group">
            <label for="apiEndpoint">API端点</label>
            <input 
              type="url" 
              id="apiEndpoint" 
              v-model="modelForm.api_endpoint" 
              placeholder="API端点将自动填充"
              required
              readonly
            >
          </div>

          <div class="form-group">
            <label for="apiKey">API密钥</label>
            <div class="api-key-input">
              <input 
                :type="showApiKey ? 'text' : 'password'" 
                id="apiKey" 
                v-model="modelForm.api_key" 
                placeholder="输入API密钥"
                required
              >
              <button 
                type="button" 
                @click="showApiKey = !showApiKey"
                class="btn-toggle-key"
              >
                {{ showApiKey ? '🙈' : '👁️' }}
              </button>
            </div>
          </div>

          <div class="form-group">
            <label for="maxTokens">最大Token数</label>
            <input 
              type="number" 
              id="maxTokens" 
              v-model.number="modelForm.max_tokens" 
              min="1" 
              max="32000"
              placeholder="2000"
            >
          </div>

          <div class="form-group">
            <label for="temperature">温度参数</label>
            <input 
              type="number" 
              id="temperature" 
              v-model.number="modelForm.temperature" 
              min="0" 
              max="2" 
              step="0.1"
              placeholder="0.7"
            >
          </div>

          <div class="form-checkboxes">
            <label class="checkbox-label">
              <input 
                type="checkbox" 
                v-model="modelForm.is_active"
              >
              <span class="checkmark"></span>
              启用此模型
            </label>

            <label class="checkbox-label">
              <input 
                type="checkbox" 
                v-model="modelForm.is_default"
                :disabled="!modelForm.is_active"
              >
              <span class="checkmark"></span>
              设为默认模型
            </label>
          </div>

          <div class="form-actions">
            <button type="button" @click="closeModal" class="btn-cancel">
              取消
            </button>
            <button 
              type="button" 
              @click="testConnection" 
              class="btn-test-connection"
              :class="{ 'testing': isTestingConnection, 'success': testResult === 'success', 'failed': testResult === 'failed' }"
              :disabled="!modelForm.api_endpoint || !modelForm.api_key || isTestingConnection"
            >
              <span v-if="isTestingConnection" class="loading-spinner">⏳</span>
              <span v-else-if="testResult === 'success'">✅</span>
              <span v-else-if="testResult === 'failed'">❌</span>
              <span v-else>🧪</span>
              {{ getTestButtonText() }}
            </button>
            <button type="submit" class="btn-save" :disabled="isSaving">
              {{ isSaving ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import NavigationBar from '@/components/NavigationBar.vue'
import api from '@/utils/api'

export default {
  name: 'AIConfig',
  components: {
    NavigationBar
  },
  setup() {
    // 数据状态
    const models = ref([])
    const showAddModal = ref(false)
    const editingModel = ref(null)
    const showApiKey = ref(false)
    const isSaving = ref(false)
    const testingModel = ref(null)
    const isTestingConnection = ref(false)
    const testResult = ref(null) // 'success', 'failed', null
    
    // 统计数据
    const dailyStats = ref({ calls: 0 })
    const monthlyStats = ref({ calls: 0 })
    const successRate = ref(0)
    const avgResponseTime = ref(0)
    
    // 模型提供商配置
    const providerConfigs = {
      tongyi: {
        name: '通义千问',
        endpoint: 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation',
        models: [
          { value: 'qwen-turbo', label: 'Qwen-Turbo (快速版)' },
          { value: 'qwen-plus', label: 'Qwen-Plus (增强版)' },
          { value: 'qwen-max', label: 'Qwen-Max (旗舰版)' },
          { value: 'qwen-max-longcontext', label: 'Qwen-Max-LongContext (长文本版)' }
        ]
      },
      deepseek: {
        name: 'DeepSeek',
        endpoint: 'https://api.deepseek.com/v1/chat/completions',
        models: [
          { value: 'deepseek-chat', label: 'DeepSeek Chat' },
          { value: 'deepseek-coder', label: 'DeepSeek Coder' }
        ]
      },
      openai: {
        name: 'OpenAI',
        endpoint: 'https://api.openai.com/v1/chat/completions',
        models: [
          { value: 'gpt-3.5-turbo', label: 'GPT-3.5 Turbo' },
          { value: 'gpt-4', label: 'GPT-4' },
          { value: 'gpt-4-turbo', label: 'GPT-4 Turbo' },
          { value: 'gpt-4o', label: 'GPT-4o' }
        ]
      },
      siliconflow: {
        name: '硅基流动',
        endpoint: 'https://api.siliconflow.cn/v1/chat/completions',
        models: [
          { value: 'Qwen/Qwen2-7B-Instruct', label: 'Qwen2-7B-Instruct' },
          { value: 'Qwen/Qwen2-72B-Instruct', label: 'Qwen2-72B-Instruct' },
          { value: 'deepseek-ai/DeepSeek-V2-Chat', label: 'DeepSeek-V2-Chat' },
          { value: 'meta-llama/Meta-Llama-3.1-8B-Instruct', label: 'Llama-3.1-8B-Instruct' },
          { value: 'meta-llama/Meta-Llama-3.1-70B-Instruct', label: 'Llama-3.1-70B-Instruct' }
        ]
      }
    }
    
    // 表单数据
    const modelForm = ref({
      provider: '',
      display_name: '',
      model_name: '',
      api_endpoint: '',
      api_key: '',
      max_tokens: 2000,
      temperature: 0.7,
      is_active: true,
      is_default: false
    })
    
    // 可用模型列表
    const availableModels = ref([])
    
    // 计算属性
    const defaultModel = computed(() => {
      return models.value.find(model => model.is_default)
    })
    
    const activeModels = computed(() => {
      return models.value.filter(model => model.is_active)
    })
    
    const totalUsage = computed(() => {
      return models.value.reduce((total, model) => total + (model.usage_count || 0), 0)
    })
    
    // 方法
    const loadModels = async () => {
      try {
        const response = await api.get('/api/admin/ai-models')
        models.value = response.data.models || []
      } catch (error) {
        console.error('加载模型配置失败:', error)
        // 使用模拟数据作为后备
        models.value = [
          {
            id: 1,
            display_name: "通义千问-Turbo",
            model_name: "qwen-turbo",
            api_endpoint: "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            usage_count: 1250,
            last_used: "2024-01-15T10:30:00",
            is_active: true,
            is_default: true,
            max_tokens: 2000,
            temperature: 0.7
          }
        ]
      }
    }
    
    const loadStats = async () => {
      try {
        const response = await api.get('/api/admin/ai-stats')
        const stats = response.data
        dailyStats.value = stats.daily || { calls: 0 }
        monthlyStats.value = stats.monthly || { calls: 0 }
        successRate.value = stats.success_rate || 0
        avgResponseTime.value = stats.avg_response_time || 0
      } catch (error) {
        console.error('加载统计数据失败:', error)
        // 使用模拟数据作为后备
        dailyStats.value = { calls: 156 }
        monthlyStats.value = { calls: 4520 }
        successRate.value = 98.5
        avgResponseTime.value = 850
      }
    }
    
    const editModel = (model) => {
      editingModel.value = model
      modelForm.value = {
        display_name: model.display_name,
        model_name: model.model_name,
        api_endpoint: model.api_endpoint,
        api_key: '', // 不显示现有密钥
        max_tokens: model.max_tokens || 2000,
        temperature: model.temperature || 0.7,
        is_active: model.is_active,
        is_default: model.is_default
      }
      showApiKey.value = false
    }
    
    const closeModal = () => {
      showAddModal.value = false
      editingModel.value = null
      resetForm()
    }
    
    const resetForm = () => {
      modelForm.value = {
        provider: '',
        display_name: '',
        model_name: '',
        api_endpoint: '',
        api_key: '',
        max_tokens: 2000,
        temperature: 0.7,
        is_active: true,
        is_default: false
      }
      availableModels.value = []
      showApiKey.value = false
    }
    
    // 处理提供商变化
    const onProviderChange = () => {
      const provider = modelForm.value.provider
      if (provider && providerConfigs[provider]) {
        const config = providerConfigs[provider]
        availableModels.value = config.models
        modelForm.value.api_endpoint = config.endpoint
        modelForm.value.display_name = config.name
        modelForm.value.model_name = ''
      } else {
        availableModels.value = []
        modelForm.value.api_endpoint = ''
        modelForm.value.display_name = ''
        modelForm.value.model_name = ''
      }
    }
    
    // 处理模型变化
    const onModelChange = () => {
      const selectedModel = availableModels.value.find(
        model => model.value === modelForm.value.model_name
      )
      if (selectedModel) {
        modelForm.value.display_name = selectedModel.label
      }
    }
    
    // 获取测试按钮文本
    const getTestButtonText = () => {
      if (isTestingConnection.value) {
        return '正在测试连通性...'
      } else if (testResult.value === 'success') {
        return '连通测试成功'
      } else if (testResult.value === 'failed') {
        return '连通测试失败'
      } else {
        return '连通测试'
      }
    }
    
    // 连通测试
    const testConnection = async () => {
      if (!modelForm.value.api_endpoint || !modelForm.value.api_key) {
        alert('请填写API端点和API密钥')
        return
      }
      
      if (!modelForm.value.provider || !modelForm.value.model_name) {
        alert('请先选择模型提供商和具体模型')
        return
      }
      
      // 重置测试结果并开始测试
      testResult.value = null
      isTestingConnection.value = true
      
      try {
        console.log('🔄 开始连通测试...', {
          provider: modelForm.value.provider,
          model_name: modelForm.value.model_name,
          api_endpoint: modelForm.value.api_endpoint
        })
        
        // 构造测试请求数据
        const testData = {
          provider: modelForm.value.provider,
          model_name: modelForm.value.model_name,
          api_endpoint: modelForm.value.api_endpoint,
          api_key: modelForm.value.api_key
        }
        
        const response = await api.post('/api/admin/ai-models/test-connection', testData)
        console.log('连通测试响应:', response.data)
        
        if (response.data.success) {
          testResult.value = 'success'
          alert(`✅ 连通测试成功！
响应时间: ${response.data.response_time}ms
模型响应: ${response.data.test_response || '正常'}`)
        } else {
          testResult.value = 'failed'
          alert(`❌ 连通测试失败: ${response.data.error}`)
        }
      } catch (error) {
        console.error('连通测试失败:', error)
        testResult.value = 'failed'
        const errorMsg = error.response?.data?.detail || error.response?.data?.message || error.message || '网络连接失败'
        alert(`❌ 连通测试失败: ${errorMsg}`)
      } finally {
        isTestingConnection.value = false
        
        // 3秒后重置按钮状态
        setTimeout(() => {
          testResult.value = null
        }, 3000)
      }
    }
    
    const saveModel = async () => {
      isSaving.value = true
      
      try {
        if (editingModel.value) {
          // 更新现有模型
          await api.put(`/api/admin/ai-models/${editingModel.value.id}`, modelForm.value)
        } else {
          // 创建新模型
          await api.post('/api/admin/ai-models', modelForm.value)
        }
        
        await loadModels()
        closeModal()
        alert(editingModel.value ? '模型配置更新成功' : '模型配置添加成功')
      } catch (error) {
        console.error('保存模型配置失败:', error)
        alert('保存失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        isSaving.value = false
      }
    }
    
    const toggleModelStatus = async (model) => {
      try {
        await api.patch(`/api/admin/ai-models/${model.id}/toggle`)
        await loadModels()
      } catch (error) {
        console.error('切换模型状态失败:', error)
        alert('操作失败')
      }
    }
    
    const setDefaultModel = async (model) => {
      try {
        await api.patch(`/api/admin/ai-models/${model.id}/set-default`)
        await loadModels()
      } catch (error) {
        console.error('设置默认模型失败:', error)
        alert('设置失败')
      }
    }
    
    const testModel = async (model) => {
      testingModel.value = model.id
      
      try {
        const response = await api.post(`/api/admin/ai-models/${model.id}/test`)
        if (response.data.success) {
          alert('模型测试成功！响应时间: ' + response.data.response_time + 'ms')
        } else {
          alert('模型测试失败: ' + response.data.error)
        }
      } catch (error) {
        console.error('测试模型失败:', error)
        alert('测试失败: ' + (error.response?.data?.detail || error.message))
      } finally {
        testingModel.value = null
      }
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return '从未使用'
      return new Date(dateString).toLocaleString('zh-CN')
    }
    
    // 生命周期
    onMounted(() => {
      loadModels()
      loadStats()
    })
    
    return {
      models,
      showAddModal,
      editingModel,
      showApiKey,
      isSaving,
      testingModel,
      isTestingConnection,
      testResult,
      dailyStats,
      monthlyStats,
      successRate,
      avgResponseTime,
      modelForm,
      availableModels,
      defaultModel,
      activeModels,
      totalUsage,
      editModel,
      closeModal,
      saveModel,
      toggleModelStatus,
      setDefaultModel,
      testModel,
      formatDate,
      onProviderChange,
      onModelChange,
      testConnection,
      getTestButtonText
    }
  }
}
</script>

<style scoped>
.ai-config {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.current-status {
  background: white;
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.current-status h2 {
  color: #333;
  margin-bottom: 20px;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.status-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
  border-left: 4px solid #667eea;
}

.status-icon {
  font-size: 2rem;
  margin-right: 15px;
}

.status-info h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 5px;
}

.status-info p {
  color: #666;
  margin: 0;
}

.models-section {
  background: white;
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.section-header h2 {
  color: #333;
  margin: 0;
}

.btn-add {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s;
}

.btn-add:hover {
  transform: translateY(-2px);
}

.models-list {
  display: grid;
  gap: 20px;
}

.model-card {
  border: 2px solid #e1e5e9;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s;
}

.model-card:hover {
  border-color: #667eea;
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

.model-card.default {
  border-color: #ffd700;
  background: linear-gradient(135deg, #fff9e6 0%, #fff3cd 100%);
}

.model-card.inactive {
  opacity: 0.6;
  background: #f8f9fa;
}

.model-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.model-info h3 {
  color: #333;
  margin-bottom: 5px;
}

.model-name {
  color: #666;
  font-family: monospace;
  background: #f1f3f4;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.9rem;
}

.model-badges {
  display: flex;
  gap: 8px;
}

.badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.badge.default {
  background: #ffd700;
  color: #b8860b;
}

.badge.active {
  background: #d4edda;
  color: #155724;
}

.badge.inactive {
  background: #f8d7da;
  color: #721c24;
}

.model-details {
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  margin-bottom: 8px;
}

.detail-item .label {
  font-weight: 600;
  color: #555;
  min-width: 100px;
}

.detail-item .value {
  color: #333;
  word-break: break-all;
}

.model-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.model-actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 15px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-edit {
  background: #17a2b8;
  color: white;
}

.btn-toggle.activate {
  background: #28a745;
  color: white;
}

.btn-toggle.deactivate {
  background: #dc3545;
  color: white;
}

.btn-default {
  background: #ffc107;
  color: #212529;
}

.btn-test {
  background: #6f42c1;
  color: white;
}

.model-actions button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
}

.model-actions button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.usage-stats {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.usage-stats h2 {
  color: #333;
  margin-bottom: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 10px;
}

.stat-item h4 {
  color: #666;
  margin-bottom: 10px;
  font-size: 0.9rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
  margin: 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 15px;
  padding: 0;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid #e1e5e9;
}

.modal-header h3 {
  color: #333;
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.model-form {
  padding: 25px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.api-key-input {
  position: relative;
}

.btn-toggle-key {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
}

.form-checkboxes {
  margin-bottom: 25px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  margin-right: 10px;
}

.form-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
}

.btn-cancel,
.btn-save,
.btn-test-connection {
  padding: 12px 25px;
  border: none;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-cancel {
  background: #6c757d;
  color: white;
}

.btn-save {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-test-connection {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.btn-test-connection.testing {
  background: linear-gradient(135deg, #17a2b8 0%, #138496 100%);
  animation: pulse 1.5s ease-in-out infinite;
}

.btn-test-connection.success {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  animation: success-flash 0.6s ease-in-out;
}

.btn-test-connection.failed {
  background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
  animation: error-shake 0.6s ease-in-out;
}

.loading-spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

@keyframes success-flash {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@keyframes error-shake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.btn-cancel:hover,
.btn-save:hover:not(:disabled),
.btn-test-connection:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.btn-save:disabled,
.btn-test-connection:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-group select {
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
  background: white;
}

.form-group select:focus {
  outline: none;
  border-color: #667eea;
}

@media (max-width: 768px) {
  .container {
    padding: 10px;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .section-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .model-actions {
    justify-content: center;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .modal-content {
    width: 95%;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>