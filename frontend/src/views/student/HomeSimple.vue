<template>
  <div class="student-home">
    <NavigationBar />
    
    <div class="container">
      <div class="welcome-section">
        <h1>学生学习中心</h1>
        <p>开始您的学习之旅</p>
      </div>
      
      <div class="quick-actions">
        <h2>快速开始</h2>
        <div class="action-grid">
          <router-link to="/student/generator" class="action-card">
            <div class="action-icon">🤖</div>
            <h3>AI题目生成</h3>
            <p>智能生成个性化练习题</p>
          </router-link>
          
          <router-link to="/student/exercise" class="action-card">
            <div class="action-icon">📝</div>
            <h3>开始练习</h3>
            <p>继续您的学习练习</p>
          </router-link>
          
          <router-link to="/student/report" class="action-card">
            <div class="action-icon">📊</div>
            <h3>学习报告</h3>
            <p>查看学习进度和分析</p>
          </router-link>
          
          <div class="action-card" @click="showComingSoon">
            <div class="action-icon">🎯</div>
            <h3>错题本</h3>
            <p>复习错题，巩固知识</p>
          </div>
        </div>
      </div>
      
      <div class="features-section">
        <h2>功能特色</h2>
        <div class="features-grid">
          <div class="feature-item">
            <div class="feature-icon">🎲</div>
            <h4>智能出题</h4>
            <p>AI根据您的学习情况生成个性化题目</p>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">📄</div>
            <h4>PDF导出</h4>
            <p>将练习题导出为PDF，随时随地学习</p>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">💡</div>
            <h4>智能解析</h4>
            <p>详细的答案解析和解题步骤</p>
          </div>
          
          <div class="feature-item">
            <div class="feature-icon">📈</div>
            <h4>学习分析</h4>
            <p>全面的学习数据分析和建议</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar.vue'

export default {
  name: 'StudentHomeSimple',
  components: {
    NavigationBar
  },
  setup() {
    const showComingSoon = () => {
      alert('功能开发中，敬请期待！')
    }
    
    return {
      showComingSoon
    }
  }
}
</script>

<style scoped>
.student-home {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.welcome-section {
  text-align: center;
  color: white;
  margin-bottom: 40px;
  padding: 40px 20px;
}

.welcome-section h1 {
  font-size: 3rem;
  margin-bottom: 15px;
  font-weight: 700;
}

.welcome-section p {
  font-size: 1.2rem;
  opacity: 0.9;
}

.quick-actions {
  background: white;
  border-radius: 20px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.quick-actions h2 {
  color: #333;
  margin-bottom: 25px;
  font-size: 1.8rem;
  text-align: center;
}

.action-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.action-card {
  display: block;
  text-decoration: none;
  color: inherit;
  background: #f8f9fa;
  border-radius: 15px;
  padding: 25px;
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  cursor: pointer;
}

.action-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  border-color: #667eea;
}

.action-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.action-card h3 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.3rem;
}

.action-card p {
  color: #666;
  margin: 0;
  font-size: 0.95rem;
  line-height: 1.4;
}

.features-section {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.features-section h2 {
  color: #333;
  margin-bottom: 25px;
  font-size: 1.8rem;
  text-align: center;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 25px;
}

.feature-item {
  text-align: center;
  padding: 20px;
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
}

.feature-item h4 {
  color: #333;
  margin-bottom: 10px;
  font-size: 1.2rem;
}

.feature-item p {
  color: #666;
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .container {
    padding: 10px;
  }
  
  .welcome-section h1 {
    font-size: 2.2rem;
  }
  
  .welcome-section {
    padding: 30px 15px;
  }
  
  .quick-actions,
  .features-section {
    padding: 20px;
  }
  
  .action-grid {
    grid-template-columns: 1fr;
  }
  
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .features-grid {
    grid-template-columns: 1fr;
  }
}
</style>