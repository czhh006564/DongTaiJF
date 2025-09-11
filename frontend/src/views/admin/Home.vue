<template>
  <div class="admin-home">
    <NavigationBar />
    <div class="welcome-section">
      <h1>系统管理中心</h1>
      <p>全面管理系统运行状态</p>
    </div>
    
    <div class="stats-overview">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <h3>{{ stats.totalUsers }}</h3>
          <p>总用户数</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">🏢</div>
        <div class="stat-content">
          <h3>{{ stats.totalInstitutions }}</h3>
          <p>机构数量</p>
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
        <div class="stat-icon">🤖</div>
        <div class="stat-content">
          <h3>{{ stats.aiCalls }}</h3>
          <p>AI调用次数</p>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>快速操作</h2>
      <div class="actions-grid">
        <router-link to="/admin/users" class="action-card">
          <div class="action-icon">👥</div>
          <h3>用户管理</h3>
          <p>管理系统用户</p>
        </router-link>
        
        <router-link to="/admin/ai-config" class="action-card">
          <div class="action-icon">🤖</div>
          <h3>AI配置</h3>
          <p>配置AI模型参数</p>
        </router-link>
        
        <router-link to="/admin/system" class="action-card">
          <div class="action-icon">⚙️</div>
          <h3>系统设置</h3>
          <p>系统参数配置</p>
        </router-link>
        
        <div class="action-card">
          <div class="action-icon">📊</div>
          <h3>数据统计</h3>
          <p>查看系统数据</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import NavigationBar from '@/components/NavigationBar.vue'

export default {
  name: 'AdminHome',
  components: {
    NavigationBar
  },
  setup() {
    const stats = ref({
      totalUsers: 0,
      totalInstitutions: 0,
      todayExercises: 0,
      aiCalls: 0
    })
    
    const loadStats = async () => {
      stats.value = {
        totalUsers: 1250,
        totalInstitutions: 15,
        todayExercises: 3500,
        aiCalls: 8900
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
.admin-home {
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