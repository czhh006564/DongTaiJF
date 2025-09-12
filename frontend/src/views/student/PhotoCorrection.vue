<template>
  <div class="photo-correction-container">
    <div class="simple-nav">
      <h2>📸 AI拍照批阅</h2>
      <button @click="goBack" class="back-btn">← 返回</button>
    </div>
    
    <div class="correction-header">
      <h1>📸 AI拍照批阅</h1>
      <p class="header-desc">拍照上传作业或题目，AI智能批阅并提供详细解析</p>
    </div>

    <div class="correction-content">
      <!-- 上传区域 -->
      <div class="upload-section">
        <div class="upload-types">
          <button 
            :class="{ active: uploadType === 'homework' }"
            @click="uploadType = 'homework'"
            class="type-btn"
          >
            📚 作业批阅
          </button>
          <button 
            :class="{ active: uploadType === 'question' }"
            @click="uploadType = 'question'"
            class="type-btn"
          >
            ❓ 题目解答
          </button>
        </div>

        <div class="upload-area" :class="{ 'drag-over': isDragOver }">
          <input 
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="handleFileSelect"
            style="display: none"
            multiple
          />
          
          <div 
            @click="triggerFileSelect"
            @dragover.prevent="isDragOver = true"
            @dragleave.prevent="isDragOver = false"
            @drop.prevent="handleFileDrop"
            class="upload-zone"
          >
            <div v-if="!selectedImages.length" class="upload-placeholder">
              <div class="upload-icon">📷</div>
              <h3>点击或拖拽上传图片</h3>
              <p>支持 JPG、PNG、WEBP 格式，最多上传5张图片</p>
              <button class="upload-btn">选择图片</button>
            </div>
            
            <div v-else class="image-preview-grid">
              <div 
                v-for="(image, index) in selectedImages" 
                :key="index"
                class="image-preview-item"
              >
                <img :src="image.preview" :alt="`预览图 ${index + 1}`" />
                <button @click.stop="removeImage(index)" class="remove-btn">×</button>
                <div class="image-info">
                  <span class="image-name">{{ image.file.name }}</span>
                  <span class="image-size">{{ formatFileSize(image.file.size) }}</span>
                </div>
              </div>
              
              <div 
                v-if="selectedImages.length < 5"
                @click="triggerFileSelect"
                class="add-more-btn"
              >
                <div class="add-icon">+</div>
                <span>添加更多</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 批阅选项 -->
        <div v-if="selectedImages.length > 0" class="correction-options">
          <div class="option-group">
            <label>学科：</label>
            <select v-model="correctionConfig.subject">
              <option value="数学">数学</option>
              <option value="语文">语文</option>
              <option value="英语">英语</option>
              <option value="物理">物理</option>
              <option value="化学">化学</option>
              <option value="生物">生物</option>
            </select>
          </div>
          
          <div class="option-group">
            <label>年级：</label>
            <select v-model="correctionConfig.grade">
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
          
          <div class="option-group">
            <label>
              <input 
                type="checkbox" 
                v-model="correctionConfig.needExplanation"
              />
              需要详细解析
            </label>
          </div>
          
          <div class="option-group">
            <label>
              <input 
                type="checkbox" 
                v-model="correctionConfig.needSimilarQuestions"
              />
              生成相似题目
            </label>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div v-if="selectedImages.length > 0" class="submit-section">
          <button 
            @click="startCorrection"
            :disabled="isProcessing"
            class="submit-btn"
          >
            {{ isProcessing ? '正在批阅中...' : '开始AI批阅' }}
          </button>
        </div>
      </div>

      <!-- 批阅结果 -->
      <div v-if="correctionResults.length > 0" class="results-section">
        <h2>📋 批阅结果</h2>
        
        <div class="results-list">
          <div 
            v-for="(result, index) in correctionResults"
            :key="index"
            class="result-item"
          >
            <div class="result-header">
              <h3>图片 {{ index + 1 }} 批阅结果</h3>
            </div>
            
            <div class="result-content">
              <div class="original-image">
                <h4>原图片</h4>
                <img :src="result.originalImage" alt="原图片" />
              </div>
              
              <div class="correction-details">
                <h4>批阅详情</h4>

                <!-- 总体评价 -->
                <div v-if="result.overall_summary" class="overall-summary">
                    <h6>🤖 AI总体评价</h6>
                    <p>{{ result.overall_summary }}</p>
                </div>
                
                <!-- 识别的题目 -->
                <div class="recognized-questions">
                  <h5>📝 题目逐一解析</h5>
                  <div 
                    v-for="(question, qIndex) in result.corrections"
                    :key="qIndex"
                    class="question-item"
                  >
                    <div class="question-header">
                      <span class="question-number">第{{ qIndex + 1 }}题</span>
                      <span class="question-status" :class="question.is_correct ? 'correct' : 'incorrect'">
                        {{ question.is_correct ? '✅ 正确' : '❌ 错误' }}
                      </span>
                    </div>
                    
                    <div class="question-content">
                      <p class="question-text">{{ question.question }}</p>
                      
                      <div class="answer-comparison">
                        <div class="student-answer">
                          <strong>学生答案：</strong>
                          <span :class="question.is_correct ? 'correct-answer-text' : 'wrong-answer'">
                            {{ question.student_answer }}
                          </span>
                        </div>
                        
                        <div v-if="!question.is_correct" class="correct-answer">
                          <strong>正确答案：</strong>
                          <span class="standard-answer">{{ question.correct_answer }}</span>
                        </div>
                      </div>
                      
                      <!-- 解析 -->
                      <div v-if="correctionConfig.needExplanation && question.explanation" class="explanation">
                        <h6>💡 详细解析</h6>
                        <p>{{ question.explanation }}</p>
                      </div>

                      <!-- 知识点 -->
                      <div v-if="question.knowledge_points && question.knowledge_points.length > 0" class="knowledge-points">
                        <h6>🧠 涉及知识点</h6>
                        <div class="kps-container">
                          <span v-for="kp in question.knowledge_points" :key="kp" class="kp-tag">{{ kp }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- 相似题目 -->
                <div v-if="correctionConfig.needSimilarQuestions && result.similarQuestions" class="similar-questions">
                  <h5>🎯 相似练习题</h5>
                  <div 
                    v-for="(similar, sIndex) in result.similarQuestions"
                    :key="sIndex"
                    class="similar-question"
                  >
                    <p class="similar-content">{{ similar.content }}</p>
                    <button @click="showSimilarAnswer(similar)" class="show-answer-btn">
                      查看答案
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 操作按钮 -->
            <div class="result-actions">
              <button @click="downloadResult(result)" class="download-btn">
                📥 下载批阅报告
              </button>
              <button @click="generateMoreQuestions(result)" class="generate-btn">
                🎲 生成更多练习
              </button>
              <button @click="saveToErrorBook(result)" class="save-btn">
                📖 保存到错题本
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 处理进度 -->
      <div v-if="isProcessing" class="processing-overlay">
        <div class="processing-content">
          <div class="ai-brain-animation">
            <div class="brain-container">
              <div class="brain-core">
                <div class="neural-network">
                  <div class="neuron" v-for="i in 8" :key="i"></div>
                </div>
                <div class="thinking-waves">
                  <div class="wave" v-for="i in 3" :key="i"></div>
                </div>
              </div>
              <div class="model-label">qwen-vl-max</div>
            </div>
          </div>
          
          <h3>🤖 AI智能批阅系统</h3>
          
          <div class="status-display">
            <div class="status-icon">
              <span v-if="processingStatus.includes('连通')">🔗</span>
              <span v-else-if="processingStatus.includes('接收')">📥</span>
              <span v-else-if="processingStatus.includes('识别')">👁️</span>
              <span v-else-if="processingStatus.includes('分析')">🧠</span>
              <span v-else-if="processingStatus.includes('批改')">✏️</span>
              <span v-else-if="processingStatus.includes('整理')">📊</span>
              <span v-else-if="processingStatus.includes('发送')">📡</span>
              <span v-else-if="processingStatus.includes('返回')">📥</span>
              <span v-else-if="processingStatus.includes('完成')">✅</span>
              <span v-else>🤖</span>
            </div>
            <p class="status-text">{{ processingStatus }}</p>
          </div>
          
          <div class="thinking-process">
            <div class="process-steps">
              <div class="step" :class="{ active: processingStatus.includes('连通') }">
                <div class="step-icon">🔗</div>
                <span>模型连通</span>
              </div>
              <div class="step" :class="{ active: processingStatus.includes('接收') || processingStatus.includes('识别') }">
                <div class="step-icon">👁️</div>
                <span>视觉识别</span>
              </div>
              <div class="step" :class="{ active: processingStatus.includes('分析') || processingStatus.includes('批改') }">
                <div class="step-icon">🧠</div>
                <span>智能分析</span>
              </div>
              <div class="step" :class="{ active: processingStatus.includes('整理') || processingStatus.includes('返回') }">
                <div class="step-icon">📊</div>
                <span>生成报告</span>
              </div>
            </div>
          </div>
          
          <div class="progress-container">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: processingProgress + '%' }"></div>
              <div class="progress-glow" :style="{ width: processingProgress + '%' }"></div>
            </div>
            <span class="progress-text">{{ processingProgress }}%</span>
          </div>
          
          <div class="ai-info">
            <div class="model-info">
              <span class="model-name">通义千问 qwen-vl-max</span>
              <span class="model-desc">多模态视觉理解模型</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import imageCompression from 'browser-image-compression'

// 配置API客户端
const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  name: 'PhotoCorrection',
  setup() {
    const router = useRouter()
    
    // 返回功能
    const goBack = () => {
      router.push('/student/home')
    }
    
    const uploadType = ref('homework')
    const selectedImages = ref([])
    const isDragOver = ref(false)
    const isProcessing = ref(false)
    const processingStatus = ref('')
    const processingProgress = ref(0)
    const correctionResults = ref([])
    const fileInput = ref(null)
    
    const correctionConfig = reactive({
      subject: '数学',
      grade: '1年级',
      needExplanation: true,
      needSimilarQuestions: false
    })
    
    // 触发文件选择
    const triggerFileSelect = () => {
      fileInput.value?.click()
    }
    
    // 处理文件选择
    const handleFileSelect = (event) => {
      const files = Array.from(event.target.files)
      addImages(files)
    }
    
    // 处理拖拽上传
    const handleFileDrop = (event) => {
      isDragOver.value = false
      const files = Array.from(event.dataTransfer.files)
      addImages(files)
    }
    
    // 添加图片
    const addImages = (files) => {
      const imageFiles = files.filter(file => file.type.startsWith('image/'))
      
      if (selectedImages.value.length + imageFiles.length > 5) {
        alert('最多只能上传5张图片')
        return
      }
      
      imageFiles.forEach(file => {
        if (file.size > 10 * 1024 * 1024) {
          alert(`文件 ${file.name} 超过10MB限制`)
          return
        }
        
        const reader = new FileReader()
        reader.onload = (e) => {
          selectedImages.value.push({
            file,
            preview: e.target.result
          })
        }
        reader.readAsDataURL(file)
      })
    }
    
    // 移除图片
    const removeImage = (index) => {
      selectedImages.value.splice(index, 1)
    }
    
    // 格式化文件大小
    const formatFileSize = (bytes) => {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    // 检查AI模型连通性 - 真实API调用
    const checkAIConnection = async () => {
      try {
        processingStatus.value = '🔍 正在检测AI模型连通性...'
        await new Promise(resolve => setTimeout(resolve, 800))
        
        const response = await axios.get('http://localhost:8000/api/ai/test-connection', { 
          timeout: 15000 
        })
        
        if (response.data && response.data.success) {
          processingStatus.value = `✅ ${response.data.message}`
          await new Promise(resolve => setTimeout(resolve, 1000))
          return true
        } else {
          processingStatus.value = `❌ AI模型连通失败: ${response.data.message}`
          await new Promise(resolve => setTimeout(resolve, 2000))
          return false
        }
      } catch (error) {
        console.error('AI连通性检测失败:', error)
        processingStatus.value = `❌ AI模型连通检测失败: ${error.message}`
        await new Promise(resolve => setTimeout(resolve, 2000))
        return false
      }
    }

    // 显示AI思考过程
    const showAIThinkingProcess = async (imageIndex, totalImages) => {
      const thinkingSteps = [
        `🔍 qwen-vl-max正在接收第${imageIndex + 1}张图片数据...`,
        `🧠 AI模型开始视觉识别和理解图片内容...`,
        `📝 正在识别题目文字和学生答案...`,
        `🤔 AI正在分析题目类型和解题思路...`,
        `✏️ 模型正在批改答案并生成详细解析...`,
        `📊 正在整理批阅结果和学习建议...`
      ]
      
      for (let i = 0; i < thinkingSteps.length; i++) {
        processingStatus.value = thinkingSteps[i]
        processingProgress.value = Math.round(((imageIndex + (i + 1) / thinkingSteps.length) / totalImages) * 90)
        await new Promise(resolve => setTimeout(resolve, 1200)) // 每个步骤显示1.2秒
      }
    }

    // 开始批阅
    const startCorrection = async () => {
      if (selectedImages.value.length === 0) {
        alert('请先上传图片')
        return
      }
      
      isProcessing.value = true
      processingProgress.value = 0
      correctionResults.value = []
      
      try {
        // 首先检查AI连通性
        processingStatus.value = '🔍 初始化AI批阅系统...'
        await new Promise(resolve => setTimeout(resolve, 500))
        
        const isConnected = await checkAIConnection()
        
        if (!isConnected) {
          throw new Error('AI模型连通性检测失败，请检查网络连接和后端服务')
        }
        
        for (let i = 0; i < selectedImages.value.length; i++) {
          const image = selectedImages.value[i]
          
          // --- 图片压缩逻辑 ---
          processingStatus.value = `🔄 正在压缩第 ${i + 1} 张图片...`
          await new Promise(resolve => setTimeout(resolve, 500))

          const options = {
            maxSizeMB: 8, // 设置最大大小为8MB，小于API的10MB限制
            maxWidthOrHeight: 1920, // 限制最大宽度或高度
            useWebWorker: true,
            onProgress: (p) => {
              processingStatus.value = `🔄 正在压缩第 ${i + 1} 张图片... ${p}%`
            }
          }
          
          console.log(` compressing image ${image.file.name} with original size ${formatFileSize(image.file.size)}...`)
          const compressedFile = await imageCompression(image.file, options)
          console.log(` compressed image to ${formatFileSize(compressedFile.size)}`)
          
          // 将压缩后的File对象转换为Base64
          const compressedBase64 = await imageCompression.getDataUrlFromFile(compressedFile)
          // --- 图片压缩结束 ---

          // 显示AI思考过程
          await showAIThinkingProcess(i, selectedImages.value.length)
          
          console.log('🖼️ 发送压缩后的图片数据:', {
            type: uploadType.value,
            config: correctionConfig,
            imageSize: compressedBase64.length,
            imageType: compressedBase64.substring(0, 30) + '...'
          })
          
          // 显示正在调用API
          processingStatus.value = `📡 正在向qwen-vl-max发送批阅请求...`
          await new Promise(resolve => setTimeout(resolve, 800))
          
          // 真实的AI批阅API调用 - 使用压缩后的图片
          const response = await axios.post('http://localhost:8000/api/ai/photo-correction', {
            image: compressedBase64, // 使用压缩后的图片
            type: uploadType.value,
            config: correctionConfig
          }, {
            timeout: 120000 // 2分钟超时
          })
          
          console.log('📡 API响应:', response.data)
          
          processingStatus.value = `📥 AI模型返回批阅数据，正在解析结果...`
          await new Promise(resolve => setTimeout(resolve, 1000))
          
          if (response.data.success) {
            correctionResults.value.push({
              originalImage: image.preview,
              ...response.data.result
            })
            processingStatus.value = `✅ 第${i + 1}张图片批阅完成！`
            await new Promise(resolve => setTimeout(resolve, 800))
          } else {
            throw new Error(response.data.message || '批阅失败')
          }
        }
        
        processingStatus.value = '🎉 所有图片批阅完成！正在生成最终报告...'
        processingProgress.value = 100
        await new Promise(resolve => setTimeout(resolve, 1500))
        
        setTimeout(() => {
          isProcessing.value = false
        }, 500)
        
      } catch (error) {
        console.error('❌ 批阅失败:', error)
        console.error('❌ 错误详情:', error.response?.data || error.message)
        
        let errorMessage = '未知错误'
        if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
          errorMessage = 'AI模型响应超时，请稍后重试'
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message
        } else if (error.message) {
          errorMessage = error.message
        }
        
        // 显示真实的错误信息
        processingStatus.value = `❌ 批阅失败: ${errorMessage}`
        processingProgress.value = 0
        
        // 显示错误提示
        alert(`批阅失败: ${errorMessage}

建议：
1. 检查网络连接是否正常
2. 确认后端服务是否运行在 http://localhost:8000
3. 如果是超时问题，请稍后重试`)
        
        setTimeout(() => {
          isProcessing.value = false
        }, 3000)
      }
    }
    
    // 生成模拟批阅结果
    const generateMockResults = () => {
      selectedImages.value.forEach((image, index) => {
        const mockResult = {
          originalImage: image.preview,
          accuracy: Math.floor(Math.random() * 30) + 70, // 70-100%
          score: Math.floor(Math.random() * 20) + 80,
          totalScore: 100,
          questions: [
            {
              content: `${correctionConfig.subject}题目 ${index + 1}：计算下列表达式的值`,
              studentAnswer: '42',
              correctAnswer: '45',
              isCorrect: Math.random() > 0.3,
              explanation: correctionConfig.needExplanation ? '这道题考查的是基本运算能力，需要按照运算顺序进行计算...' : null,
              errorAnalysis: '计算过程中可能在加法运算时出现了错误',
              suggestion: `建议加强${correctionConfig.subject}基础运算练习`
            },
            {
              content: `${correctionConfig.subject}题目 ${index + 2}：解答应用题`,
              studentAnswer: '正确解答过程',
              correctAnswer: '正确解答过程',
              isCorrect: true,
              explanation: correctionConfig.needExplanation ? '解题思路正确，步骤清晰...' : null,
              suggestion: '继续保持良好的解题习惯'
            }
          ],
          similarQuestions: correctionConfig.needSimilarQuestions ? [
            {
              content: `类似题目1：计算 (3+5) × 2 - 4 = ?`,
              answer: '12'
            },
            {
              content: `类似题目2：小明有15个苹果，吃了3个，还剩多少个？`,
              answer: '12个'
            }
          ] : null
        }
        
        correctionResults.value.push(mockResult)
      })
    }
    
    // 显示相似题目答案
    const showSimilarAnswer = (similar) => {
      alert(`答案：${similar.answer}`)
    }
    
    // 下载批阅报告
    const downloadResult = (result) => {
      // 生成报告内容
      let reportContent = `AI批阅报告\n\n`
      reportContent += `总体评价：\n`
      reportContent += `准确率：${result.accuracy}%\n`
      reportContent += `得分：${result.score}/${result.totalScore}\n\n`
      
      result.questions.forEach((q, index) => {
        reportContent += `第${index + 1}题：\n`
        reportContent += `题目：${q.content}\n`
        reportContent += `学生答案：${q.studentAnswer}\n`
        reportContent += `正确答案：${q.correctAnswer}\n`
        reportContent += `结果：${q.isCorrect ? '正确' : '错误'}\n`
        if (q.explanation) reportContent += `解析：${q.explanation}\n`
        if (q.errorAnalysis) reportContent += `错误分析：${q.errorAnalysis}\n`
        if (q.suggestion) reportContent += `学习建议：${q.suggestion}\n`
        reportContent += `\n`
      })
      
      // 创建下载
      const blob = new Blob([reportContent], { type: 'text/plain;charset=utf-8' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `AI批阅报告_${new Date().toLocaleDateString()}.txt`
      a.click()
      URL.revokeObjectURL(url)
    }
    
    // 生成更多练习题
    const generateMoreQuestions = (result) => {
      router.push({
        path: '/student/exercise',
        query: {
          subject: correctionConfig.subject,
          grade: correctionConfig.grade,
          type: 'similar',
          source: 'photo-correction'
        }
      })
    }
    
    // 保存到错题本
    const saveToErrorBook = (result) => {
      const wrongQuestions = result.questions.filter(q => !q.isCorrect)
      if (wrongQuestions.length === 0) {
        alert('没有错题需要保存')
        return
      }
      
      // 这里应该调用保存错题的API
      alert(`已保存 ${wrongQuestions.length} 道错题到错题本`)
    }
    
    return {
      uploadType,
      selectedImages,
      isDragOver,
      isProcessing,
      processingStatus,
      processingProgress,
      correctionResults,
      correctionConfig,
      fileInput,
      goBack,
      triggerFileSelect,
      handleFileSelect,
      handleFileDrop,
      removeImage,
      formatFileSize,
      startCorrection,
      showSimilarAnswer,
      downloadResult,
      generateMoreQuestions,
      saveToErrorBook
    }
  }
}
</script>

<style scoped>
.photo-correction-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.simple-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.simple-nav h2 {
  margin: 0;
  font-size: 1.5rem;
}

.back-btn {
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.2);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s;
}

.back-btn:hover {
  background: rgba(255, 255, 255, 0.3);
}

.correction-header {
  text-align: center;
  padding: 2rem 1rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.correction-header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
}

.header-desc {
  margin: 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.correction-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.upload-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.upload-types {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  justify-content: center;
}

.type-btn {
  padding: 0.75rem 1.5rem;
  border: 2px solid #e9ecef;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1rem;
}

.type-btn.active {
  border-color: #007bff;
  background-color: #007bff;
  color: white;
}

.type-btn:hover:not(.active) {
  border-color: #007bff;
  color: #007bff;
}

.upload-area {
  border: 2px dashed #dee2e6;
  border-radius: 12px;
  transition: all 0.3s;
  margin-bottom: 2rem;
}

.upload-area.drag-over {
  border-color: #007bff;
  background-color: #f8f9fa;
}

.upload-zone {
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
}

.upload-placeholder {
  color: #6c757d;
}

.upload-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.upload-placeholder h3 {
  margin: 1rem 0 0.5rem 0;
  color: #495057;
}

.upload-placeholder p {
  margin: 0 0 1.5rem 0;
  font-size: 0.9rem;
}

.upload-btn {
  padding: 0.75rem 2rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
}

.upload-btn:hover {
  background-color: #0056b3;
}

.image-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  text-align: left;
}

.image-preview-item {
  position: relative;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  overflow: hidden;
  background: white;
}

.image-preview-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.remove-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 50%;
  background: rgba(220, 53, 69, 0.9);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
}

.image-info {
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.image-name {
  font-size: 0.8rem;
  font-weight: 500;
  color: #495057;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.image-size {
  font-size: 0.7rem;
  color: #6c757d;
}

.add-more-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  cursor: pointer;
  color: #6c757d;
  transition: all 0.3s;
}

.add-more-btn:hover {
  border-color: #007bff;
  color: #007bff;
}

.add-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.correction-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.option-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.option-group label {
  font-weight: 500;
  color: #495057;
  white-space: nowrap;
}

.option-group select {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #dee2e6;
  border-radius: 4px;
}

.option-group input[type="checkbox"] {
  margin-right: 0.5rem;
}

.submit-section {
  text-align: center;
}

.submit-btn {
  padding: 1rem 3rem;
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.results-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.results-section h2 {
  margin: 0 0 2rem 0;
  color: #333;
  text-align: center;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.result-item {
  border: 1px solid #dee2e6;
  border-radius: 12px;
  overflow: hidden;
}

.result-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-header h3 {
  margin: 0;
}

.result-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.9rem;
}

.result-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  padding: 1.5rem;
}

.original-image h4 {
  margin: 0 0 1rem 0;
  color: #495057;
}

.original-image img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.correction-details h4 {
  margin: 0 0 1rem 0;
  color: #495057;
}

.recognized-questions h5 {
  margin: 0 0 1rem 0;
  color: #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.question-item {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.question-number {
  font-weight: 500;
  color: #495057;
}

.question-status.correct {
  color: #28a745;
  font-weight: 500;
}

.question-status.incorrect {
  color: #dc3545;
  font-weight: 500;
}

.question-text {
  margin: 0 0 1rem 0;
  color: #333;
  font-weight: 500;
}

.answer-comparison {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.correct-answer-text {
  color: #28a745;
  font-weight: 500;
}

.wrong-answer {
  color: #dc3545;
  font-weight: 500;
}

.standard-answer {
  color: #28a745;
  font-weight: 500;
}

.explanation, .error-analysis, .suggestion {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 6px;
}

.explanation {
  background-color: #e3f2fd;
  border-left: 4px solid #2196f3;
}

.error-analysis {
  background-color: #ffebee;
  border-left: 4px solid #f44336;
}

.suggestion {
  background-color: #e8f5e8;
  border-left: 4px solid #4caf50;
}

.overall-summary {
  background-color: #f8f9fa;
  border-left: 4px solid #667eea;
  padding: 1rem;
  margin-bottom: 2rem;
  border-radius: 6px;
}
.overall-summary h6 {
  margin: 0 0 0.5rem 0;
  color: #667eea;
}
.overall-summary p {
  margin: 0;
  line-height: 1.6;
}

.knowledge-points {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f1f3f5;
  border-left: 4px solid #fd7e14;
  border-radius: 6px;
}
.knowledge-points h6 {
  margin: 0 0 0.5rem 0;
  color: #333;
}
.kps-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.kp-tag {
  background-color: #fd7e14;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
}

.explanation h6, .error-analysis h6, .suggestion h6 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 0.9rem;
}

.explanation p, .error-analysis p, .suggestion p {
  margin: 0;
  color: #555;
  line-height: 1.5;
}

.similar-questions {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.similar-questions h5 {
  margin: 0 0 1rem 0;
  color: #333;
}

.similar-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: white;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.similar-content {
  margin: 0;
  flex: 1;
  color: #333;
}

.show-answer-btn {
  padding: 0.5rem 1rem;
  background-color: #17a2b8;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
}

.show-answer-btn:hover {
  background-color: #138496;
}

.result-actions {
  display: flex;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background-color: #f8f9fa;
  justify-content: center;
}

.result-actions button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.download-btn {
  background-color: #6c757d;
  color: white;
}

.download-btn:hover {
  background-color: #545b62;
}

.generate-btn {
  background-color: #fd7e14;
  color: white;
}

.generate-btn:hover {
  background-color: #e8590c;
}

.save-btn {
  background-color: #20c997;
  color: white;
}

.save-btn:hover {
  background-color: #1aa179;
}

.processing-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 0, 0, 0.9), rgba(30, 30, 60, 0.9));
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  backdrop-filter: blur(10px);
}

.processing-content {
  background: linear-gradient(145deg, #ffffff, #f8f9fa);
  padding: 3rem;
  border-radius: 20px;
  text-align: center;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.ai-brain-animation {
  margin-bottom: 2rem;
}

.brain-container {
  position: relative;
  display: inline-block;
}

.brain-core {
  width: 80px;
  height: 80px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  border-radius: 50%;
  position: relative;
  margin: 0 auto 1rem;
  animation: brainPulse 2s ease-in-out infinite;
  display: flex;
  align-items: center;
  justify-content: center;
}

.neural-network {
  position: absolute;
  width: 100%;
  height: 100%;
}

.neuron {
  position: absolute;
  width: 6px;
  height: 6px;
  background: #fff;
  border-radius: 50%;
  animation: neuronFlash 1.5s ease-in-out infinite;
}

.neuron:nth-child(1) { top: 20%; left: 30%; animation-delay: 0s; }
.neuron:nth-child(2) { top: 30%; right: 25%; animation-delay: 0.2s; }
.neuron:nth-child(3) { bottom: 30%; left: 25%; animation-delay: 0.4s; }
.neuron:nth-child(4) { bottom: 20%; right: 30%; animation-delay: 0.6s; }
.neuron:nth-child(5) { top: 50%; left: 15%; animation-delay: 0.8s; }
.neuron:nth-child(6) { top: 50%; right: 15%; animation-delay: 1s; }
.neuron:nth-child(7) { top: 15%; left: 50%; animation-delay: 1.2s; }
.neuron:nth-child(8) { bottom: 15%; left: 50%; animation-delay: 1.4s; }

.thinking-waves {
  position: absolute;
  top: -10px;
  left: -10px;
  right: -10px;
  bottom: -10px;
}

.wave {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 50%;
  animation: waveExpand 3s ease-out infinite;
}

.wave:nth-child(1) { animation-delay: 0s; }
.wave:nth-child(2) { animation-delay: 1s; }
.wave:nth-child(3) { animation-delay: 2s; }

.model-label {
  font-size: 0.8rem;
  color: #667eea;
  font-weight: 600;
  margin-top: 0.5rem;
}

.status-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 1.5rem 0;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 12px;
  border: 1px solid rgba(102, 126, 234, 0.2);
}

.status-icon {
  font-size: 1.5rem;
  animation: iconBounce 1s ease-in-out infinite;
}

.status-text {
  margin: 0;
  color: #333;
  font-weight: 500;
  font-size: 1rem;
}

.thinking-process {
  margin: 2rem 0;
}

.process-steps {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  opacity: 0.4;
  transition: all 0.3s ease;
}

.step.active {
  opacity: 1;
  transform: scale(1.1);
}

.step-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(45deg, #f093fb, #f5576c);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: white;
  animation: stepPulse 2s ease-in-out infinite;
}

.step.active .step-icon {
  animation: stepActive 1s ease-in-out infinite;
}

.step span {
  font-size: 0.8rem;
  color: #666;
  font-weight: 500;
}

.step.active span {
  color: #333;
  font-weight: 600;
}

.progress-container {
  margin: 2rem 0 1rem;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
  position: relative;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 4px;
  transition: width 0.3s ease;
  position: relative;
}

.progress-glow {
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  border-radius: 4px;
  animation: progressGlow 2s ease-in-out infinite;
}

.progress-text {
  font-size: 0.9rem;
  color: #667eea;
  font-weight: 600;
}

.ai-info {
  margin-top: 1.5rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.05);
  border-radius: 8px;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.model-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.model-name {
  font-weight: 600;
  color: #667eea;
  font-size: 1rem;
}

.model-desc {
  font-size: 0.8rem;
  color: #666;
}

@keyframes brainPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

@keyframes neuronFlash {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

@keyframes waveExpand {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

@keyframes iconBounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

@keyframes stepPulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
}

@keyframes stepActive {
  0%, 100% { 
    transform: scale(1.1);
    box-shadow: 0 0 0 0 rgba(240, 147, 251, 0.7);
  }
  50% { 
    transform: scale(1.2);
    box-shadow: 0 0 0 10px rgba(240, 147, 251, 0);
  }
}

@keyframes progressGlow {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.processing-content h3 {
  margin: 0 0 1rem 0;
  color: #333;
}

.processing-content p {
  margin: 0 0 2rem 0;
  color: #666;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background-color: #007bff;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 0.9rem;
  color: #666;
}

@media (max-width: 768px) {
  .correction-content {
    padding: 1rem;
  }
  
  .upload-section, .results-section {
    padding: 1rem;
  }
  
  .result-content {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .correction-options {
    grid-template-columns: 1fr;
  }
  
  .result-actions {
    flex-direction: column;
  }
  
  .upload-types {
    flex-direction: column;
  }
}
</style>