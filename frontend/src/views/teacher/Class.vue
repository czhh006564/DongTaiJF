<template>
  <div class="teacher-class">
    <h1>班级管理</h1>
    <div class="class-list">
      <div v-for="cls in classes" :key="cls.id" class="class-card">
        <h3>{{ cls.name }}</h3>
        <p>学生人数: {{ cls.studentCount }}</p>
        <p>平均成绩: {{ cls.averageScore }}%</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  name: 'TeacherClass',
  setup() {
    const classes = ref([])
    
    const loadClasses = async () => {
      classes.value = [
        { id: 1, name: '九年级一班', studentCount: 35, averageScore: 85 },
        { id: 2, name: '九年级二班', studentCount: 32, averageScore: 88 },
        { id: 3, name: '九年级三班', studentCount: 38, averageScore: 82 }
      ]
    }
    
    onMounted(() => {
      loadClasses()
    })
    
    return {
      classes
    }
  }
}
</script>

<style scoped>
.teacher-class {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.class-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.class-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.class-card h3 {
  margin: 0 0 1rem 0;
  color: #333;
}

.class-card p {
  margin: 0.5rem 0;
  color: #666;
}
</style>