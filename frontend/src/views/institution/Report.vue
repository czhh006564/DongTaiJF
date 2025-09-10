<template>
  <div class="institution-report">
    <h1>教学报告</h1>
    <div class="report-overview">
      <div class="overview-card">
        <h3>整体表现</h3>
        <p>平均成绩: {{ reportData.averageScore }}%</p>
        <p>完成练习: {{ reportData.totalExercises }}题</p>
      </div>
      
      <div class="overview-card">
        <h3>教师表现</h3>
        <p>优秀教师: {{ reportData.excellentTeachers }}人</p>
        <p>活跃教师: {{ reportData.activeTeachers }}人</p>
      </div>
      
      <div class="overview-card">
        <h3>学生表现</h3>
        <p>优秀学生: {{ reportData.excellentStudents }}人</p>
        <p>进步学生: {{ reportData.improvedStudents }}人</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'InstitutionReport',
  setup() {
    const reportData = ref({})
    
    const loadReport = async () => {
      reportData.value = {
        averageScore: 86,
        totalExercises: 12500,
        excellentTeachers: 18,
        activeTeachers: 25,
        excellentStudents: 125,
        improvedStudents: 280
      }
    }
    
    onMounted(() => {
      loadReport()
    })
    
    return {
      reportData
    }
  }
}
</script>

<style scoped>
.institution-report {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.report-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.overview-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.overview-card h3 {
  margin: 0 0 1rem 0;
  color: #333;
}

.overview-card p {
  margin: 0.5rem 0;
  color: #666;
}
</style>