<template>
  <div class="student-home">
    <div class="welcome-section">
      <h1>欢迎回来，{{ userStore.user?.username }}！</h1>
      <p>今天也要努力学习哦～</p>
    </div>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">📚</div>
        <div class="stat-info">
          <h3>{{ stats.totalExercises }}</h3>
          <p>总练习题数</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <h3>{{ stats.correctRate }}%</h3>
          <p>正确率</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🏆</div>
        <div class="stat-info">
          <h3>{{ stats.points }}</h3>
          <p>积分</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🎯</div>
        <div class="stat-info">
          <h3>{{ stats.streak }}</h3>
          <p>连续学习天数</p>
        </div>
      </div>
    </div>
    
    <div class="quick-actions">
      <h2>快速开始</h2>
      <div class="action-grid">
        <router-link to="/student/exercise" class="action-card">
          <div class="action-icon">📝</div>
          <h3>开始练习</h3>
          <p>智能推荐练习题目</p>
        </router-link>
        
        <router-link to="/student/report" class="action-card">
          <div class="action-icon">📊</div>
          <h3>学习报告</h3>
          <p>查看详细学习分析</p>
        </router-link>
        
        <div class="action-card" @click="generateExercise">
          <div class="action-icon">🎲</div>
          <h3>随机练习</h3>
          <p>挑战随机题目</p>
        </div>
      </div>
    </div>
    
    <div class="recent-activities">
      <h2>最近活动</h2>
      <div class="activity-list">
        <div v-for="activity in recentActivities" :key="activity.id" class="activity-item">
          <div class="activity-icon">{{ activity.icon }}</div>
          <div class="activity-content">
            <h4>{{ activity.title }}</h4>
            <p>{{ activity.description }}</p>
            <span class="activity-time">{{ activity.time }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

export default {
  name: 'StudentHome',
  setup() {
    const userStore = useUserStore()
    
    const stats = ref({
      totalExercises: 0,
      correctRate: 0,
      points: 0,
      streak: 0
    })
    
    const recentActivities = ref([
      {
        id: 1,
        icon: '📝',
        title: '完成数学练习',
        description: '完成了10道代数题目，正确率90%',
        time: '2小时前'
      },
      {
        id: 2,
        icon: '🏆',
        title: '获得成就',
        description: '连续学习7天，获得"坚持不懈"徽章',
        time: '1天前'
      },
      {
        id: 3,
        icon: '📊',
        title: '查看报告',
        description: '查看了本周学习报告',
        time: '2天前'
      }
    ])
    
    const loadStats = async () => {
      try {
        // 这里应该调用API获取统计数据
        stats.value = {
          totalExercises: 156,
          correctRate: 85,
          points: 1250,
          streak: 7
        }
      } catch (error) {
        console.error('加载统计数据失败:', error)
      }
    }
    
    const generateExercise = () => {
      // 生成随机练习
      alert('正在生成随机练习题目...')
    }
    
    onMounted(() => {
      loadStats()
    })
    
    return {
      userStore,
      stats,
      recentActivities,
      generateExercise
    }
  }
}
</script>

<style scoped>
.student-home {
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
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

.stat-info h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.stat-info p {
  margin: 0.25rem 0 0 0;
  color: #666;
  font-size: 0.9rem;
}

.quick-actions {
  margin-bottom: 2rem;
}

.quick-actions h2 {
  margin-bottom: 1rem;
  color: #333;
}

.action-grid {
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

.recent-activities h2 {
  margin-bottom: 1rem;
  color: #333;
}

.activity-list {
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

.activity-icon {
  font-size: 1.5rem;
}

.activity-content {
  flex: 1;
}

.activity-content h4 {
  margin: 0 0 0.25rem 0;
  color: #333;
}

.activity-content p {
  margin: 0 0 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}

.activity-time {
  font-size: 0.8rem;
  color: #999;
}
</style>