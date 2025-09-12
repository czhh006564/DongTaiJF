<template>
  <div class="exercise-container">
    <NavigationBar />
    <div class="exercise-header">
      <h1>智能练习</h1>
      <div class="exercise-config">
        <div class="config-row">
          <div class="config-item">
            <label>学科：</label>
            <select v-model="config.subject" required>
              <option value="">请选择学科</option>
              <option value="数学">数学</option>
              <option value="语文">语文</option>
              <option value="英语">英语</option>
            </select>
          </div>
          <div class="config-item">
            <label>年级：</label>
            <select v-model="config.grade" required>
              <option value="">请选择年级</option>
              <option value="1年级">1年级</option>
              <option value="2年级">2年级</option>
              <option value="3年级">3年级</option>
              <option value="4年级">4年级</option>
              <option value="5年级">5年级</option>
              <option value="6年级">6年级</option>
              <option value="7年级">7年级</option>
              <option value="8年级">8年级</option>
              <option value="9年级">9年级</option>
            </select>
          </div>
        </div>
        <div class="config-row">
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
        </div>
        <div class="config-actions">
          <button 
            @click="generateExercise" 
            :disabled="!canGenerate || loading"
            class="generate-btn"
          >
            {{ loading ? '生成中...' : '生成题目' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 练习区域 -->
    <div v-if="exercises.length > 0" class="exercise-area">
      <div class="exercise-progress">
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
        <span class="progress-text">{{ currentIndex + 1 }} / {{ exercises.length }}</span>
      </div>

      <div class="exercise-content">
        <div class="question-header">
          <h3>第 {{ currentIndex + 1 }} 题</h3>
          <span class="question-type">{{ getTypeText(currentExercise.type) }}题</span>
        </div>
        
        <div class="question-content">
          <p class="question-text">{{ currentExercise.question }}</p>
          
          <!-- 选择题选项 -->
          <div v-if="currentExercise.type === 'choice'" class="options">
            <div 
              v-for="option in currentExercise.options" 
              :key="option.key"
              class="option"
              :class="{ selected: userAnswers[currentIndex] === option.key }"
              @click="selectOption(option.key)"
            >
              <span class="option-key">{{ option.key }}.</span>
              <span class="option-text">{{ option.text }}</span>
            </div>
          </div>
          
          <!-- 填空题和解答题输入框 -->
          <div v-else class="answer-input">
            <textarea 
              v-model="userAnswers[currentIndex]"
              :placeholder="currentExercise.type === 'fill' ? '请填写答案...' : '请写出详细解答过程...'"
              :rows="currentExercise.type === 'solve' ? 6 : 2"
            ></textarea>
          </div>
        </div>

        <div class="exercise-actions">
          <button @click="previousQuestion" :disabled="currentIndex === 0" class="nav-btn">上一题</button>
          <button @click="nextQuestion" :disabled="currentIndex === exercises.length - 1" class="nav-btn">下一题</button>
          <button @click="submitExercise" :disabled="!canSubmit" class="submit-btn">提交答案</button>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else class="empty-state">
      <h3>开始你的智能练习</h3>
      <p>选择题目类型和数量，系统将为你生成个性化练习题目</p>
    </div>

    <!-- 结果弹窗 -->
    <div v-if="showResult" class="result-modal" @click="closeResult">
      <div class="result-content" @click.stop>
        <div class="result-header">
          <h2>🎉 练习完成！</h2>
          <div class="result-stats">
            <div class="stat-item">
              <span class="stat-label">正确率：</span>
              <span class="stat-value" :class="{ 'high-score': result.accuracy >= 80, 'medium-score': result.accuracy >= 60 && result.accuracy < 80, 'low-score': result.accuracy < 60 }">{{ result.accuracy }}%</span>
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
        </div>

        <!-- 题目详细回顾 -->
        <div class="questions-review">
          <h3>📋 题目回顾与分析</h3>
          <div class="questions-list">
            <div 
              v-for="(exercise, index) in exercises" 
              :key="index" 
              class="question-review-item"
              :class="{ 'correct': isAnswerCorrect(index), 'incorrect': !isAnswerCorrect(index) }"
            >
              <div class="question-header">
                <span class="question-number">第{{ index + 1 }}题</span>
                <span class="question-result">
                  <i v-if="isAnswerCorrect(index)" class="icon-correct">✅</i>
                  <i v-else class="icon-incorrect">❌</i>
                </span>
              </div>
              
              <div class="question-content">
                <div class="question-text">{{ exercise.question }}</div>
                <div class="knowledge-point">
                  <span class="knowledge-label">📚 知识点：</span>
                  <span class="knowledge-text">{{ exercise.knowledge_point || `${config.subject} - ${config.grade}` }}</span>
                </div>
              </div>

              <!-- 选择题选项显示 -->
              <div v-if="exercise.type === 'choice' && exercise.options" class="options-review">
                <div 
                  v-for="option in exercise.options" 
                  :key="option.key"
                  class="option-item"
                  :class="{
                    'user-selected': userAnswers[index] === option.key,
                    'correct-answer': exercise.answer === option.key,
                    'wrong-selected': userAnswers[index] === option.key && exercise.answer !== option.key
                  }"
                >
                  <span class="option-key">{{ option.key }}.</span>
                  <span class="option-text">{{ option.text }}</span>
                  <span v-if="exercise.answer === option.key" class="correct-mark">✓ 正确答案</span>
                  <span v-if="userAnswers[index] === option.key && exercise.answer !== option.key" class="wrong-mark">✗ 你的选择</span>
                  <span v-if="userAnswers[index] === option.key && exercise.answer === option.key" class="your-correct-mark">✓ 你的选择</span>
                </div>
              </div>

              <!-- 填空题和解答题答案显示 -->
              <div v-else class="answer-review">
                <div class="answer-item">
                  <span class="answer-label">正确答案：</span>
                  <span class="correct-answer-text">{{ exercise.answer }}</span>
                </div>
                <div v-if="userAnswers[index]" class="answer-item">
                  <span class="answer-label">你的答案：</span>
                  <span class="user-answer-text" :class="{ 'correct': isAnswerCorrect(index), 'incorrect': !isAnswerCorrect(index) }">
                    {{ userAnswers[index] }}
                  </span>
                </div>
              </div>

              <!-- 错题辅导和鼓励 -->
              <div v-if="!isAnswerCorrect(index)" class="error-guidance">
                <div class="encouragement">
                  <span class="encourage-icon">💪</span>
                  <span class="encourage-text">{{ getEncouragement() }}</span>
                </div>
                <div class="error-analysis">
                  <span class="analysis-label">💡 错因分析：</span>
                  <span class="analysis-text">{{ getErrorAnalysis(exercise, userAnswers[index]) }}</span>
                </div>
                <div class="improvement-tip">
                  <span class="tip-label">📖 学习建议：</span>
                  <span class="tip-text">{{ getImprovementTip(exercise) }}</span>
                </div>
              </div>

              <!-- 正确题目的解析 -->
              <div v-else class="correct-explanation">
                <div class="explanation">
                  <span class="explanation-label">✨ 解析：</span>
                  <span class="explanation-text">{{ exercise.explanation }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="result-actions">
          <button @click="restartExercise" class="restart-btn">🔄 重新练习</button>
          <button @click="generateSimilarExercise" class="similar-btn">📝 生成相似题目</button>
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
import axios from 'axios'

// 配置API客户端
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  name: 'StudentExercise',
  components: {
    NavigationBar
  },
  setup() {
    const router = useRouter()
    
    const config = ref({
      subject: '数学',
      grade: '1年级',
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
    
    const canGenerate = computed(() => {
      return config.value.subject && config.value.grade
    })
    
    const generateExercise = async () => {
      if (!canGenerate.value) {
        alert('请先选择学科和年级')
        return
      }
      
      loading.value = true
      try {
        console.log('🎯 开始生成题目...', {
          subject: config.value.subject,
          grade: config.value.grade,
          type: config.value.type,
          count: config.value.count
        })
        
        // 调用AI生成题目
        const response = await api.post('/api/ai/generate-exercise', {
          subject: config.value.subject,
          grade: config.value.grade,
          question_type: config.value.type,
          question_count: parseInt(config.value.count),
          knowledge_points: [`${config.value.grade}年级${config.value.subject}`],
          difficulty_level: 1
        })
        
        console.log('✅ AI题目生成成功:', response.data)
        
        if (response.data.success && response.data.questions) {
          // 转换AI生成的题目格式
          const aiExercises = response.data.questions.map((q, index) => ({
            id: index + 1,
            type: config.value.type === 'mixed' ? ['choice', 'fill', 'solve'][Math.floor(Math.random() * 3)] : config.value.type,
            question: q.content || q.question || `${config.value.subject}题目 ${index + 1}`,
            options: q.options ? q.options.map((opt, i) => ({
              key: String.fromCharCode(65 + i), // A, B, C, D
              text: opt
            })) : (config.value.type === 'choice' ? [
              { key: 'A', text: '选项A' },
              { key: 'B', text: '选项B' },
              { key: 'C', text: '选项C' },
              { key: 'D', text: '选项D' }
            ] : null),
            answer: q.answer || 'A',
            explanation: q.explanation || '这是题目的详细解析...',
            knowledge_point: q.knowledge_point || `${config.value.grade}年级${config.value.subject}`,
            difficulty: q.difficulty || 1
          }))
          
          exercises.value = aiExercises
          alert(`🎉 成功生成 ${aiExercises.length} 道${config.value.subject}题目！`)
        } else {
          throw new Error(response.data.message || 'AI题目生成失败')
        }
        
      } catch (error) {
        console.error('❌ 题目生成失败:', error)
        
        // 如果AI生成失败，使用备用题目
        const fallbackExercises = generateFallbackQuestions()
        exercises.value = fallbackExercises
        
        // 正确提取错误信息
        let errorMsg = '网络连接失败'
        if (error.response?.data?.detail) {
          errorMsg = error.response.data.detail
        } else if (error.response?.data?.message) {
          errorMsg = error.response.data.message
        } else if (error.message) {
          errorMsg = error.message
        }
        
        alert(`❌ AI题目生成失败，使用备用题目: ${errorMsg}`)
      } finally {
        loading.value = false
      }
    }
    
    // 生成备用题目
    const generateFallbackQuestions = () => {
      const subjectQuestions = {
        '数学': [
          { question: `计算：2 + 3 = ?`, options: [
            { key: 'A', text: '4' }, { key: 'B', text: '5' }, { key: 'C', text: '6' }, { key: 'D', text: '7' }
          ], answer: 'B' },
          { question: `计算：8 - 3 = ?`, options: [
            { key: 'A', text: '4' }, { key: 'B', text: '5' }, { key: 'C', text: '6' }, { key: 'D', text: '7' }
          ], answer: 'B' },
          { question: `计算：4 × 2 = ?`, options: [
            { key: 'A', text: '6' }, { key: 'B', text: '7' }, { key: 'C', text: '8' }, { key: 'D', text: '9' }
          ], answer: 'C' }
        ],
        '语文': [
          { question: `下列词语中，哪个是形容词？`, options: [
            { key: 'A', text: '跑步' }, { key: 'B', text: '美丽' }, { key: 'C', text: '吃饭' }, { key: 'D', text: '睡觉' }
          ], answer: 'B' },
          { question: `"春眠不觉晓"的下一句是？`, options: [
            { key: 'A', text: '处处闻啼鸟' }, { key: 'B', text: '夜来风雨声' }, { key: 'C', text: '花落知多少' }, { key: 'D', text: '红掌拨清波' }
          ], answer: 'A' },
          { question: `下列哪个字是多音字？`, options: [
            { key: 'A', text: '山' }, { key: 'B', text: '水' }, { key: 'C', text: '行' }, { key: 'D', text: '火' }
          ], answer: 'C' }
        ],
        '英语': [
          { question: `"Hello" 的中文意思是？`, options: [
            { key: 'A', text: '再见' }, { key: 'B', text: '你好' }, { key: 'C', text: '谢谢' }, { key: 'D', text: '对不起' }
          ], answer: 'B' },
          { question: `下列哪个是颜色单词？`, options: [
            { key: 'A', text: 'cat' }, { key: 'B', text: 'red' }, { key: 'C', text: 'run' }, { key: 'D', text: 'book' }
          ], answer: 'B' },
          { question: `"apple" 的中文意思是？`, options: [
            { key: 'A', text: '香蕉' }, { key: 'B', text: '苹果' }, { key: 'C', text: '橙子' }, { key: 'D', text: '葡萄' }
          ], answer: 'B' }
        ]
      }
      
      const questions = subjectQuestions[config.value.subject] || subjectQuestions['数学']
      return questions.slice(0, parseInt(config.value.count)).map((q, index) => ({
        id: index + 1,
        type: config.value.type === 'mixed' ? ['choice', 'fill', 'solve'][Math.floor(Math.random() * 3)] : config.value.type,
        ...q,
        explanation: `这是${config.value.subject}${config.value.grade}年级的题目解析...`
      }))
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

    // 判断答案是否正确
    const isAnswerCorrect = (index) => {
      const exercise = exercises.value[index]
      const userAnswer = userAnswers.value[index]
      
      if (!exercise || !userAnswer) return false
      
      // 对于选择题，直接比较选项
      if (exercise.type === 'choice') {
        return userAnswer === exercise.answer
      }
      
      // 对于填空题和解答题，进行模糊匹配
      const correctAnswer = exercise.answer.toString().toLowerCase().trim()
      const userAnswerStr = userAnswer.toString().toLowerCase().trim()
      
      // 简单的模糊匹配逻辑
      return correctAnswer === userAnswerStr || 
             correctAnswer.includes(userAnswerStr) || 
             userAnswerStr.includes(correctAnswer)
    }

    // 获取鼓励语句
    const getEncouragement = () => {
      const encouragements = [
        "没关系，错误是学习的好朋友！继续加油！",
        "每一次错误都是进步的机会，你很棒！",
        "学习就是在错误中成长，保持好奇心！",
        "不要气馁，每个人都会犯错，重要的是从中学习！",
        "你已经很努力了，再接再厉！",
        "错误让我们更聪明，你正在变得更强！",
        "学习路上有起伏很正常，坚持就是胜利！",
        "每一道错题都是宝贵的学习资源！"
      ]
      return encouragements[Math.floor(Math.random() * encouragements.length)]
    }

    // 获取错因分析
    const getErrorAnalysis = (exercise, userAnswer) => {
      if (exercise.type === 'choice') {
        const analyses = [
          "可能是对题目理解不够准确，建议仔细阅读题目要求",
          "可能是相关知识点掌握不够牢固，需要加强基础练习",
          "可能是计算过程中出现了小错误，要养成检查的好习惯",
          "可能是对选项的理解有偏差，要学会排除法解题",
          "可能是审题不够仔细，要注意题目中的关键词"
        ]
        return analyses[Math.floor(Math.random() * analyses.length)]
      } else if (exercise.type === 'fill') {
        return "填空题需要准确记忆和理解，建议多做相关练习巩固知识点"
      } else {
        return "解答题需要完整的思路和步骤，建议梳理解题方法和关键步骤"
      }
    }

    // 获取学习建议
    const getImprovementTip = (exercise) => {
      const subject = config.value.subject
      const grade = config.value.grade
      
      const tips = {
        '数学': [
          `建议多练习${grade}数学基础运算，熟练掌握计算方法`,
          `可以通过画图或实物操作来理解数学概念`,
          `建议每天坚持做几道数学题，培养数学思维`,
          `可以寻求老师或同学的帮助，讨论解题思路`
        ],
        '语文': [
          `建议多阅读${grade}适合的课外书籍，提高语文素养`,
          `可以多背诵古诗词，培养语感和文学素养`,
          `建议多练习写作，提高语言表达能力`,
          `可以多查字典，积累词汇量`
        ],
        '英语': [
          `建议多听英语音频，培养语感和听力`,
          `可以多背单词，扩大词汇量`,
          `建议多练习英语口语，提高表达能力`,
          `可以看英语动画片或简单的英语读物`
        ]
      }
      
      const subjectTips = tips[subject] || tips['数学']
      return subjectTips[Math.floor(Math.random() * subjectTips.length)]
    }

    // 生成相似题目
    const generateSimilarExercise = async () => {
      // 找出错题的知识点
      const wrongQuestions = exercises.value.filter((_, index) => !isAnswerCorrect(index))
      
      if (wrongQuestions.length === 0) {
        alert('🎉 你全部答对了！可以尝试更高难度的题目')
        return
      }
      
      // 重新生成题目，重点关注错题的知识点
      await generateExercise()
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
      canGenerate,
      generateExercise,
      selectOption,
      nextQuestion,
      previousQuestion,
      submitExercise,
      formatTime,
      restartExercise,
      closeResult,
      isAnswerCorrect,
      getEncouragement,
      getErrorAnalysis,
      getImprovementTip,
      generateSimilarExercise,
      getTypeText
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
  flex-direction: column;
  gap: 1rem;
}

.config-row {
  display: flex;
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
  min-width: 4rem;
}

.config-item select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  min-width: 8rem;
}

.config-actions {
  display: flex;
  gap: 1rem;
}

.generate-btn {
  padding: 0.75rem 1.5rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.generate-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.exercise-area {
  margin-top: 2rem;
}

.exercise-progress {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #007bff;
  transition: width 0.3s ease;
}

.progress-text {
  font-weight: 500;
  color: #495057;
}

.exercise-content {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.question-header h3 {
  margin: 0;
  color: #333;
}

.question-type {
  background-color: #007bff;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.question-content {
  margin-bottom: 1.5rem;
}

.question-text {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 1rem;
  color: #333;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.option {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background-color: white;
  border: 2px solid #dee2e6;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.option:hover {
  border-color: #007bff;
  background-color: #f8f9fa;
}

.option.selected {
  border-color: #007bff;
  background-color: #e3f2fd;
}

.option-key {
  font-weight: bold;
  margin-right: 0.75rem;
  color: #495057;
}

.option-text {
  flex: 1;
  color: #333;
}

.answer-input {
  margin-top: 1rem;
}

.answer-input textarea {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #dee2e6;
  border-radius: 6px;
  font-size: 1rem;
  resize: vertical;
  font-family: inherit;
}

.answer-input textarea:focus {
  outline: none;
  border-color: #007bff;
}

.exercise-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.nav-btn, .submit-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.nav-btn {
  background-color: #6c757d;
  color: white;
}

.nav-btn:disabled {
  background-color: #adb5bd;
  cursor: not-allowed;
}

.submit-btn {
  background-color: #28a745;
  color: white;
}

.submit-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.nav-btn:hover:not(:disabled), .submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.empty-state {
  text-align: center;
  padding: 3rem 1rem;
  color: #6c757d;
}

.empty-state h3 {
  margin-bottom: 1rem;
  color: #495057;
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
  background-color: white;
  border-radius: 12px;
  padding: 2rem;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.result-header {
  margin-bottom: 1.5rem;
}

.result-header h2 {
  margin-bottom: 1rem;
  text-align: center;
  color: #333;
}

.result-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
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

.high-score {
  color: #28a745 !important;
  font-weight: bold;
}

.medium-score {
  color: #ffc107 !important;
  font-weight: bold;
}

.low-score {
  color: #dc3545 !important;
  font-weight: bold;
}

/* 题目回顾样式 */
.questions-review {
  margin-top: 1.5rem;
  max-height: 400px;
  overflow-y: auto;
}

.questions-review h3 {
  margin-bottom: 1rem;
  color: #333;
  font-size: 1.1rem;
}

.questions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.question-review-item {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  background-color: #f8f9fa;
}

.question-review-item.correct {
  border-color: #28a745;
  background-color: #d4edda;
}

.question-review-item.incorrect {
  border-color: #dc3545;
  background-color: #f8d7da;
}

.question-review-item .question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.question-number {
  font-weight: bold;
  color: #495057;
}

.icon-correct, .icon-incorrect {
  font-size: 1.2rem;
}

.question-review-item .question-content {
  margin-bottom: 1rem;
}

.question-review-item .question-text {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #212529;
}

.knowledge-point {
  font-size: 0.9rem;
  color: #6c757d;
  background-color: #e9ecef;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  display: inline-block;
}

.knowledge-label {
  font-weight: 500;
}

.knowledge-text {
  margin-left: 0.25rem;
}

/* 选项回顾样式 */
.options-review {
  margin: 0.5rem 0;
}

.option-item {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  margin: 0.25rem 0;
  border-radius: 4px;
  background-color: #ffffff;
  border: 1px solid #dee2e6;
}

.option-item.correct-answer {
  background-color: #d4edda;
  border-color: #28a745;
}

.option-item.wrong-selected {
  background-color: #f8d7da;
  border-color: #dc3545;
}

.option-item.user-selected.correct-answer {
  background-color: #d1ecf1;
  border-color: #17a2b8;
}

.option-item .option-key {
  font-weight: bold;
  margin-right: 0.5rem;
  min-width: 1.5rem;
}

.option-item .option-text {
  flex: 1;
}

.correct-mark, .wrong-mark, .your-correct-mark {
  font-size: 0.8rem;
  font-weight: bold;
  margin-left: 0.5rem;
}

.correct-mark, .your-correct-mark {
  color: #28a745;
}

.wrong-mark {
  color: #dc3545;
}

/* 答案回顾样式 */
.answer-review {
  margin: 0.5rem 0;
}

.answer-item {
  display: flex;
  align-items: center;
  margin: 0.25rem 0;
}

.answer-label {
  font-weight: 500;
  margin-right: 0.5rem;
  min-width: 5rem;
}

.correct-answer-text {
  color: #28a745;
  font-weight: 500;
}

.user-answer-text.correct {
  color: #28a745;
  font-weight: 500;
}

.user-answer-text.incorrect {
  color: #dc3545;
  font-weight: 500;
}

/* 错题辅导样式 */
.error-guidance {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 6px;
}

.encouragement {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
}

.encourage-icon {
  font-size: 1.2rem;
  margin-right: 0.5rem;
}

.encourage-text {
  color: #856404;
  font-weight: 500;
}

.error-analysis, .improvement-tip {
  display: flex;
  align-items: flex-start;
  margin-bottom: 0.5rem;
}

.analysis-label, .tip-label {
  font-weight: 500;
  margin-right: 0.5rem;
  min-width: 5rem;
  color: #495057;
}

.analysis-text, .tip-text {
  color: #6c757d;
  line-height: 1.4;
}

/* 正确题目解析样式 */
.correct-explanation {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 6px;
}

.explanation {
  display: flex;
  align-items: flex-start;
}

.explanation-label {
  font-weight: 500;
  margin-right: 0.5rem;
  min-width: 3rem;
  color: #155724;
}

.explanation-text {
  color: #155724;
  line-height: 1.4;
}

.result-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-top: 1.5rem;
}

.result-actions button {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  min-width: 120px;
}

.restart-btn {
  background-color: #28a745;
  color: white;
}

.similar-btn {
  background-color: #17a2b8;
  color: white;
}

.close-btn {
  background-color: #6c757d;
  color: white;
}

.result-actions button:hover {
  opacity: 0.9;
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .exercise-container {
    padding: 1rem;
  }
  
  .config-row {
    flex-direction: column;
  }
  
  .exercise-actions {
    flex-direction: column;
  }
  
  .result-content {
    padding: 1rem;
    margin: 1rem;
  }
  
  .questions-review {
    max-height: 300px;
  }
}
</style>