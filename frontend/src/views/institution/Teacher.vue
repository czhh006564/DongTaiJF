<template>
  <div class="institution-teacher">
    <h1>教师管理</h1>
    <div class="teacher-list">
      <div v-for="teacher in teachers" :key="teacher.id" class="teacher-card">
        <div class="teacher-avatar">
          <div class="default-avatar">{{ teacher.name.charAt(0) }}</div>
        </div>
        <div class="teacher-info">
          <h3>{{ teacher.name }}</h3>
          <p>科目: {{ teacher.subject }}</p>
          <p>班级数: {{ teacher.classCount }}</p>
          <p>学生数: {{ teacher.studentCount }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'InstitutionTeacher',
  setup() {
    const teachers = ref([])
    
    const loadTeachers = async () => {
      teachers.value = [
        { id: 1, name: '王老师', subject: '数学', classCount: 3, studentCount: 95 },
        { id: 2, name: '李老师', subject: '语文', classCount: 2, studentCount: 68 },
        { id: 3, name: '张老师', subject: '英语', classCount: 4, studentCount: 120 }
      ]
    }
    
    onMounted(() => {
      loadTeachers()
    })
    
    return {
      teachers
    }
  }
}
</script>

<style scoped>
.institution-teacher {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.teacher-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.teacher-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.teacher-avatar {
  width: 60px;
  height: 60px;
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
  font-size: 1.2rem;
}

.teacher-info h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
}

.teacher-info p {
  margin: 0.25rem 0;
  color: #666;
  font-size: 0.9rem;
}
</style>