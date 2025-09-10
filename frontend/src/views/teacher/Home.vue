<template>
  <div class="teacher-home">
    <NavigationBar />
    <div class="welcome-section">
      <h1>教师工作台</h1>
      <p>管理班级，关注学生成长</p>
    </div>
    
    <div class="stats-overview">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3>{{ stats.totalStudents }}</h3>
          <p>管理学生</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📚</div>
        <div class="stat-content">
          <h3>{{ stats.totalClasses }}</h3>
          <p>授课班级</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📝</div>
        <div class="stat-content">
          <h3>{{ stats.todayExercises }}</h3>
          <p>今日练习</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">✅</div>
        <div class="stat-content">
          <h3>{{ stats.averageAccuracy }}%</h3>
          <p>班级平均正确率</p>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>快速操作</h2>
      <div class="actions-grid">
        <router-link to="/teacher/class" class="action-card">
          <div class="action-icon">🏫</div>
          <h3>班级管理</h3>
          <p>查看和管理班级信息</p>
        </router-link>
        
        <router-link to="/teacher/student" class="action-card">
          <div class="action-icon">👨‍🎓</div>
          <h3>学生管理</h3>
          <p>查看学生学习情况</p>
        </router-link>
        
        <div class="action-card" @click="createExercise">
          <div class="action-icon">📝</div>
          <h3>布置作业</h3>
          <p>为学生布置练习任务</p>
        </div>
        
        <div class="action-card" @click="viewReports">
          <div class="action-icon">📊</div>
          <h3>学习报告</h3>
          <p>查看班级学习分析</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import NavigationBar from '@/components/NavigationBar.vue'

export default {
  name: 'TeacherHome',
  components: {
    NavigationBar
  },
  setup() {
    const stats = ref({
      totalStudents: 0,
      totalClasses: 0,
      todayExercises: 0,
      averageAccuracy: 0
    })
    
    const loadStats = async () => {
      stats.value = {
        totalStudents: 45,
        totalClasses: 3,
        todayExercises: 128,
        averageAccuracy: 85
      }
    }
    
    const createExercise = () => {
      alert('布置作业功能开发中...')
    }
    
    const viewReports = () => {
      alert('学习报告功能开发中...')
    }
    
    onMounted(() => {
      loadStats()
    })
    
    return {
      stats,
      createExercise,
      viewReports
    }
  }
}
</script>

<style scoped>
.teacher-home {
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

.stats-overview {
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
</style>