<template>
  <div class="admin-users">
    <div class="users-header">
      <h1>用户管理</h1>
      <div class="filter-controls">
        <select v-model="filterRole">
          <option value="">所有角色</option>
          <option value="student">学生</option>
          <option value="parent">家长</option>
          <option value="teacher">教师</option>
          <option value="institution">机构</option>
        </select>
        <input v-model="searchQuery" type="text" placeholder="搜索用户..." />
      </div>
    </div>
    
    <div class="users-table">
      <table>
        <thead>
          <tr>
            <th>用户名</th>
            <th>邮箱</th>
            <th>角色</th>
            <th>注册时间</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>
              <span class="role-badge" :class="user.role">
                {{ getRoleText(user.role) }}
              </span>
            </td>
            <td>{{ user.createdAt }}</td>
            <td>
              <span class="status-badge" :class="user.status">
                {{ user.status === 'active' ? '活跃' : '禁用' }}
              </span>
            </td>
            <td>
              <button @click="toggleUserStatus(user)" class="action-btn">
                {{ user.status === 'active' ? '禁用' : '启用' }}
              </button>
              <button @click="deleteUser(user)" class="action-btn danger">删除</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'

export default {
  name: 'AdminUsers',
  setup() {
    const users = ref([])
    const filterRole = ref('')
    const searchQuery = ref('')
    
    const filteredUsers = computed(() => {
      let filtered = users.value
      
      if (filterRole.value) {
        filtered = filtered.filter(user => user.role === filterRole.value)
      }
      
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(user => 
          user.username.toLowerCase().includes(query) ||
          user.email.toLowerCase().includes(query)
        )
      }
      
      return filtered
    })
    
    const loadUsers = async () => {
      users.value = [
        {
          id: 1,
          username: 'student1',
          email: 'student1@example.com',
          role: 'student',
          createdAt: '2024-01-15',
          status: 'active'
        },
        {
          id: 2,
          username: 'teacher1',
          email: 'teacher1@example.com',
          role: 'teacher',
          createdAt: '2024-01-10',
          status: 'active'
        },
        {
          id: 3,
          username: 'parent1',
          email: 'parent1@example.com',
          role: 'parent',
          createdAt: '2024-01-12',
          status: 'inactive'
        }
      ]
    }
    
    const getRoleText = (role) => {
      const roleMap = {
        student: '学生',
        parent: '家长',
        teacher: '教师',
        institution: '机构',
        admin: '管理员'
      }
      return roleMap[role] || role
    }
    
    const toggleUserStatus = (user) => {
      user.status = user.status === 'active' ? 'inactive' : 'active'
      alert(`用户 ${user.username} 已${user.status === 'active' ? '启用' : '禁用'}`)
    }
    
    const deleteUser = (user) => {
      if (confirm(`确定要删除用户 ${user.username} 吗？`)) {
        const index = users.value.findIndex(u => u.id === user.id)
        if (index > -1) {
          users.value.splice(index, 1)
          alert('用户已删除')
        }
      }
    }
    
    onMounted(() => {
      loadUsers()
    })
    
    return {
      users,
      filterRole,
      searchQuery,
      filteredUsers,
      getRoleText,
      toggleUserStatus,
      deleteUser
    }
  }
}
</script>

<style scoped>
.admin-users {
  padding: 1.5rem;
  max-width: 1200px;
  margin: 0 auto;
}

.users-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.filter-controls {
  display: flex;
  gap: 1rem;
}

.filter-controls select,
.filter-controls input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.users-table {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #eee;
}

th {
  background-color: #f8f9fa;
  font-weight: 500;
  color: #333;
}

.role-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.role-badge.student {
  background-color: #e3f2fd;
  color: #1976d2;
}

.role-badge.parent {
  background-color: #f3e5f5;
  color: #7b1fa2;
}

.role-badge.teacher {
  background-color: #e8f5e8;
  color: #388e3c;
}

.role-badge.institution {
  background-color: #fff3e0;
  color: #f57c00;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-badge.active {
  background-color: #d4edda;
  color: #155724;
}

.status-badge.inactive {
  background-color: #f8d7da;
  color: #721c24;
}

.action-btn {
  padding: 0.25rem 0.5rem;
  margin-right: 0.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  background-color: #007bff;
  color: white;
}

.action-btn:hover {
  background-color: #0056b3;
}

.action-btn.danger {
  background-color: #dc3545;
}

.action-btn.danger:hover {
  background-color: #c82333;
}

@media (max-width: 768px) {
  .users-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-controls {
    justify-content: center;
  }
  
  .users-table {
    overflow-x: auto;
  }
  
  table {
    min-width: 600px;
  }
}
</style>