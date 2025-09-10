<template>
  <div class="parent-settings">
    <h1>学习设置</h1>
    
    <div class="settings-content">
      <div class="child-selector">
        <label>选择孩子：</label>
        <select v-model="selectedChildId">
          <option value="">请选择孩子</option>
          <option v-for="child in children" :key="child.id" :value="child.id">
            {{ child.name }}
          </option>
        </select>
      </div>

      <div v-if="selectedChildId" class="settings-form">
        <div class="setting-section">
          <h3>学习目标</h3>
          <div class="form-group">
            <label>每日学习时长（分钟）</label>
            <input v-model.number="settings.dailyGoal" type="number" min="10" max="300" />
          </div>
          <div class="form-group">
            <label>每周练习次数</label>
            <input v-model.number="settings.weeklyTarget" type="number" min="1" max="7" />
          </div>
        </div>

        <div class="setting-section">
          <h3>学习偏好</h3>
          <div class="form-group">
            <label>难度设置</label>
            <select v-model="settings.difficulty">
              <option value="easy">简单</option>
              <option value="medium">中等</option>
              <option value="hard">困难</option>
              <option value="adaptive">自适应</option>
            </select>
          </div>
        </div>

        <div class="setting-section">
          <h3>提醒设置</h3>
          <div class="checkbox-group">
            <label class="checkbox-item">
              <input v-model="settings.notifications.daily" type="checkbox" />
              <span>每日学习提醒</span>
            </label>
            <label class="checkbox-item">
              <input v-model="settings.notifications.report" type="checkbox" />
              <span>周报告提醒</span>
            </label>
          </div>
        </div>

        <div class="form-actions">
          <button @click="saveSettings" class="save-btn">保存设置</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'ParentSettings',
  setup() {
    const children = ref([])
    const selectedChildId = ref('')
    const settings = ref({
      dailyGoal: 30,
      weeklyTarget: 5,
      difficulty: 'adaptive',
      notifications: {
        daily: true,
        report: true
      }
    })
    
    const loadChildren = async () => {
      children.value = [
        { id: 1, name: '张小明' },
        { id: 2, name: '张小红' }
      ]
    }
    
    const saveSettings = async () => {
      alert('设置保存成功！')
    }
    
    onMounted(() => {
      loadChildren()
    })
    
    return {
      children,
      selectedChildId,
      settings,
      saveSettings
    }
  }
}
</script>

<style scoped>
.parent-settings {
  padding: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}

.settings-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.child-selector {
  margin-bottom: 2rem;
}

.child-selector label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.child-selector select {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 200px;
}

.setting-section {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.setting-section:last-child {
  border-bottom: none;
}

.setting-section h3 {
  margin-bottom: 1rem;
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
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 200px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.checkbox-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-item input {
  width: auto;
}

.form-actions {
  margin-top: 2rem;
}

.save-btn {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.save-btn:hover {
  background-color: #0056b3;
}
</style>