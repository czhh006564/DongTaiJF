<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h1>欢迎使用精准动态教辅系统</h1>
      <p>您好，{{ userStore.userInfo?.real_name }}！</p>
    </div>
    
    <div class="role-navigation">
      <el-card class="role-card" shadow="hover">
        <div class="role-info">
          <el-icon class="role-icon"><User /></el-icon>
          <h3>当前角色：{{ getRoleDisplayName(userStore.userRole) }}</h3>
          <p>{{ getRoleDescription(userStore.userRole) }}</p>
        </div>
        
        <el-button 
          type="primary" 
          size="large"
          @click="navigateToRoleHome"
        >
          进入{{ getRoleDisplayName(userStore.userRole) }}工作台
        </el-button>
      </el-card>
    </div>
    
    <div class="quick-actions">
      <h2>快速操作</h2>
      <div class="actions-grid">
        <el-card 
          v-for="action in getQuickActions()" 
          :key="action.name"
          class="action-card"
          shadow="hover"
          @click="action.handler"
        >
          <div class="action-content">
            <el-icon class="action-icon" :style="{ color: action.color }">
              <component :is="action.icon" />
            </el-icon>
            <h4>{{ action.name }}</h4>
            <p>{{ action.description }}</p>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { 
  User, 
  Document, 
  DataAnalysis, 
  Setting,
  EditPen,
  PieChart,
  UserFilled,
  Management
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()

// 获取角色显示名称
const getRoleDisplayName = (role) => {
  const roleMap = {
    'student': '学生',
    'parent': '家长',
    'teacher': '老师',
    'institution': '机构',
    'super_admin': '超级管理员'
  }
  return roleMap[role] || '用户'
}

// 获取角色描述
const getRoleDescription = (role) => {
  const descMap = {
    'student': '完成练习，查看学习报告，提升学习效果',
    'parent': '监督孩子学习，查看学习进度和报告',
    'teacher': '管理班级学生，布置作业，查看教学效果',
    'institution': '管理多个班级和老师，统计教学数据',
    'super_admin': '系统管理，用户管理，AI模型配置'
  }
  return descMap[role] || '使用系统功能'
}

// 导航到角色首页
const navigateToRoleHome = () => {
  const role = userStore.userRole
  const routeMap = {
    'student': '/student/home',
    'parent': '/parent/home',
    'teacher': '/teacher/home',
    'institution': '/institution/home',
    'super_admin': '/admin/home'
  }
  
  const route = routeMap[role]
  if (route) {
    router.push(route)
  }
}

// 获取快速操作
const getQuickActions = () => {
  const role = userStore.userRole
  
  const actionsMap = {
    'student': [
      {
        name: '拍照批阅',
        description: '上传作业照片进行AI批阅',
        icon: 'EditPen',
        color: '#409EFF',
        handler: () => router.push('/student/exercise')
      },
      {
        name: '动态练习',
        description: '生成个性化练习题目',
        icon: 'Document',
        color: '#67C23A',
        handler: () => router.push('/student/exercise')
      },
      {
        name: '学习报告',
        description: '查看学习进度和分析报告',
        icon: 'DataAnalysis',
        color: '#E6A23C',
        handler: () => router.push('/student/report')
      }
    ],
    'parent': [
      {
        name: '孩子报告',
        description: '查看孩子的学习情况',
        icon: 'PieChart',
        color: '#67C23A',
        handler: () => router.push('/parent/report')
      },
      {
        name: '学习设置',
        description: '设置学习提醒和目标',
        icon: 'Setting',
        color: '#409EFF',
        handler: () => router.push('/parent/settings')
      }
    ],
    'teacher': [
      {
        name: '班级管理',
        description: '管理班级学生信息',
        icon: 'UserFilled',
        color: '#E6A23C',
        handler: () => router.push('/teacher/class')
      },
      {
        name: '学生分析',
        description: '查看学生学习数据',
        icon: 'DataAnalysis',
        color: '#409EFF',
        handler: () => router.push('/teacher/student')
      }
    ],
    'institution': [
      {
        name: '老师管理',
        description: '管理机构内的老师',
        icon: 'Management',
        color: '#F56C6C',
        handler: () => router.push('/institution/teacher')
      },
      {
        name: '教学报告',
        description: '查看整体教学效果',
        icon: 'PieChart',
        color: '#409EFF',
        handler: () => router.push('/institution/report')
      }
    ],
    'super_admin': [
      {
        name: '用户管理',
        description: '管理系统所有用户',
        icon: 'UserFilled',
        color: '#909399',
        handler: () => router.push('/admin/users')
      },
      {
        name: 'AI配置',
        description: '配置AI模型和参数',
        icon: 'Setting',
        color: '#409EFF',
        handler: () => router.push('/admin/ai-config')
      },
      {
        name: '系统设置',
        description: '系统参数和配置管理',
        icon: 'Management',
        color: '#E6A23C',
        handler: () => router.push('/admin/system')
      }
    ]
  }
  
  return actionsMap[role] || []
}
</script>

<style lang="scss" scoped>
.dashboard-container {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 32px;
  
  h1 {
    font-size: 32px;
    font-weight: 600;
    color: #303133;
    margin-bottom: 8px;
  }
  
  p {
    font-size: 16px;
    color: #606266;
  }
}

.role-navigation {
  margin-bottom: 40px;
  
  .role-card {
    max-width: 600px;
    margin: 0 auto;
    text-align: center;
    padding: 24px;
    
    .role-info {
      margin-bottom: 24px;
      
      .role-icon {
        font-size: 48px;
        color: #409EFF;
        margin-bottom: 16px;
      }
      
      h3 {
        font-size: 24px;
        font-weight: 500;
        color: #303133;
        margin-bottom: 8px;
      }
      
      p {
        color: #606266;
        font-size: 14px;
      }
    }
  }
}

.quick-actions {
  h2 {
    font-size: 24px;
    font-weight: 500;
    color: #303133;
    margin-bottom: 24px;
    text-align: center;
  }
  
  .actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 24px;
    
    .action-card {
      cursor: pointer;
      transition: transform 0.2s ease;
      
      &:hover {
        transform: translateY(-4px);
      }
      
      .action-content {
        text-align: center;
        padding: 16px;
        
        .action-icon {
          font-size: 40px;
          margin-bottom: 16px;
        }
        
        h4 {
          font-size: 18px;
          font-weight: 500;
          color: #303133;
          margin-bottom: 8px;
        }
        
        p {
          color: #606266;
          font-size: 14px;
          line-height: 1.5;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 16px;
  }
  
  .dashboard-header h1 {
    font-size: 24px;
  }
  
  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>