<template>
  <div class="institution-home">
    <div class="welcome-section">
      <h1>机构管理中心</h1>
      <p>统筹管理，提升教学质量</p>
    </div>
    
    <div class="stats-overview">
      <div class="stat-card">
        <div class="stat-icon">👨‍🏫</div>
        <div class="stat-content">
          <h3>{{ stats.totalTeachers }}</h3>
          <p>教师总数</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3>{{ stats.totalStudents }}</h3>
          <p>学生总数</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🏫</div>
        <div class="stat-content">
          <h3>{{ stats.totalClasses }}</h3>
          <p>班级总数</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">📊</div>
        <div class="stat-content">
          <h3>{{ stats.averageScore }}%</h3>
          <p>平均成绩</p>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>快速操作</h2>
      <div class="actions-grid">
        <router-link to="/institution/teacher" class="action-card">
          <div class="action-icon">👨‍🏫</div>
          <h3>教师管理</h3>
          <p>管理机构内的教师</p>
        </router-link>
        
        <router-link to="/institution/report" class="action-card">
          <div class="action-icon">📊</div>
          <h3>教学报告</h3>
          <p>查看整体教学数据</p>
        </router-link>
        
        <div class="action-card">
          <div class="action-icon">⚙️</div>
          <h3>系统设置</h3>
          <p>配置机构相关设置</p>
        </div>
        
        <div class="action-card">
          <div class="action-icon">📈</div>
          <h3>数据分析</h3>
          <p>深度分析教学效果</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'InstitutionHome',
  setup() {
    const stats = ref({
      totalTeachers: 0,
      totalStudents: 0,
      totalClasses: 0,
      averageScore: 0
    })
    
    const loadStats = async () => {
      stats.value = {
        totalTeachers: 25,
        totalStudents: 450,
        totalClasses: 18,
        averageScore: 86
      }
    }
    
    onMounted(() => {
      loadStats()
    })
    
    return {
      stats
    }
  }
}
</script>

<style scoped>
.institution-home {
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