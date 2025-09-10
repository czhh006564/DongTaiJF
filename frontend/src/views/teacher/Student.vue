<template>
  <div class="teacher-student">
    <h1>学生管理</h1>
    <div class="student-list">
      <div v-for="student in students" :key="student.id" class="student-card">
        <div class="student-avatar">
          <div class="default-avatar">{{ student.name.charAt(0) }}</div>
        </div>
        <div class="student-info">
          <h3>{{ student.name }}</h3>
          <p>班级: {{ student.class }}</p>
          <p>正确率: {{ student.accuracy }}%</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'TeacherStudent',
  setup() {
    const students = ref([])
    
    const loadStudents = async () => {
      students.value = [
        { id: 1, name: '张小明', class: '九年级一班', accuracy: 85 },
        { id: 2, name: '李小红', class: '九年级一班', accuracy: 92 },
        { id: 3, name: '王小华', class: '九年级二班', accuracy: 78 }
      ]
    }
    
    onMounted(() => {
      loadStudents()
    })
    
    return {
      students
    }
  }
}
</script>

<style scoped>
.teacher-student {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.student-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.student-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.student-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  overflow: hidden;
}

.default-avatar {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #007bff;
  color: white;
  font-weight: bold;
}

.student-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.student-info p {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}
</style>