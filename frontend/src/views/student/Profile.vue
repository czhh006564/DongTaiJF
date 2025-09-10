<template>
  <div class="profile-container">
    <div class="profile-header">
      <h1>个人中心</h1>
    </div>

    <div class="profile-content">
      <!-- 基本信息 -->
      <div class="info-section">
        <h2>基本信息</h2>
        <div class="info-card">
          <div class="avatar-section">
            <div class="avatar">
              <img v-if="userInfo.avatar" :src="userInfo.avatar" alt="头像" />
              <div v-else class="default-avatar">{{ userInfo.username?.charAt(0)?.toUpperCase() }}</div>
            </div>
            <button @click="changeAvatar" class="change-avatar-btn">更换头像</button>
          </div>
          
          <div class="info-form">
            <div class="form-row">
              <div class="form-group">
                <label>用户名</label>
                <input v-model="userInfo.username" type="text" :disabled="!editing" />
              </div>
              <div class="form-group">
                <label>邮箱</label>
                <input v-model="userInfo.email" type="email" :disabled="!editing" />
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>真实姓名</label>
                <input v-model="userInfo.realName" type="text" :disabled="!editing" />
              </div>
              <div class="form-group">
                <label>年级</label>
                <select v-model="userInfo.grade" :disabled="!editing">
                  <option value="">请选择年级</option>
                  <option value="1">一年级</option>
                  <option value="2">二年级</option>
                  <option value="3">三年级</option>
                  <option value="4">四年级</option>
                  <option value="5">五年级</option>
                  <option value="6">六年级</option>
                  <option value="7">七年级</option>
                  <option value="8">八年级</option>
                  <option value="9">九年级</option>
                  <option value="10">高一</option>
                  <option value="11">高二</option>
                  <option value="12">高三</option>
                </select>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label>学校</label>
                <input v-model="userInfo.school" type="text" :disabled="!editing" />
              </div>
              <div class="form-group">
                <label>班级</label>
                <input v-model="userInfo.class" type="text" :disabled="!editing" />
              </div>
            </div>
            
            <div class="form-actions">
              <button v-if="!editing" @click="startEdit" class="edit-btn">编辑信息</button>
              <template v-else>
                <button @click="saveInfo" :disabled="saving" class="save-btn">
                  {{ saving ? '保存中...' : '保存' }}
                </button>
                <button @click="cancelEdit" class="cancel-btn">取消</button>
              </template>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习统计 -->
      <div class="stats-section">
        <h2>学习统计</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <div class="stat-icon">📚</div>
            <div class="stat-content">
              <h3>{{ stats.totalExercises }}</h3>
              <p>总练习数</p>
            </div>
          </div>
          
          <div class="stat-item">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <h3>{{ stats.correctRate }}%</h3>
              <p>正确率</p>
            </div>
          </div>
          
          <div class="stat-item">
            <div class="stat-icon">🏆</div>
            <div class="stat-content">
              <h3>{{ stats.totalPoints }}</h3>
              <p>总积分</p>
            </div>
          </div>
          
          <div class="stat-item">
            <div class="stat-icon">🎯</div>
            <div class="stat-content">
              <h3>{{ stats.streak }}</h3>
              <p>连续学习天数</p>
            </div>
          </div>
          
          <div class="stat-item">
            <div class="stat-icon">⏱️</div>
            <div class="stat-content">
              <h3>{{ formatTime(stats.totalTime) }}</h3>
              <p>学习时长</p>
            </div>
          </div>
          
          <div class="stat-item">
            <div class="stat-icon">📈</div>
            <div class="stat-content">
              <h3>{{ stats.level }}</h3>
              <p>当前等级</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 成就徽章 -->
      <div class="achievements-section">
        <h2>成就徽章</h2>
        <div class="achievements-grid">
          <div 
            v-for="achievement in achievements" 
            :key="achievement.id"
            class="achievement-item"
            :class="{ unlocked: achievement.unlocked }"
          >
            <div class="achievement-icon">{{ achievement.icon }}</div>
            <div class="achievement-info">
              <h4>{{ achievement.name }}</h4>
              <p>{{ achievement.description }}</p>
              <div v-if="achievement.unlocked" class="unlock-date">
                {{ achievement.unlockDate }}
              </div>
              <div v-else class="progress-info">
                进度: {{ achievement.progress }}/{{ achievement.target }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习偏好设置 -->
      <div class="preferences-section">
        <h2>学习偏好</h2>
        <div class="preferences-card">
          <div class="preference-item">
            <label>每日学习目标（分钟）</label>
            <input v-model.number="preferences.dailyGoal" type="number" min="10" max="300" />
          </div>
          
          <div class="preference-item">
            <label>难度偏好</label>
            <select v-model="preferences.difficulty">
              <option value="easy">简单</option>
              <option value="medium">中等</option>
              <option value="hard">困难</option>
              <option value="adaptive">自适应</option>
            </select>
          </div>
          
          <div class="preference-item">
            <label>提醒设置</label>
            <div class="checkbox-group">
              <label class="checkbox-item">
                <input v-model="preferences.notifications.daily" type="checkbox" />
                <span>每日学习提醒</span>
              </label>
              <label class="checkbox-item">
                <input v-model="preferences.notifications.achievement" type="checkbox" />
                <span>成就获得提醒</span>
              </label>
              <label class="checkbox-item">
                <input v-model="preferences.notifications.report" type="checkbox" />
                <span>学习报告提醒</span>
              </label>
            </div>
          </div>
          
          <div class="preference-actions">
            <button @click="savePreferences" :disabled="savingPreferences" class="save-btn">
              {{ savingPreferences ? '保存中...' : '保存设置' }}
            </button>
          </div>
        </div>
      </div>

      <!-- 账户安全 -->
      <div class="security-section">
        <h2>账户安全</h2>
        <div class="security-card">
          <div class="security-item">
            <div class="security-info">
              <h4>修改密码</h4>
              <p>定期修改密码以保护账户安全</p>
            </div>
            <button @click="changePassword" class="security-btn">修改密码</button>
          </div>
          
          <div class="security-item">
            <div class="security-info">
              <h4>登录记录</h4>
              <p>查看最近的登录活动</p>
            </div>
            <button @click="viewLoginHistory" class="security-btn">查看记录</button>
          </div>
          
          <div class="security-item">
            <div class="security-info">
              <h4>数据导出</h4>
              <p>导出你的学习数据</p>
            </div>
            <button @click="exportData" class="security-btn">导出数据</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 修改密码弹窗 -->
    <div v-if="showPasswordModal" class="modal-overlay" @click="closePasswordModal">
      <div class="modal-content" @click.stop>
        <h3>修改密码</h3>
        <form @submit.prevent="submitPasswordChange">
          <div class="form-group">
            <label>当前密码</label>
            <input v-model="passwordForm.current" type="password" required />
          </div>
          <div class="form-group">
            <label>新密码</label>
            <input v-model="passwordForm.new" type="password" required />
          </div>
          <div class="form-group">
            <label>确认新密码</label>
            <input v-model="passwordForm.confirm" type="password" required />
          </div>
          <div class="modal-actions">
            <button type="submit" :disabled="changingPassword" class="save-btn">
              {{ changingPassword ? '修改中...' : '确认修改' }}
            </button>
            <button type="button" @click="closePasswordModal" class="cancel-btn">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

export default {
  name: 'StudentProfile',
  setup() {
    const userStore = useUserStore()
    
    const userInfo = ref({
      username: '',
      email: '',
      realName: '',
      grade: '',
      school: '',
      class: '',
      avatar: ''
    })
    
    const originalUserInfo = ref({})
    const editing = ref(false)
    const saving = ref(false)
    
    const stats = ref({
      totalExercises: 0,
      correctRate: 0,
      totalPoints: 0,
      streak: 0,
      totalTime: 0,
      level: 0
    })
    
    const achievements = ref([])
    
    const preferences = ref({
      dailyGoal: 30,
      difficulty: 'adaptive',
      notifications: {
        daily: true,
        achievement: true,
        report: false
      }
    })
    
    const savingPreferences = ref(false)
    const showPasswordModal = ref(false)
    const changingPassword = ref(false)
    
    const passwordForm = ref({
      current: '',
      new: '',
      confirm: ''
    })
    
    const loadUserInfo = async () => {
      try {
        // 模拟API调用
        const mockUserInfo = {
          username: userStore.user?.username || 'student123',
          email: userStore.user?.email || 'student@example.com',
          realName: '张小明',
          grade: '9',
          school: '示例中学',
          class: '九年级三班',
          avatar: ''
        }
        
        userInfo.value = { ...mockUserInfo }
        originalUserInfo.value = { ...mockUserInfo }
        
      } catch (error) {
        console.error('加载用户信息失败:', error)
      }
    }
    
    const loadStats = async () => {
      try {
        stats.value = {
          totalExercises: 156,
          correctRate: 87,
          totalPoints: 1250,
          streak: 7,
          totalTime: 12600,
          level: 5
        }
      } catch (error) {
        console.error('加载统计数据失败:', error)
      }
    }
    
    const loadAchievements = async () => {
      try {
        achievements.value = [
          {
            id: 1,
            name: '初学者',
            description: '完成第一次练习',
            icon: '🎯',
            unlocked: true,
            unlockDate: '2024-01-10',
            progress: 1,
            target: 1
          },
          {
            id: 2,
            name: '坚持不懈',
            description: '连续学习7天',
            icon: '🔥',
            unlocked: true,
            unlockDate: '2024-01-15',
            progress: 7,
            target: 7
          },
          {
            id: 3,
            name: '百题达人',
            description: '完成100道练习题',
            icon: '💯',
            unlocked: true,
            unlockDate: '2024-01-20',
            progress: 156,
            target: 100
          },
          {
            id: 4,
            name: '完美主义者',
            description: '单次练习正确率达到100%',
            icon: '⭐',
            unlocked: false,
            progress: 95,
            target: 100
          },
          {
            id: 5,
            name: '学习狂人',
            description: '单日学习时长超过2小时',
            icon: '📚',
            unlocked: false,
            progress: 90,
            target: 120
          }
        ]
      } catch (error) {
        console.error('加载成就数据失败:', error)
      }
    }
    
    const formatTime = (seconds) => {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      return `${hours}h ${minutes}m`
    }
    
    const startEdit = () => {
      editing.value = true
    }
    
    const cancelEdit = () => {
      userInfo.value = { ...originalUserInfo.value }
      editing.value = false
    }
    
    const saveInfo = async () => {
      saving.value = true
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        originalUserInfo.value = { ...userInfo.value }
        editing.value = false
        alert('信息保存成功！')
        
      } catch (error) {
        alert('保存失败：' + error.message)
      } finally {
        saving.value = false
      }
    }
    
    const changeAvatar = () => {
      // 这里应该打开文件选择器
      alert('头像更换功能开发中...')
    }
    
    const savePreferences = async () => {
      savingPreferences.value = true
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        alert('设置保存成功！')
      } catch (error) {
        alert('保存失败：' + error.message)
      } finally {
        savingPreferences.value = false
      }
    }
    
    const changePassword = () => {
      showPasswordModal.value = true
    }
    
    const closePasswordModal = () => {
      showPasswordModal.value = false
      passwordForm.value = {
        current: '',
        new: '',
        confirm: ''
      }
    }
    
    const submitPasswordChange = async () => {
      if (passwordForm.value.new !== passwordForm.value.confirm) {
        alert('两次输入的新密码不一致')
        return
      }
      
      changingPassword.value = true
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        alert('密码修改成功！')
        closePasswordModal()
      } catch (error) {
        alert('密码修改失败：' + error.message)
      } finally {
        changingPassword.value = false
      }
    }
    
    const viewLoginHistory = () => {
      alert('登录记录功能开发中...')
    }
    
    const exportData = () => {
      alert('数据导出功能开发中...')
    }
    
    onMounted(() => {
      loadUserInfo()
      loadStats()
      loadAchievements()
    })
    
    return {
      userInfo,
      editing,
      saving,
      stats,
      achievements,
      preferences,
      savingPreferences,
      showPasswordModal,
      changingPassword,
      passwordForm,
      formatTime,
      startEdit,
      cancelEdit,
      saveInfo,
      changeAvatar,
      savePreferences,
      changePassword,
      closePasswordModal,
      submitPasswordChange,
      viewLoginHistory,
      exportData
    }
  }
}
</script>

<style scoped>
.profile-container {
  padding: 1.5rem;
  max-width: 1000px;
  margin: 0 auto;
}

.profile-header h1 {
  margin-bottom: 2rem;
  color: #333;
}

.profile-content > div {
  margin-bottom: 2rem;
}

.profile-content h2 {
  margin-bottom: 1rem;
  color: #333;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

/* 基本信息 */
.info-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  gap: 2rem;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #007bff;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.default-avatar {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #007bff;
  color: white;
  font-size: 2rem;
  font-weight: bold;
}

.change-avatar-btn {
  padding: 0.5rem 1rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.change-avatar-btn:hover {
  background-color: #545b62;
}

.info-form {
  flex: 1;
}

.form-row {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  flex: 1;
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

.form-group input:disabled,
.form-group select:disabled {
  background-color: #f8f9fa;
  color: #6c757d;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #007bff;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.edit-btn, .save-btn, .cancel-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.edit-btn {
  background-color: #007bff;
  color: white;
}

.save-btn {
  background-color: #28a745;
  color: white;
}

.cancel-btn {
  background-color: #6c757d;
  color: white;
}

.edit-btn:hover {
  background-color: #0056b3;
}

.save-btn:hover:not(:disabled) {
  background-color: #218838;
}

.cancel-btn:hover {
  background-color: #545b62;
}

.save-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 学习统计 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-item {
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

/* 成就徽章 */
.achievements-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.achievement-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.achievement-item.unlocked {
  opacity: 1;
}

.achievement-icon {
  font-size: 2.5rem;
}

.achievement-info h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.achievement-info p {
  margin: 0 0 0.5rem 0;
  color: #666;
  font-size: 0.9rem;
}

.unlock-date {
  font-size: 0.8rem;
  color: #28a745;
  font-weight: 500;
}

.progress-info {
  font-size: 0.8rem;
  color: #007bff;
  font-weight: 500;
}

/* 学习偏好 */
.preferences-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.preference-item {
  margin-bottom: 1.5rem;
}

.preference-item label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-weight: 500;
}

.preference-item input,
.preference-item select {
  width: 100%;
  max-width: 300px;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
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

.preference-actions {
  margin-top: 1.5rem;
}

/* 账户安全 */
.security-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid #eee;
}

.security-item:last-child {
  border-bottom: none;
}

.security-info h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.security-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.security-btn {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.security-btn:hover {
  background-color: #0056b3;
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
  max-width: 400px;
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

@media (max-width: 768px) {
  .info-card {
    flex-direction: column;
    align-items: center;
  }
  
  .form-row {
    flex-direction: column;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .security-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .modal-actions {
    flex-direction: column;
  }
}
</style>