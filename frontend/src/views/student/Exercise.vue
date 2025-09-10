<template>
  <div class="exercise-container">
    <NavigationBar />
    <div class="exercise-header">
      <h1>智能练习</h1>
      <div class="exercise-config">
        <div class="config-item">
          <label>题目类型：</label>
          <select v-model="config.type">
            <option value="choice">选择题</option>
            <option value="fill">填空题</option>
            <option value="solve">解答题</option>
            <option value="mixed">混合题型</option>
          </select>
        </div>
        <div class="config-item">
          <label>题目数量：</label>
          <select v-model="config.count">
            <option value="5">5题</option>
            <option value="10">10题</option>
            <option value="15">15题</option>
            <option value="20">20题</option>
          </select>
        </div>
        <button @click="generateExercise" :disabled="loading" class="generate-btn">
          {{ loading ? '生成中...' : '生成题目' }}
        </button>
      </div>
    </div>

    <div v-if="exercises.length > 0" class="exercise-content">
      <div class="progress-bar">
        <div class="progress" :style="{ width: `${progress}%` }"></div>
      </div>
      
      <div class="question-info">
        <span>第 {{ currentIndex + 1 }} 题 / 共 {{ exercises.length }} 题</span>
        <span class="timer">⏱️ {{ formatTime(timeElapsed) }}</span>
      </div>

      <div class="question-card">
        <div class="question-content">
          <h3>{{ currentExercise.question }}</h3>
          <div v-if="currentExercise.image" class="question-image">
            <img :src="currentExercise.image" alt="题目图片" />
          </div>
        </div>

        <div class="answer-section">
          <!-- 选择题 -->
          <div v-if="currentExercise.type === 'choice'" class="choice-options">
            <div 
              v-for="(option, index) in currentExercise.options" 
              :key="index"
              class="option-item"
              :class="{ selected: userAnswers[currentIndex] === option.key }"
              @click="selectOption(option.key)"
            >
              <span class="option-key">{{ option.key }}</span>
              <span class="option-text">{{ option.text }}</span>
            </div>
          </div>

          <!-- 填空题 -->
          <div v-else-if="currentExercise.type === 'fill'" class="fill-answer">
            <input 
              v-model="userAnswers[currentIndex]"
              type="text" 
              placeholder="请输入答案"
              class="fill-input"
            />
          </div>

          <!-- 解答题 -->
          <div v-else-if="currentExercise.type === 'solve'" class="solve-answer">
            <textarea 
              v-model="userAnswers[currentIndex]"
              placeholder="请写出详细解答过程"
              class="solve-textarea"
              rows="6"
            ></textarea>
          </div>
        </div>

        <div class="question-actions">
          <button 
            @click="previousQuestion" 
            :disabled="currentIndex === 0"
            class="nav-btn prev-btn"
          >
            上一题
          </button>
          
          <button 
            v-if="currentIndex < exercises.length - 1"
            @click="nextQuestion"
            class="nav-btn next-btn"
          >
            下一题
          </button>
          
          <button 
            v-else
            @click="submitExercise"
            class="submit-btn"
            :disabled="!canSubmit"
          >
            提交答案
          </button>
        </div>
      </div>
    </div>

    <div v-else-if="!loading" class="empty-state">
      <div class="empty-icon">📝</div>
      <h3>开始你的智能练习</h3>
      <p>选择题目类型和数量，系统将为你生成个性化练习题目</p>
    </div>

    <!-- 结果弹窗 -->
    <div v-if="showResult" class="result-modal" @click="closeResult">
      <div class="result-content" @click.stop>
        <h2>练习完成！</h2>
        <div class="result-stats">
          <div class="stat-item">
            <span class="stat-label">正确率：</span>
            <span class="stat-value">{{ result.accuracy }}%</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">用时：</span>
            <span class="stat-value">{{ formatTime(result.timeUsed) }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">获得积分：</span>
            <span class="stat-value">+{{ result.points }}</span>
          </div>
        </div>
        <div class="result-actions">
          <button @click="viewReport" class="view-report-btn">查看详细报告</button>
          <button @click="restartExercise" class="restart-btn">重新练习</button>
          <button @click="closeResult" class="close-btn">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import NavigationBar from '@/components/NavigationBar.vue'

export default {
  name: 'StudentExercise',
  components: {
    NavigationBar
  },
  setup() {
    const router = useRouter()
    
    const config = ref({
      type: 'choice',
      count: '10'
    })
    
    const exercises = ref([])
    const currentIndex = ref(0)
    const userAnswers = ref({})
    const loading = ref(false)
    const showResult = ref(false)
    const result = ref({})
    const timeElapsed = ref(0)
    const timer = ref(null)
    
    const currentExercise = computed(() => exercises.value[currentIndex.value] || {})
    const progress = computed(() => ((currentIndex.value + 1) / exercises.value.length) * 100)
    const canSubmit = computed(() => {
      return exercises.value.every((_, index) => userAnswers.value[index])
    })
    
    const generateExercise = async () => {
      loading.value = true
      try {
        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        // 生成模拟题目
        const mockExercises = []
        for (let i = 0; i < parseInt(config.value.count); i++) {
          mockExercises.push({
            id: i + 1,
            type: config.value.type === 'mixed' ? ['choice', 'fill', 'solve'][Math.floor(Math.random() * 3)] : config.value.type,
            question: `这是第${i + 1}道${getTypeText(config.value.type)}题目，请仔细阅读并作答。`,
            options: config.value.type === 'choice' ? [
              { key: 'A', text: '选项A的内容' },
              { key: 'B', text: '选项B的内容' },
              { key: 'C', text: '选项C的内容' },
              { key: 'D', text: '选项D的内容' }
            ] : null,
            answer: 'A',
            explanation: '这是题目的详细解析...'
          })
        }
        
        exercises.value = mockExercises
        currentIndex.value = 0
        userAnswers.value = {}
        startTimer()
        
      } catch (error) {
        alert('生成题目失败：' + error.message)
      } finally {
        loading.value = false
      }
    }
    
    const getTypeText = (type) => {
      const typeMap = {
        choice: '选择',
        fill: '填空',
        solve: '解答',
        mixed: '混合'
      }
      return typeMap[type] || '选择'
    }
    
    const selectOption = (key) => {
      userAnswers.value[currentIndex.value] = key
    }
    
    const nextQuestion = () => {
      if (currentIndex.value < exercises.value.length - 1) {
        currentIndex.value++
      }
    }
    
    const previousQuestion = () => {
      if (currentIndex.value > 0) {
        currentIndex.value--
      }
    }
    
    const submitExercise = async () => {
      stopTimer()
      
      // 计算结果
      let correctCount = 0
      exercises.value.forEach((exercise, index) => {
        if (userAnswers.value[index] === exercise.answer) {
          correctCount++
        }
      })
      
      const accuracy = Math.round((correctCount / exercises.value.length) * 100)
      const points = Math.round(accuracy * exercises.value.length / 10)
      
      result.value = {
        accuracy,
        timeUsed: timeElapsed.value,
        points,
        correctCount,
        totalCount: exercises.value.length
      }
      
      showResult.value = true
    }
    
    const startTimer = () => {
      timeElapsed.value = 0
      timer.value = setInterval(() => {
        timeElapsed.value++
      }, 1000)
    }
    
    const stopTimer = () => {
      if (timer.value) {
        clearInterval(timer.value)
        timer.value = null
      }
    }
    
    const formatTime = (seconds) => {
      const mins = Math.floor(seconds / 60)
      const secs = seconds % 60
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    }
    
    const viewReport = () => {
      router.push('/student/report')
    }
    
    const restartExercise = () => {
      showResult.value = false
      exercises.value = []
      userAnswers.value = {}
      currentIndex.value = 0
      timeElapsed.value = 0
    }
    
    const closeResult = () => {
      showResult.value = false
    }
    
    onUnmounted(() => {
      stopTimer()
    })
    
    return {
      config,
      exercises,
      currentIndex,
      currentExercise,
      userAnswers,
      loading,
      showResult,
      result,
      timeElapsed,
      progress,
      canSubmit,
      generateExercise,
      selectOption,
      nextQuestion,
      previousQuestion,
      submitExercise,
      formatTime,
      viewReport,
      restartExercise,
      closeResult
    }
  }
}
</script>

<style scoped>
.exercise-container {
  padding: 1.5rem;
  max-width: 800px;
  margin: 0 auto;
}

.exercise-header {
  margin-bottom: 2rem;
}

.exercise-header h1 {
  margin-bottom: 1rem;
  color: #333;
}

.exercise-config {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.config-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.config-item label {
  font-weight: 500;
  color: #555;
}

.config-item select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.generate-btn {
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.generate-btn:hover:not(:disabled) {
  background-color: #0056b3;
}

.generate-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.exercise-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.progress-bar {
  height: 4px;
  background-color: #f0f0f0;
}

.progress {
  height: 100%;
  background-color: #007bff;
  transition: width 0.3s ease;
}

.question-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.timer {
  font-weight: 500;
  color: #666;
}

.question-card {
  padding: 2rem;
}

.question-content h3 {
  margin-bottom: 1rem;
  color: #333;
  line-height: 1.6;
}

.question-image {
  margin: 1rem 0;
}

.question-image img {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.answer-section {
  margin: 2rem 0;
}

.choice-options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.option-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border: 2px solid #eee;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.option-item:hover {
  border-color: #007bff;
  background-color: #f8f9ff;
}

.option-item.selected {
  border-color: #007bff;
  background-color: #e3f2fd;
}

.option-key {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background-color: #f0f0f0;
  border-radius: 50%;
  font-weight: 500;
}

.option-item.selected .option-key {
  background-color: #007bff;
  color: white;
}

.fill-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #eee;
  border-radius: 4px;
  font-size: 1rem;
}

.fill-input:focus {
  outline: none;
  border-color: #007bff;
}

.solve-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #eee;
  border-radius: 4px;
  font-size: 1rem;
  resize: vertical;
}

.solve-textarea:focus {
  outline: none;
  border-color: #007bff;
}

.question-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.nav-btn, .submit-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.nav-btn {
  background-color: #6c757d;
  color: white;
}

.nav-btn:hover:not(:disabled) {
  background-color: #545b62;
}

.nav-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.submit-btn {
  background-color: #28a745;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background-color: #218838;
}

.submit-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.empty-state {
  text-align: center;
  padding: 3rem;
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

.result-modal {
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

.result-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  max-width: 400px;
  width: 90%;
}

.result-content h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

.result-stats {
  margin-bottom: 1.5rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.stat-item:last-child {
  border-bottom: none;
}

.stat-label {
  color: #666;
}

.stat-value {
  font-weight: 500;
  color: #333;
}

.result-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.result-actions button {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.view-report-btn {
  background-color: #007bff;
  color: white;
}

.restart-btn {
  background-color: #28a745;
  color: white;
}

.close-btn {
  background-color: #6c757d;
  color: white;
}

.result-actions button:hover {
  opacity: 0.9;
}
</style>