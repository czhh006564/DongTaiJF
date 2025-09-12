<template>
  <div class="report-container">
    <NavigationBarSafe />
    <div class="report-header">
      <h1>学习报告</h1>
      <div class="time-filter">
        <button 
          v-for="period in timePeriods" 
          :key="period.value"
          :class="{ active: selectedPeriod === period.value }"
          @click="selectPeriod(period.value)"
          class="period-btn"
        >
          {{ period.label }}
        </button>
      </div>
    </div>

    <div class="report-content">
      <!-- 总体统计 -->
      <div class="overview-section">
        <h2>总体表现</h2>
        <div class="overview-grid">
          <div class="overview-card">
            <div class="card-icon">📊</div>
            <div class="card-content">
              <h3>{{ overview.totalExercises }}</h3>
              <p>完成练习</p>
            </div>
          </div>
          
          <div class="overview-card">
            <div class="card-icon">✅</div>
            <div class="card-content">
              <h3>{{ overview.averageAccuracy }}%</h3>
              <p>平均正确率</p>
            </div>
          </div>
          
          <div class="overview-card">
            <div class="card-icon">⏱️</div>
            <div class="card-content">
              <h3>{{ formatTime(overview.totalTime) }}</h3>
              <p>学习时长</p>
            </div>
          </div>
          
          <div class="overview-card">
            <div class="card-icon">🏆</div>
            <div class="card-content">
              <h3>{{ overview.totalPoints }}</h3>
              <p>获得积分</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习趋势图 -->
      <div class="chart-section">
        <h2>学习趋势</h2>
        <div class="chart-container">
          <div class="chart-placeholder">
            <div class="chart-info">
              <p>📈 学习趋势图表</p>
              <p class="chart-desc">显示{{ selectedPeriodLabel }}的学习数据变化</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 知识点分析 -->
      <div class="knowledge-section">
        <h2>知识点掌握情况</h2>
        <div class="knowledge-grid">
          <div 
            v-for="knowledge in knowledgePoints" 
            :key="knowledge.id"
            class="knowledge-card"
          >
            <div class="knowledge-header">
              <h4>{{ knowledge.name }}</h4>
              <span class="mastery-level" :class="getMasteryClass(knowledge.mastery)">
                {{ getMasteryText(knowledge.mastery) }}
              </span>
            </div>
            
            <div class="progress-container">
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: `${knowledge.mastery}%` }"
                  :class="getMasteryClass(knowledge.mastery)"
                ></div>
              </div>
              <span class="progress-text">{{ knowledge.mastery }}%</span>
            </div>
            
            <div class="knowledge-stats">
              <span>练习次数: {{ knowledge.practiceCount }}</span>
              <span>错误次数: {{ knowledge.errorCount }}</span>
            </div>
            
            <div class="knowledge-actions">
              <button @click="practiceKnowledge(knowledge)" class="practice-btn">
                针对练习
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 错题分析 -->
      <div class="error-section">
        <h2>错题分析</h2>
        <div class="error-summary">
          <div class="error-stats">
            <div class="error-stat">
              <span class="stat-number">{{ errorAnalysis.totalErrors }}</span>
              <span class="stat-label">总错题数</span>
            </div>
            <div class="error-stat">
              <span class="stat-number">{{ errorAnalysis.repeatedErrors }}</span>
              <span class="stat-label">重复错误</span>
            </div>
            <div class="error-stat">
              <span class="stat-number">{{ errorAnalysis.improvedErrors }}</span>
              <span class="stat-label">已改进</span>
            </div>
          </div>
        </div>
        
        <div class="error-list">
          <div 
            v-for="error in recentErrors" 
            :key="error.id"
            class="error-item"
          >
            <div class="error-content">
              <h4>{{ error.question }}</h4>
              <div class="error-details">
                <span class="error-type">{{ error.type }}</span>
                <span class="error-subject">{{ error.subject }}</span>
                <span class="error-date">{{ error.date }}</span>
              </div>
              <p class="error-reason">常见错误原因: {{ error.reason }}</p>
            </div>
            <div class="error-actions">
              <button @click="reviewError(error)" class="review-btn">
                查看详情
              </button>
              <button @click="practiceError(error)" class="practice-btn">
                重新练习
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 学习建议 -->
      <div class="suggestion-section">
        <h2>学习建议</h2>
        <div class="suggestion-list">
          <div 
            v-for="suggestion in suggestions" 
            :key="suggestion.id"
            class="suggestion-item"
            :class="suggestion.priority"
          >
            <div class="suggestion-icon">{{ suggestion.icon }}</div>
            <div class="suggestion-content">
              <h4>{{ suggestion.title }}</h4>
              <p>{{ suggestion.description }}</p>
            </div>
            <div class="suggestion-action">
              <button @click="applySuggestion(suggestion)" class="apply-btn">
                立即执行
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavigationBarSafe from '@/components/NavigationBar-Safe.vue'

export default {
  name: 'StudentReport',
  components: {
    NavigationBarSafe
  },
  setup() {
    const router = useRouter()
    
    const selectedPeriod = ref('week')
    const timePeriods = [
      { value: 'week', label: '本周' },
      { value: 'month', label: '本月' },
      { value: 'quarter', label: '本季度' },
      { value: 'year', label: '本年' }
    ]
    
    const overview = ref({
      totalExercises: 0,
      averageAccuracy: 0,
      totalTime: 0,
      totalPoints: 0
    })
    
    const knowledgePoints = ref([])
    const errorAnalysis = ref({
      totalErrors: 0,
      repeatedErrors: 0,
      improvedErrors: 0
    })
    const recentErrors = ref([])
    const suggestions = ref([])
    
    const selectedPeriodLabel = computed(() => {
      const period = timePeriods.find(p => p.value === selectedPeriod.value)
      return period ? period.label : '本周'
    })
    
    const selectPeriod = (period) => {
      selectedPeriod.value = period
      loadReportData()
    }
    
    const loadReportData = async () => {
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        // 模拟数据
        overview.value = {
          totalExercises: 45,
          averageAccuracy: 87,
          totalTime: 12600, // 秒
          totalPoints: 1250
        }
        
        knowledgePoints.value = [
          {
            id: 1,
            name: '代数运算',
            mastery: 92,
            practiceCount: 15,
            errorCount: 2
          },
          {
            id: 2,
            name: '几何图形',
            mastery: 78,
            practiceCount: 12,
            errorCount: 5
          },
          {
            id: 3,
            name: '函数概念',
            mastery: 65,
            practiceCount: 8,
            errorCount: 7
          },
          {
            id: 4,
            name: '概率统计',
            mastery: 85,
            practiceCount: 10,
            errorCount: 3
          }
        ]
        
        errorAnalysis.value = {
          totalErrors: 17,
          repeatedErrors: 5,
          improvedErrors: 12
        }
        
        recentErrors.value = [
          {
            id: 1,
            question: '求函数f(x)=x²+2x-3的最小值',
            type: '解答题',
            subject: '数学',
            date: '2024-01-15',
            reason: '配方法运用不熟练'
          },
          {
            id: 2,
            question: '计算圆的面积公式应用',
            type: '选择题',
            subject: '数学',
            date: '2024-01-14',
            reason: '公式记忆错误'
          }
        ]
        
        suggestions.value = [
          {
            id: 1,
            icon: '📚',
            title: '加强函数概念练习',
            description: '函数概念掌握程度较低，建议增加相关练习',
            priority: 'high',
            action: 'practice_function'
          },
          {
            id: 2,
            icon: '⏰',
            title: '保持学习节奏',
            description: '最近学习时间较少，建议每天至少练习30分钟',
            priority: 'medium',
            action: 'daily_practice'
          },
          {
            id: 3,
            icon: '🎯',
            title: '复习错题',
            description: '有5道题目重复出错，建议重点复习',
            priority: 'high',
            action: 'review_errors'
          }
        ]
        
      } catch (error) {
        console.error('加载报告数据失败:', error)
      }
    }
    
    const formatTime = (seconds) => {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      return `${hours}h ${minutes}m`
    }
    
    const getMasteryClass = (mastery) => {
      if (mastery >= 90) return 'excellent'
      if (mastery >= 80) return 'good'
      if (mastery >= 70) return 'average'
      return 'poor'
    }
    
    const getMasteryText = (mastery) => {
      if (mastery >= 90) return '优秀'
      if (mastery >= 80) return '良好'
      if (mastery >= 70) return '一般'
      return '需提高'
    }
    
    const practiceKnowledge = (knowledge) => {
      router.push(`/student/exercise?knowledge=${knowledge.id}`)
    }
    
    const reviewError = (error) => {
      alert(`查看错题详情: ${error.question}`)
    }
    
    const practiceError = (error) => {
      router.push(`/student/exercise?error=${error.id}`)
    }
    
    const applySuggestion = (suggestion) => {
      switch (suggestion.action) {
        case 'practice_function':
          router.push('/student/exercise?type=function')
          break
        case 'daily_practice':
          alert('已为您制定每日练习计划')
          break
        case 'review_errors':
          router.push('/student/exercise?mode=review')
          break
        default:
          alert('执行建议: ' + suggestion.title)
      }
    }
    
    onMounted(() => {
      loadReportData()
    })
    
    return {
      selectedPeriod,
      selectedPeriodLabel,
      timePeriods,
      overview,
      knowledgePoints,
      errorAnalysis,
      recentErrors,
      suggestions,
      selectPeriod,
      formatTime,
      getMasteryClass,
      getMasteryText,
      practiceKnowledge,
      reviewError,
      practiceError,
      applySuggestion
    }
  }
}
</script>

<style scoped>
.report-container {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.report-header h1 {
  margin: 0;
  color: #333;
}

.time-filter {
  display: flex;
  gap: 0.5rem;
}

.period-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.period-btn:hover {
  border-color: #007bff;
}

.period-btn.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.report-content > div {
  margin-bottom: 2rem;
}

.report-content h2 {
  margin-bottom: 1rem;
  color: #333;
  border-bottom: 2px solid #007bff;
  padding-bottom: 0.5rem;
}

/* 总体统计 */
.overview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
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

.card-content h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.card-content p {
  margin: 0.25rem 0 0 0;
  color: #666;
  font-size: 0.9rem;
}

/* 图表区域 */
.chart-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chart-placeholder {
  text-align: center;
  color: #666;
}

.chart-info p {
  margin: 0.5rem 0;
}

.chart-desc {
  font-size: 0.9rem;
  opacity: 0.8;
}

/* 知识点分析 */
.knowledge-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.knowledge-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.knowledge-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.knowledge-header h4 {
  margin: 0;
  color: #333;
}

.mastery-level {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.mastery-level.excellent {
  background-color: #d4edda;
  color: #155724;
}

.mastery-level.good {
  background-color: #d1ecf1;
  color: #0c5460;
}

.mastery-level.average {
  background-color: #fff3cd;
  color: #856404;
}

.mastery-level.poor {
  background-color: #f8d7da;
  color: #721c24;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
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

.progress-text {
  font-size: 0.9rem;
  font-weight: 500;
  color: #666;
}

.knowledge-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  color: #666;
}

.knowledge-actions {
  text-align: center;
}

.practice-btn {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.practice-btn:hover {
  background-color: #0056b3;
}

/* 错题分析 */
.error-summary {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 1rem;
}

.error-stats {
  display: flex;
  justify-content: space-around;
  text-align: center;
}

.error-stat {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #007bff;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
}

.error-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.error-item {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.error-content {
  flex: 1;
}

.error-content h4 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.error-details {
  display: flex;
  gap: 1rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.error-type, .error-subject {
  padding: 0.25rem 0.5rem;
  background-color: #f8f9fa;
  border-radius: 4px;
  color: #666;
}

.error-date {
  color: #999;
}

.error-reason {
  margin: 0;
  color: #666;
  font-size: 0.9rem;
}

.error-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.review-btn {
  padding: 0.5rem 1rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.review-btn:hover {
  background-color: #545b62;
}

/* 学习建议 */
.suggestion-list {
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
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.apply-btn:hover {
  background-color: #218838;
}

@media (max-width: 768px) {
  .report-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .time-filter {
    justify-content: center;
  }
  
  .error-item {
    flex-direction: column;
  }
  
  .error-actions {
    flex-direction: row;
    align-self: stretch;
  }
  
  .suggestion-item {
    flex-direction: column;
    text-align: center;
  }
}
</style>