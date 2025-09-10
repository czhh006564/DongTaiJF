<template>
  <div class="parent-report">
    <div class="report-header">
      <h1>孩子学习报告</h1>
      <div class="child-selector">
        <select v-model="selectedChildId" @change="loadReport">
          <option value="">选择孩子</option>
          <option v-for="child in children" :key="child.id" :value="child.id">
            {{ child.name }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="selectedChild" class="report-content">
      <h2>{{ selectedChild.name }} 的学习报告</h2>
      
      <!-- 总体表现 -->
      <div class="overview-section">
        <h3>总体表现</h3>
        <div class="overview-grid">
          <div class="overview-card">
            <div class="card-icon">📊</div>
            <div class="card-content">
              <h4>{{ reportData.totalExercises }}</h4>
              <p>完成练习</p>
            </div>
          </div>
          
          <div class="overview-card">
            <div class="card-icon">✅</div>
            <div class="card-content">
              <h4>{{ reportData.averageAccuracy }}%</h4>
              <p>平均正确率</p>
            </div>
          </div>
          
          <div class="overview-card">
            <div class="card-icon">⏱️</div>
            <div class="card-content">
              <h4>{{ formatTime(reportData.totalTime) }}</h4>
              <p>学习时长</p>
            </div>
          </div>
          
          <div class="overview-card">
            <div class="card-icon">🏆</div>
            <div class="card-content">
              <h4>{{ reportData.totalPoints }}</h4>
              <p>获得积分</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 学科分析 -->
      <div class="subjects-section">
        <h3>学科分析</h3>
        <div class="subjects-grid">
          <div v-for="subject in reportData.subjects" :key="subject.name" class="subject-card">
            <h4>{{ subject.name }}</h4>
            <div class="subject-progress">
              <div class="progress-bar">
                <div class="progress-fill" :style="{ width: `${subject.mastery}%` }"></div>
              </div>
              <span>{{ subject.mastery }}%</span>
            </div>
            <div class="subject-stats">
              <span>练习次数: {{ subject.exercises }}</span>
              <span>正确率: {{ subject.accuracy }}%</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习建议 -->
      <div class="suggestions-section">
        <h3>学习建议</h3>
        <div class="suggestions-list">
          <div v-for="suggestion in reportData.suggestions" :key="suggestion.id" class="suggestion-item">
            <div class="suggestion-icon">{{ suggestion.icon }}</div>
            <div class="suggestion-content">
              <h4>{{ suggestion.title }}</h4>
              <p>{{ suggestion.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="no-selection">
      <div class="empty-state">
        <div class="empty-icon">📊</div>
        <h3>请选择一个孩子查看报告</h3>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'ParentReport',
  setup() {
    const children = ref([])
    const selectedChildId = ref('')
    const reportData = ref({})
    
    const selectedChild = computed(() => {
      return children.value.find(child => child.id === selectedChildId.value)
    })
    
    const loadChildren = async () => {
      children.value = [
        { id: 1, name: '张小明' },
        { id: 2, name: '张小红' }
      ]
    }
    
    const loadReport = async () => {
      if (!selectedChildId.value) return
      
      // 模拟报告数据
      reportData.value = {
        totalExercises: 156,
        averageAccuracy: 87,
        totalTime: 12600,
        totalPoints: 1250,
        subjects: [
          { name: '数学', mastery: 78, exercises: 45, accuracy: 85 },
          { name: '语文', mastery: 82, exercises: 32, accuracy: 90 },
          { name: '英语', mastery: 75, exercises: 38, accuracy: 82 }
        ],
        suggestions: [
          { id: 1, icon: '📚', title: '加强数学练习', description: '建议增加几何题目的练习' },
          { id: 2, icon: '⏰', title: '调整学习时间', description: '建议在下午进行重点科目学习' }
        ]
      }
    }
    
    const formatTime = (seconds) => {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      return `${hours}h ${minutes}m`
    }
    
    onMounted(() => {
      loadChildren()
    })
    
    return {
      children,
      selectedChildId,
      selectedChild,
      reportData,
      loadReport,
      formatTime
    }
  }
}
</script>

<style scoped>
.parent-report {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.child-selector select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.overview-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.card-icon {
  font-size: 2rem;
}

.card-content h4 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.card-content p {
  margin: 0.25rem 0 0 0;
  color: #666;
  font-size: 0.9rem;
}

.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.subject-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.subject-progress {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 1rem 0;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #007bff;
  transition: width 0.3s ease;
}

.subject-stats {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: #666;
}

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
}

.suggestion-icon {
  font-size: 2rem;
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

.no-selection {
  background: white;
  padding: 3rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  color: #333;
}
</style>