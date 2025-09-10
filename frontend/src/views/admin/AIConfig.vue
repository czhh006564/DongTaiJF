<template>
  <div class="admin-ai-config">
    <div class="config-header">
      <h1>AI模型配置</h1>
      <p>管理系统使用的AI模型和参数</p>
    </div>
    
    <div class="config-content">
      <!-- 默认模型设置 -->
      <div class="config-section">
        <h2>默认模型设置</h2>
        <div class="config-card">
          <div class="form-group">
            <label>默认AI模型</label>
            <select v-model="defaultConfig.model">
              <option value="tongyi">通义千问</option>
              <option value="deepseek">DeepSeek</option>
              <option value="gpt-3.5">GPT-3.5</option>
              <option value="gpt-4">GPT-4</option>
            </select>
          </div>
          
          <div class="form-group">
            <label>API端点</label>
            <input v-model="defaultConfig.apiEndpoint" type="url" placeholder="https://api.example.com" />
          </div>
          
          <div class="form-group">
            <label>API密钥</label>
            <input v-model="defaultConfig.apiKey" type="password" placeholder="输入API密钥" />
          </div>
          
          <div class="form-group">
            <label>最大Token数</label>
            <input v-model.number="defaultConfig.maxTokens" type="number" min="100" max="4000" />
          </div>
          
          <div class="form-group">
            <label>温度参数</label>
            <input v-model.number="defaultConfig.temperature" type="number" min="0" max="2" step="0.1" />
          </div>
          
          <div class="form-actions">
            <button @click="saveDefaultConfig" :disabled="saving" class="save-btn">
              {{ saving ? '保存中...' : '保存默认配置' }}
            </button>
            <button @click="testConnection" :disabled="testing" class="test-btn">
              {{ testing ? '测试中...' : '测试连接' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 模型列表 -->
      <div class="config-section">
        <h2>可用模型列表</h2>
        <div class="models-grid">
          <div 
            v-for="model in availableModels" 
            :key="model.id"
            class="model-card"
            :class="{ active: model.id === defaultConfig.model }"
          >
            <div class="model-header">
              <h3>{{ model.name }}</h3>
              <span class="model-status" :class="model.status">
                {{ model.status === 'active' ? '可用' : '不可用' }}
              </span>
            </div>
            
            <div class="model-info">
              <p><strong>提供商:</strong> {{ model.provider }}</p>
              <p><strong>类型:</strong> {{ model.type }}</p>
              <p><strong>最大Token:</strong> {{ model.maxTokens }}</p>
              <p><strong>费用:</strong> {{ model.pricing }}</p>
            </div>
            
            <div class="model-description">
              <p>{{ model.description }}</p>
            </div>
            
            <div class="model-actions">
              <button 
                @click="setAsDefault(model)" 
                :disabled="model.status !== 'active'"
                class="set-default-btn"
              >
                设为默认
              </button>
              <button 
                @click="configureModel(model)" 
                class="config-btn"
              >
                配置
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 使用统计 -->
      <div class="config-section">
        <h2>使用统计</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-content">
              <h3>{{ stats.totalCalls }}</h3>
              <p>总调用次数</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-content">
              <h3>¥{{ stats.totalCost }}</h3>
              <p>总费用</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">⚡</div>
            <div class="stat-content">
              <h3>{{ stats.avgResponseTime }}ms</h3>
              <p>平均响应时间</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <h3>{{ stats.successRate }}%</h3>
              <p>成功率</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 模型配置弹窗 -->
    <div v-if="showConfigModal" class="modal-overlay" @click="closeConfigModal">
      <div class="modal-content" @click.stop>
        <h3>配置 {{ selectedModel?.name }}</h3>
        <form @submit.prevent="saveModelConfig">
          <div class="form-group">
            <label>API端点</label>
            <input v-model="modelConfig.apiEndpoint" type="url" required />
          </div>
          <div class="form-group">
            <label>API密钥</label>
            <input v-model="modelConfig.apiKey" type="password" required />
          </div>
          <div class="form-group">
            <label>最大Token数</label>
            <input v-model.number="modelConfig.maxTokens" type="number" min="100" max="8000" />
          </div>
          <div class="modal-actions">
            <button type="submit" :disabled="savingModel" class="save-btn">
              {{ savingModel ? '保存中...' : '保存配置' }}
            </button>
            <button type="button" @click="closeConfigModal" class="cancel-btn">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'AdminAIConfig',
  setup() {
    const defaultConfig = ref({
      model: 'tongyi',
      apiEndpoint: '',
      apiKey: '',
      maxTokens: 2000,
      temperature: 0.7
    })
    
    const availableModels = ref([])
    const stats = ref({})
    const saving = ref(false)
    const testing = ref(false)
    const showConfigModal = ref(false)
    const selectedModel = ref(null)
    const modelConfig = ref({})
    const savingModel = ref(false)
    
    const loadConfig = async () => {
      // 模拟加载配置
      defaultConfig.value = {
        model: 'tongyi',
        apiEndpoint: 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation',
        apiKey: '****',
        maxTokens: 2000,
        temperature: 0.7
      }
      
      availableModels.value = [
        {
          id: 'tongyi',
          name: '通义千问',
          provider: '阿里云',
          type: '大语言模型',
          maxTokens: 6000,
          pricing: '¥0.008/1K tokens',
          description: '阿里云自研的大规模语言模型，支持中文对话和文本生成',
          status: 'active'
        },
        {
          id: 'deepseek',
          name: 'DeepSeek',
          provider: 'DeepSeek',
          type: '大语言模型',
          maxTokens: 4000,
          pricing: '¥0.001/1K tokens',
          description: '高性价比的大语言模型，适合大规模应用',
          status: 'active'
        },
        {
          id: 'gpt-3.5',
          name: 'GPT-3.5 Turbo',
          provider: 'OpenAI',
          type: '大语言模型',
          maxTokens: 4000,
          pricing: '¥0.015/1K tokens',
          description: 'OpenAI的经典模型，性能稳定可靠',
          status: 'inactive'
        },
        {
          id: 'gpt-4',
          name: 'GPT-4',
          provider: 'OpenAI',
          type: '大语言模型',
          maxTokens: 8000,
          pricing: '¥0.21/1K tokens',
          description: 'OpenAI最先进的模型，理解能力更强',
          status: 'inactive'
        }
      ]
      
      stats.value = {
        totalCalls: 8900,
        totalCost: 156.78,
        avgResponseTime: 1250,
        successRate: 98.5
      }
    }
    
    const saveDefaultConfig = async () => {
      saving.value = true
      try {
        // 模拟保存配置
        await new Promise(resolve => setTimeout(resolve, 1000))
        alert('默认配置保存成功！')
      } catch (error) {
        alert('保存失败：' + error.message)
      } finally {
        saving.value = false
      }
    }
    
    const testConnection = async () => {
      testing.value = true
      try {
        // 模拟测试连接
        await new Promise(resolve => setTimeout(resolve, 2000))
        alert('连接测试成功！')
      } catch (error) {
        alert('连接测试失败：' + error.message)
      } finally {
        testing.value = false
      }
    }
    
    const setAsDefault = (model) => {
      defaultConfig.value.model = model.id
      alert(`已将 ${model.name} 设为默认模型`)
    }
    
    const configureModel = (model) => {
      selectedModel.value = model
      modelConfig.value = {
        apiEndpoint: '',
        apiKey: '',
        maxTokens: model.maxTokens
      }
      showConfigModal.value = true
    }
    
    const closeConfigModal = () => {
      showConfigModal.value = false
      selectedModel.value = null
      modelConfig.value = {}
    }
    
    const saveModelConfig = async () => {
      savingModel.value = true
      try {
        // 模拟保存模型配置
        await new Promise(resolve => setTimeout(resolve, 1000))
        alert(`${selectedModel.value.name} 配置保存成功！`)
        closeConfigModal()
      } catch (error) {
        alert('保存失败：' + error.message)
      } finally {
        savingModel.value = false
      }
    }
    
    onMounted(() => {
      loadConfig()
    })
    
    return {
      defaultConfig,
      availableModels,
      stats,
      saving,
      testing,
      showConfigModal,
      selectedModel,
      modelConfig,
      savingModel,
      saveDefaultConfig,
      testConnection,
      setAsDefault,
      configureModel,
      closeConfigModal,
      saveModelConfig
    }
  }
}
</script>

<style scoped>
.admin-ai-config {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.config-header {
  text-align: center;
  margin-bottom: 2rem;
}

.config-header h1 {
  margin-bottom: 0.5rem;
  color: #333;
}

.config-header p {
  color: #666;
}

.config-section {
  margin-bottom: 3rem;
}

.config-section h2 {
  margin-bottom: 1rem;
  color: #333;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

.config-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1.5rem;
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
  max-width: 400px;
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

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.save-btn, .test-btn, .set-default-btn, .config-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.save-btn {
  background-color: #28a745;
  color: white;
}

.save-btn:hover:not(:disabled) {
  background-color: #218838;
}

.test-btn {
  background-color: #007bff;
  color: white;
}

.test-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

.save-btn:disabled, .test-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.models-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1rem;
}

.model-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
  transition: border-color 0.2s;
}

.model-card.active {
  border-color: #007bff;
}

.model-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.model-header h3 {
  margin: 0;
  color: #333;
}

.model-status {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.model-status.active {
  background-color: #d4edda;
  color: #155724;
}

.model-status.inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.model-info {
  margin-bottom: 1rem;
}

.model-info p {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.model-description {
  margin-bottom: 1rem;
}

.model-description p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
  line-height: 1.4;
}

.model-actions {
  display: flex;
  gap: 0.5rem;
}

.set-default-btn {
  background-color: #007bff;
  color: white;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
}

.set-default-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

.set-default-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.config-btn {
  background-color: #6c757d;
  color: white;
  font-size: 0.9rem;
  padding: 0.5rem 1rem;
}

.config-btn:hover {
  background-color: #545b62;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2rem;
}

.stat-content h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.stat-content p {
  margin: 0.25rem 0 0 0;
  color: #666;
  font-size: 0.9rem;
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
}

.modal-content h3 {
  margin: 0 0 1.5rem 0;
  color: #333;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.cancel-btn {
  padding: 0.75rem 1.5rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.cancel-btn:hover {
  background-color: #545b62;
}

@media (max-width: 768px) {
  .form-actions {
    flex-direction: column;
  }
  
  .model-actions {
    flex-direction: column;
  }
  
  .modal-actions {
    flex-direction: column;
  }
}
</style>