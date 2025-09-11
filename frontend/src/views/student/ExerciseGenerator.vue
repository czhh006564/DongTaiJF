<template>
  <div class="exercise-generator">
    <NavigationBar />
    
    <div class="container">
      <div class="header">
        <h1>智能题目生成</h1>
        <p>根据您的学习需求，AI将为您生成个性化练习题目</p>
      </div>

      <div class="generator-form" v-if="!isGenerating && !generatedExercise">
        <div class="form-section">
          <h3>基础设置</h3>
          <div class="form-group">
            <label for="subject">学科</label>
            <select id="subject" v-model="form.subject" required>
              <option value="">请选择学科</option>
              <option value="数学">数学</option>
              <option value="语文">语文</option>
              <option value="英语">英语</option>
              <option value="物理">物理</option>
              <option value="化学">化学</option>
              <option value="生物">生物</option>
              <option value="历史">历史</option>
              <option value="地理">地理</option>
              <option value="政治">政治</option>
            </select>
          </div>

          <div class="form-group">
            <label for="knowledgePoints">知识点 (多个知识点用逗号分隔)</label>
            <textarea 
              id="knowledgePoints" 
              v-model="knowledgePointsText" 
              placeholder="例如：二次函数，函数图像，最值问题"
              rows="3"
              required
            ></textarea>
          </div>
        </div>

        <div class="form-section">
          <h3>题目配置</h3>
          <div class="form-group">
            <label for="questionType">题目类型</label>
            <select id="questionType" v-model="form.question_type" required>
              <option value="choice">选择题</option>
              <option value="fill">填空题</option>
              <option value="solve">解答题</option>
              <option value="mixed">混合题型</option>
            </select>
          </div>

          <div class="form-group">
            <label for="questionCount">题目数量</label>
            <input 
              type="number" 
              id="questionCount" 
              v-model.number="form.question_count" 
              min="1" 
              max="20" 
              required
            >
          </div>

          <div class="form-group">
            <label for="difficultyLevel">难度等级</label>
            <select id="difficultyLevel" v-model.number="form.difficulty_level" required>
              <option :value="1">基础 (1级)</option>
              <option :value="2">中等 (2级)</option>
              <option :value="3">困难 (3级)</option>
              <option :value="4">挑战 (4级)</option>
            </select>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" @click="generateExercise" class="btn-generate" :disabled="!isFormValid">
            <span v-if="!isGenerating">🎯 生成题目</span>
            <span v-else>⏳ 生成中...</span>
          </button>
        </div>
      </div>

      <!-- 生成中状态 -->
      <div class="generating-status" v-if="isGenerating">
        <div class="loading-animation">
          <div class="spinner"></div>
          <h3>AI正在为您生成题目...</h3>
          <p>请稍候，这可能需要几秒钟时间</p>
        </div>
      </div>

      <!-- 生成结果 -->
      <div class="exercise-result" v-if="generatedExercise && !isGenerating">
        <div class="result-header">
          <h3>生成完成！</h3>
          <p>共生成 {{ generatedExercise.questions.length }} 道题目</p>
        </div>

        <div class="questions-preview">
          <div 
            v-for="(question, index) in generatedExercise.questions" 
            :key="index"
            class="question-card"
          >
            <div class="question-header">
              <span class="question-number">第 {{ index + 1 }} 题</span>
              <span class="question-type">{{ getQuestionTypeText(question.type) }}</span>
            </div>
            <div class="question-content">
              {{ question.content }}
            </div>
            <div class="question-options" v-if="question.options">
              <div 
                v-for="(option, optIndex) in question.options" 
                :key="optIndex"
                class="option"
              >
                {{ String.fromCharCode(65 + optIndex) }}. {{ option }}
              </div>
            </div>
          </div>
        </div>

        <div class="result-actions">
          <button @click="generatePDF" class="btn-pdf" :disabled="isGeneratingPDF">
            <span v-if="!isGeneratingPDF">📄 生成PDF</span>
            <span v-else>⏳ 生成中...</span>
          </button>
          <button @click="generateAnalysis" class="btn-analysis" :disabled="isGeneratingAnalysis">
            <span v-if="!isGeneratingAnalysis">💡 生成解析</span>
            <span v-else>⏳ 生成中...</span>
          </button>
          <button @click="resetGenerator" class="btn-reset">
            🔄 重新生成
          </button>
        </div>
      </div>

      <!-- 答案解析 -->
      <div class="analysis-result" v-if="analysisResult">
        <h3>答案解析</h3>
        <div 
          v-for="(analysis, index) in analysisResult.analyses" 
          :key="index"
          class="analysis-card"
        >
          <div class="analysis-header">
            <span class="question-number">第 {{ index + 1 }} 题解析</span>
          </div>
          <div class="analysis-content">
            <div class="answer-section">
              <strong>答案：</strong>{{ analysis.answer }}
            </div>
            <div class="steps-section" v-if="analysis.steps && analysis.steps.length">
              <strong>解题步骤：</strong>
              <ol>
                <li v-for="(step, stepIndex) in analysis.steps" :key="stepIndex">
                  {{ step }}
                </li>
              </ol>
            </div>
            <div class="tips-section" v-if="analysis.tips">
              <strong>解题提示：</strong>{{ analysis.tips }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import NavigationBar from '@/components/NavigationBar.vue'
import api from '@/utils/api'

export default {
  name: 'ExerciseGenerator',
  components: {
    NavigationBar
  },
  setup() {
    const router = useRouter()
    
    // 表单数据
    const form = ref({
      subject: '',
      question_type: 'choice',
      question_count: 5,
      difficulty_level: 1
    })
    
    const knowledgePointsText = ref('')
    
    // 状态管理
    const isGenerating = ref(false)
    const isGeneratingPDF = ref(false)
    const isGeneratingAnalysis = ref(false)
    const generatedExercise = ref(null)
    const analysisResult = ref(null)
    
    // 计算属性
    const isFormValid = computed(() => {
      return form.value.subject && 
             knowledgePointsText.value.trim() && 
             form.value.question_count > 0
    })
    
    // 方法
    const generateExercise = async () => {
      if (!isFormValid.value) {
        alert('请填写完整的表单信息')
        return
      }
      
      isGenerating.value = true
      
      try {
        const knowledge_points = knowledgePointsText.value
          .split(',')
          .map(point => point.trim())
          .filter(point => point)
        
        const response = await api.post('/api/ai/generate-exercise', {
          ...form.value,
          knowledge_points
        })
        
        if (response.data.success) {
          generatedExercise.value = response.data
          analysisResult.value = null // 重置解析结果
        } else {
          alert('题目生成失败：' + response.data.message)
        }
      } catch (error) {
        console.error('生成题目失败:', error)
        alert('生成题目时发生错误，请稍后重试')
      } finally {
        isGenerating.value = false
      }
    }
    
    const generatePDF = async () => {
      if (!generatedExercise.value) return
      
      isGeneratingPDF.value = true
      
      try {
        const response = await api.post('/api/ai/generate-pdf', {
          exercise_id: generatedExercise.value.exercise_id
        }, {
          responseType: 'blob'
        })
        
        // 创建下载链接
        const blob = new Blob([response.data], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)
        const link = document.createElement('a')
        link.href = url
        link.download = `练习题目_${form.value.subject}_${new Date().toLocaleDateString()}.pdf`
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
        
      } catch (error) {
        console.error('生成PDF失败:', error)
        alert('生成PDF时发生错误，请稍后重试')
      } finally {
        isGeneratingPDF.value = false
      }
    }
    
    const generateAnalysis = async () => {
      if (!generatedExercise.value) return
      
      isGeneratingAnalysis.value = true
      
      try {
        const response = await api.post('/api/ai/generate-analysis', {
          exercise_id: generatedExercise.value.exercise_id
        })
        
        if (response.data.success) {
          analysisResult.value = response.data
        } else {
          alert('解析生成失败：' + response.data.message)
        }
      } catch (error) {
        console.error('生成解析失败:', error)
        alert('生成解析时发生错误，请稍后重试')
      } finally {
        isGeneratingAnalysis.value = false
      }
    }
    
    const resetGenerator = () => {
      generatedExercise.value = null
      analysisResult.value = null
    }
    
    const getQuestionTypeText = (type) => {
      const typeMap = {
        'choice': '选择题',
        'fill': '填空题',
        'solve': '解答题',
        'mixed': '混合题'
      }
      return typeMap[type] || type
    }
    
    return {
      form,
      knowledgePointsText,
      isGenerating,
      isGeneratingPDF,
      isGeneratingAnalysis,
      generatedExercise,
      analysisResult,
      isFormValid,
      generateExercise,
      generatePDF,
      generateAnalysis,
      resetGenerator,
      getQuestionTypeText
    }
  }
}
</script>

<style scoped>
.exercise-generator {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  color: white;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
}

.header p {
  font-size: 1.1rem;
  opacity: 0.9;
}

.generator-form {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.form-section {
  margin-bottom: 30px;
}

.form-section h3 {
  color: #333;
  margin-bottom: 20px;
  font-size: 1.3rem;
  border-bottom: 2px solid #667eea;
  padding-bottom: 10px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
  color: #555;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 2px solid #e1e5e9;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
}

.form-actions {
  text-align: center;
  margin-top: 30px;
}

.btn-generate {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.btn-generate:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-generate:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.generating-status {
  text-align: center;
  color: white;
  padding: 60px 20px;
}

.loading-animation {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.exercise-result {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.result-header {
  text-align: center;
  margin-bottom: 30px;
}

.result-header h3 {
  color: #333;
  font-size: 1.5rem;
  margin-bottom: 10px;
}

.questions-preview {
  margin-bottom: 30px;
}

.question-card {
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
  transition: border-color 0.3s;
}

.question-card:hover {
  border-color: #667eea;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.question-number {
  font-weight: 600;
  color: #667eea;
}

.question-type {
  background: #667eea;
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.9rem;
}

.question-content {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 15px;
  color: #333;
}

.question-options {
  margin-top: 15px;
}

.option {
  padding: 8px 0;
  color: #555;
}

.result-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-pdf,
.btn-analysis,
.btn-reset {
  padding: 12px 25px;
  border: none;
  border-radius: 20px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.btn-pdf {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.btn-analysis {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.btn-reset {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.btn-pdf:hover:not(:disabled),
.btn-analysis:hover:not(:disabled),
.btn-reset:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.btn-pdf:disabled,
.btn-analysis:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.analysis-result {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin-top: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.analysis-result h3 {
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.analysis-card {
  border: 2px solid #e1e5e9;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 20px;
}

.analysis-header {
  margin-bottom: 15px;
}

.analysis-content {
  line-height: 1.6;
}

.answer-section,
.steps-section,
.tips-section {
  margin-bottom: 15px;
}

.steps-section ol {
  margin-left: 20px;
  margin-top: 10px;
}

.steps-section li {
  margin-bottom: 5px;
}

@media (max-width: 768px) {
  .container {
    padding: 10px;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .generator-form,
  .exercise-result,
  .analysis-result {
    padding: 20px;
  }
  
  .result-actions {
    flex-direction: column;
  }
  
  .btn-pdf,
  .btn-analysis,
  .btn-reset {
    width: 100%;
  }
}
</style>