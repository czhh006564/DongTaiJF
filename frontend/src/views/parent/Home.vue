<template>
  <div class="parent-home">
    <div class="welcome-section">
      <h1>家长中心</h1>
      <p>关注孩子学习，助力成长每一步</p>
    </div>
    
    <div class="children-overview">
      <h2>孩子概览</h2>
      <div class="children-grid">
        <div 
          v-for="child in children" 
          :key="child.id"
          class="child-card"
          @click="selectChild(child)"
          :class="{ active: selectedChild?.id === child.id }"
        >
          <div class="child-avatar">
            <img v-if="child.avatar" :src="child.avatar" alt="头像" />
            <div v-else class="default-avatar">{{ child.name.charAt(0) }}</div>
          </div>
          <div class="child-info">
            <h3>{{ child.name }}</h3>
            <p>{{ child.grade }} | {{ child.school }}</p>
            <div class="child-stats">
              <span class="stat-item">
                <span class="stat-icon">📚</span>
                <span>{{ child.todayExercises }}题</span>
              </span>
              <span class="stat-item">
                <span class="stat-icon">✅</span>
                <span>{{ child.todayAccuracy }}%</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="selectedChild" class="child-details">
      <!-- 今日学习情况 -->
      <div class="today-section">
        <h2>{{ selectedChild.name }} - 今日学习</h2>
        <div class="today-stats">
          <div class="stat-card">
            <div class="stat-icon">📝</div>
            <div class="stat-content">
              <h3>{{ selectedChild.todayExercises }}</h3>
              <p>完成练习</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">⏱️</div>
            <div class="stat-content">
              <h3>{{ formatTime(selectedChild.todayTime) }}</h3>
              <p>学习时长</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <h3>{{ selectedChild.todayAccuracy }}%</h3>
              <p>正确率</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon">🏆</div>
            <div class="stat-content">
              <h3>+{{ selectedChild.todayPoints }}</h3>
              <p>获得积分</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习进度 -->
      <div class="progress-section">
        <h2>学习进度</h2>
        <div class="progress-grid">
          <div 
            v-for="subject in selectedChild.subjects" 
            :key="subject.name"
            class="subject-progress"
          >
            <div class="subject-header">
              <h4>{{ subject.name }}</h4>
              <span class="progress-percent">{{ subject.progress }}%</span>
            </div>
            <div class="progress-bar">
              <div 
                class="progress-fill" 
                :style="{ width: `${subject.progress}%` }"
                :class="getProgressClass(subject.progress)"
              ></div>
            </div>
            <div class="subject-stats">
              <span>本周练习: {{ subject.weeklyExercises }}题</span>
              <span>平均正确率: {{ subject.averageAccuracy }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近活动 -->
      <div class="activity-section">
        <h2>最近活动</h2>
        <div class="activity-timeline">
          <div 
            v-for="activity in selectedChild.recentActivities" 
            :key="activity.id"
            class="activity-item"
          >
            <div class="activity-time">{{ activity.time }}</div>
            <div class="activity-content">
              <div class="activity-icon">{{ activity.icon }}</div>
              <div class="activity-info">
                <h4>{{ activity.title }}</h4>
                <p>{{ activity.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习建议 -->
      <div class="suggestions-section">
        <h2>学习建议</h2>
        <div class="suggestions-list">
          <div 
            v-for="suggestion in selectedChild.suggestions" 
            :key="suggestion.id"
            class="suggestion-item"
            :class="suggestion.priority"
          >
            <div class="suggestion-icon">{{ suggestion.icon }}</div>
            <div class="suggestion-content">
              <h4>{{ suggestion.title }}</h4>
              <p>{{ suggestion.description }}</p>
            </div>
            <div class="suggestion-actions">
              <button @click="applySuggestion(suggestion)" class="apply-btn">
                查看详情
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="no-selection">
      <div class="empty-state">
        <div class="empty-icon">👨‍👩‍👧‍👦</div>
        <h3>选择一个孩子查看详细信息</h3>
        <p>点击上方的孩子卡片来查看他们的学习情况</p>
      </div>
    </div>

    <!-- 快速操作 -->
    <div class="quick-actions">
      <h2>快速操作</h2>
      <div class="actions-grid">
        <router-link to="/parent/report" class="action-card">
          <div class="action-icon">📊</div>
          <h3>学习报告</h3>
          <p>查看详细的学习分析报告</p>
        </router-link>
        
        <router-link to="/parent/settings" class="action-card">
          <div class="action-icon">⚙️</div>
          <h3>学习设置</h3>
          <p>管理孩子的学习偏好和目标</p>
        </router-link>
        
        <div class="action-card" @click="contactTeacher">
          <div class="action-icon">👨‍🏫</div>
          <h3>联系老师</h3>
          <p>与孩子的老师进行沟通</p>
        </div>
        
        <div class="action-card" @click="viewSchedule">
          <div class="action-icon">📅</div>
          <h3>学习计划</h3>
          <p>查看和制定学习计划</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'ParentHome',
  setup() {
    const router = useRouter()
    
    const children = ref([])
    const selectedChild = ref(null)
    
    const loadChildren = async () => {
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        children.value = [
          {
            id: 1,
            name: '张小明',
            grade: '九年级',
            school: '示例中学',
            avatar: '',
            todayExercises: 15,
            todayTime: 3600, // 秒
            todayAccuracy: 87,
            todayPoints: 125,
            subjects: [
              {
                name: '数学',
                progress: 78,
                weeklyExercises: 45,
                averageAccuracy: 85
              },
              {
                name: '语文',
                progress: 82,
                weeklyExercises: 32,
                averageAccuracy: 90
              },
              {
                name: '英语',
                progress: 75,
                weeklyExercises: 38,
                averageAccuracy: 82
              },
              {
                name: '物理',
                progress: 70,
                weeklyExercises: 28,
                averageAccuracy: 78
              }
            ],
            recentActivities: [
              {
                id: 1,
                time: '14:30',
                icon: '📝',
                title: '完成数学练习',
                description: '完成了10道代数题目，正确率90%'
              },
              {
                id: 2,
                time: '13:15',
                icon: '🏆',
                title: '获得成就',
                description: '连续学习7天，获得"坚持不懈"徽章'
              },
              {
                id: 3,
                time: '10:45',
                icon: '📚',
                title: '开始学习',
                description: '开始今天的学习计划'
              }
            ],
            suggestions: [
              {
                id: 1,
                icon: '📐',
                title: '加强几何练习',
                description: '几何题目正确率较低，建议增加相关练习',
                priority: 'high'
              },
              {
                id: 2,
                icon: '⏰',
                title: '调整学习时间',
                description: '建议在下午3-5点进行数学练习，效果更佳',
                priority: 'medium'
              }
            ]
          },
          {
            id: 2,
            name: '张小红',
            grade: '六年级',
            school: '示例小学',
            avatar: '',
            todayExercises: 8,
            todayTime: 1800,
            todayAccuracy: 92,
            todayPoints: 85,
            subjects: [
              {
                name: '数学',
                progress: 85,
                weeklyExercises: 25,
                averageAccuracy: 92
              },
              {
                name: '语文',
                progress: 88,
                weeklyExercises: 20,
                averageAccuracy: 95
              },
              {
                name: '英语',
                progress: 80,
                weeklyExercises: 18,
                averageAccuracy: 88
              }
            ],
            recentActivities: [
              {
                id: 1,
                time: '16:00',
                icon: '📝',
                title: '完成语文练习',
                description: '完成了5道阅读理解题目'
              },
              {
                id: 2,
                time: '15:30',
                icon: '🎯',
                title: '达成目标',
                description: '完成了今日学习目标'
              }
            ],
            suggestions: [
              {
                id: 1,
                icon: '📖',
                title: '增加阅读量',
                description: '建议每天增加30分钟课外阅读',
                priority: 'medium'
              }
            ]
          }
        ]
        
        // 默认选择第一个孩子
        if (children.value.length > 0) {
          selectedChild.value = children.value[0]
        }
        
      } catch (error) {
        console.error('加载孩子信息失败:', error)
      }
    }
    
    const selectChild = (child) => {
      selectedChild.value = child
    }
    
    const formatTime = (seconds) => {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      if (hours > 0) {
        return `${hours}h ${minutes}m`
      }
      return `${minutes}m`
    }
    
    const getProgressClass = (progress) => {
      if (progress >= 90) return 'excellent'
      if (progress >= 80) return 'good'
      if (progress >= 70) return 'average'
      return 'poor'
    }
    
    const applySuggestion = (suggestion) => {
      alert(`查看建议详情: ${suggestion.title}`)
    }
    
    const contactTeacher = () => {
      alert('联系老师功能开发中...')
    }
    
    const viewSchedule = () => {
      alert('学习计划功能开发中...')
    }
    
    onMounted(() => {
      loadChildren()
    })
    
    return {
      children,
      selectedChild,
      selectChild,
      formatTime,
      getProgressClass,
      applySuggestion,
      contactTeacher,
      viewSchedule
    }
  }
}
</script>

<style scoped>
.parent-home {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-section {
  text-align: center;
  margin-bottom: 2rem;
  padding: 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
}

.welcome-section h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
}

.welcome-section p {
  margin: 0;
  opacity: 0.9;
}

.parent-home > div {
  margin-bottom: 2rem;
}

.parent-home h2 {
  margin-bottom: 1rem;
  color: #333;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

/* 孩子概览 */
.children-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.child-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.child-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.child-card.active {
  border-color: #007bff;
  background-color: #f8f9ff;
}

.child-card {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.child-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #007bff;
}

.child-avatar img {
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
  font-size: 1.5rem;
  font-weight: bold;
}

.child-info {
  flex: 1;
}

.child-info h3 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.child-info p {
  margin: 0 0 0.5rem 0;
  color: #666;
  font-size: 0.9rem;
}

.child-stats {
  display: flex;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.9rem;
  color: #666;
}

.stat-icon {
  font-size: 1rem;
}

/* 今日学习 */
.today-stats {
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

.stat-card .stat-icon {
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

/* 学习进度 */
.progress-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.subject-progress {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.subject-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.subject-header h4 {
  margin: 0;
  color: #333;
}

.progress-percent {
  font-weight: 500;
  color: #007bff;
}

.progress-bar {
  height: 8px;
  background-color: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 1rem;
}

.progress-fill {
  height: 100%;
  transition: width 0.3s ease;
}

.progress-fill.excellent {
  background-color: #28a745;
}

.progress-fill.good {
  background-color: #17a2b8;
}

.progress-fill.average {
  background-color: #ffc107;
}

.progress-fill.poor {
  background-color: #dc3545;
}

.subject-stats {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #666;
}

/* 活动时间线 */
.activity-timeline {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-bottom: 1px solid #eee;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-time {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
  min-width: 60px;
}

.activity-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex: 1;
}

.activity-icon {
  font-size: 1.5rem;
}

.activity-info h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.activity-info p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

/* 学习建议 */
.suggestions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.suggestion-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  border-left: 4px solid #007bff;
}

.suggestion-item.high {
  border-left-color: #dc3545;
}

.suggestion-item.medium {
  border-left-color: #ffc107;
}

.suggestion-icon {
  font-size: 2rem;
}

.suggestion-content {
  flex: 1;
}

.suggestion-content h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.suggestion-content p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.apply-btn {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.apply-btn:hover {
  background-color: #0056b3;
}

/* 空状态 */
.no-selection {
  background: white;
  padding: 3rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.empty-state {
  color: #666;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin-bottom: 0.5rem;
  color: #333;
}

/* 快速操作 */
.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.action-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
  cursor: pointer;
}

.action-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.action-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.action-card h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.action-card p {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .child-card {
    flex-direction: column;
    text-align: center;
  }
  
  .child-stats {
    justify-content: center;
  }
  
  .subject-stats {
    flex-direction: column;
    gap: 0.25rem;
  }
  
  .activity-item {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .suggestion-item {
    flex-direction: column;
    text-align: center;
  }
}
</style>