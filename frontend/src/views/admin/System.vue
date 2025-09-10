<template>
  <div class="admin-system">
    <h1>系统设置</h1>
    
    <div class="system-content">
      <!-- 基本设置 -->
      <div class="setting-section">
        <h2>基本设置</h2>
        <div class="setting-card">
          <div class="form-group">
            <label>系统名称</label>
            <input v-model="systemConfig.name" type="text" />
          </div>
          
          <div class="form-group">
            <label>系统描述</label>
            <textarea v-model="systemConfig.description" rows="3"></textarea>
          </div>
          
          <div class="form-group">
            <label>系统版本</label>
            <input v-model="systemConfig.version" type="text" readonly />
          </div>
          
          <div class="form-group">
            <label>维护模式</label>
            <label class="switch">
              <input v-model="systemConfig.maintenanceMode" type="checkbox" />
              <span class="slider"></span>
            </label>
          </div>
        </div>
      </div>

      <!-- 安全设置 -->
      <div class="setting-section">
        <h2>安全设置</h2>
        <div class="setting-card">
          <div class="form-group">
            <label>密码最小长度</label>
            <input v-model.number="securityConfig.minPasswordLength" type="number" min="6" max="20" />
          </div>
          
          <div class="form-group">
            <label>登录失败锁定次数</label>
            <input v-model.number="securityConfig.maxLoginAttempts" type="number" min="3" max="10" />
          </div>
          
          <div class="form-group">
            <label>会话超时时间（分钟）</label>
            <input v-model.number="securityConfig.sessionTimeout" type="number" min="30" max="480" />
          </div>
        </div>
      </div>

      <!-- 邮件设置 -->
      <div class="setting-section">
        <h2>邮件设置</h2>
        <div class="setting-card">
          <div class="form-group">
            <label>SMTP服务器</label>
            <input v-model="emailConfig.smtpHost" type="text" />
          </div>
          
          <div class="form-group">
            <label>SMTP端口</label>
            <input v-model.number="emailConfig.smtpPort" type="number" />
          </div>
          
          <div class="form-group">
            <label>发件人邮箱</label>
            <input v-model="emailConfig.fromEmail" type="email" />
          </div>
          
          <div class="form-group">
            <label>邮箱密码</label>
            <input v-model="emailConfig.password" type="password" />
          </div>
        </div>
      </div>

      <!-- 存储设置 -->
      <div class="setting-section">
        <h2>存储设置</h2>
        <div class="setting-card">
          <div class="storage-info">
            <div class="storage-item">
              <span>数据库大小:</span>
              <span>{{ storageInfo.databaseSize }}</span>
            </div>
            <div class="storage-item">
              <span>文件存储:</span>
              <span>{{ storageInfo.fileStorage }}</span>
            </div>
            <div class="storage-item">
              <span>缓存大小:</span>
              <span>{{ storageInfo.cacheSize }}</span>
            </div>
          </div>
          
          <div class="storage-actions">
            <button @click="clearCache" class="action-btn">清理缓存</button>
            <button @click="backupDatabase" class="action-btn">备份数据库</button>
            <button @click="optimizeDatabase" class="action-btn">优化数据库</button>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button @click="saveSettings" :disabled="saving" class="save-btn">
          {{ saving ? '保存中...' : '保存所有设置' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'AdminSystem',
  setup() {
    const systemConfig = ref({
      name: '',
      description: '',
      version: '',
      maintenanceMode: false
    })
    
    const securityConfig = ref({
      minPasswordLength: 8,
      maxLoginAttempts: 5,
      sessionTimeout: 120
    })
    
    const emailConfig = ref({
      smtpHost: '',
      smtpPort: 587,
      fromEmail: '',
      password: ''
    })
    
    const storageInfo = ref({
      databaseSize: '',
      fileStorage: '',
      cacheSize: ''
    })
    
    const saving = ref(false)
    
    const loadSettings = async () => {
      // 模拟加载设置
      systemConfig.value = {
        name: '精准动态教辅系统',
        description: '基于AI的智能教学辅助平台',
        version: '1.0.0',
        maintenanceMode: false
      }
      
      storageInfo.value = {
        databaseSize: '256 MB',
        fileStorage: '1.2 GB',
        cacheSize: '45 MB'
      }
    }
    
    const saveSettings = async () => {
      saving.value = true
      try {
        // 模拟保存设置
        await new Promise(resolve => setTimeout(resolve, 1000))
        alert('设置保存成功！')
      } catch (error) {
        alert('保存失败：' + error.message)
      } finally {
        saving.value = false
      }
    }
    
    const clearCache = async () => {
      if (confirm('确定要清理缓存吗？')) {
        alert('缓存清理完成！')
      }
    }
    
    const backupDatabase = async () => {
      alert('数据库备份已开始，请稍候...')
    }
    
    const optimizeDatabase = async () => {
      if (confirm('确定要优化数据库吗？此操作可能需要一些时间。')) {
        alert('数据库优化已开始...')
      }
    }
    
    onMounted(() => {
      loadSettings()
    })
    
    return {
      systemConfig,
      securityConfig,
      emailConfig,
      storageInfo,
      saving,
      saveSettings,
      clearCache,
      backupDatabase,
      optimizeDatabase
    }
  }
}
</script>

<style scoped>
.admin-system {
  padding: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}

.system-content > div {
  margin-bottom: 2rem;
}

.setting-section h2 {
  margin-bottom: 1rem;
  color: #333;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

.setting-card {
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
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #007bff;
}

/* 开关样式 */
.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: .4s;
  border-radius: 34px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .slider {
  background-color: #007bff;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.storage-info {
  margin-bottom: 1.5rem;
}

.storage-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.storage-item:last-child {
  border-bottom: none;
}

.storage-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.5rem 1rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.action-btn:hover {
  background-color: #545b62;
}

.form-actions {
  text-align: center;
  margin-top: 2rem;
}

.save-btn {
  padding: 0.75rem 2rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.save-btn:hover:not(:disabled) {
  background-color: #218838;
}

.save-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .storage-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style>