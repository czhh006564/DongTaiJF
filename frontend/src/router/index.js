import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// 路由组件懒加载
const Login = () => import('@/views/auth/Login-simple.vue')
const Register = () => import('@/views/auth/Register.vue')
const Dashboard = () => import('@/views/Dashboard.vue')
const TestLogin = () => import('@/views/TestLogin.vue')

// 学生端路由
const StudentHome = () => import('@/views/student/Home.vue')
const StudentExercise = () => import('@/views/student/Exercise.vue')
const StudentReport = () => import('@/views/student/Report.vue')
const StudentProfile = () => import('@/views/student/Profile.vue')

// 家长端路由
const ParentHome = () => import('@/views/parent/Home.vue')
const ParentReport = () => import('@/views/parent/Report.vue')
const ParentSettings = () => import('@/views/parent/Settings.vue')

// 老师端路由
const TeacherHome = () => import('@/views/teacher/Home.vue')
const TeacherClass = () => import('@/views/teacher/Class.vue')
const TeacherStudent = () => import('@/views/teacher/Student.vue')

// 机构端路由
const InstitutionHome = () => import('@/views/institution/Home.vue')
const InstitutionTeacher = () => import('@/views/institution/Teacher.vue')
const InstitutionReport = () => import('@/views/institution/Report.vue')

// 超级管理员路由
const AdminHome = () => import('@/views/admin/Home.vue')
const AdminUsers = () => import('@/views/admin/Users.vue')
const AdminAIConfig = () => import('@/views/admin/AIConfig.vue')
const AdminSystem = () => import('@/views/admin/System.vue')

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { requiresAuth: false }
  },
  {
    path: '/test-login',
    name: 'TestLogin',
    component: TestLogin,
    meta: { requiresAuth: false }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  
  // 学生端路由
  {
    path: '/student',
    name: 'Student',
    redirect: '/student/home',
    meta: { requiresAuth: true, roles: ['student'] },
    children: [
      {
        path: 'home',
        name: 'StudentHome',
        component: StudentHome
      },
      {
        path: 'exercise',
        name: 'StudentExercise',
        component: StudentExercise
      },
      {
        path: 'report',
        name: 'StudentReport',
        component: StudentReport
      },
      {
        path: 'profile',
        name: 'StudentProfile',
        component: StudentProfile
      }
    ]
  },
  
  // 家长端路由
  {
    path: '/parent',
    name: 'Parent',
    redirect: '/parent/home',
    meta: { requiresAuth: true, roles: ['parent'] },
    children: [
      {
        path: 'home',
        name: 'ParentHome',
        component: ParentHome
      },
      {
        path: 'report',
        name: 'ParentReport',
        component: ParentReport
      },
      {
        path: 'settings',
        name: 'ParentSettings',
        component: ParentSettings
      }
    ]
  },
  
  // 老师端路由
  {
    path: '/teacher',
    name: 'Teacher',
    redirect: '/teacher/home',
    meta: { requiresAuth: true, roles: ['teacher'] },
    children: [
      {
        path: 'home',
        name: 'TeacherHome',
        component: TeacherHome
      },
      {
        path: 'class',
        name: 'TeacherClass',
        component: TeacherClass
      },
      {
        path: 'student',
        name: 'TeacherStudent',
        component: TeacherStudent
      }
    ]
  },
  
  // 机构端路由
  {
    path: '/institution',
    name: 'Institution',
    redirect: '/institution/home',
    meta: { requiresAuth: true, roles: ['institution'] },
    children: [
      {
        path: 'home',
        name: 'InstitutionHome',
        component: InstitutionHome
      },
      {
        path: 'teacher',
        name: 'InstitutionTeacher',
        component: InstitutionTeacher
      },
      {
        path: 'report',
        name: 'InstitutionReport',
        component: InstitutionReport
      }
    ]
  },
  
  // 超级管理员路由
  {
    path: '/admin',
    name: 'Admin',
    redirect: '/admin/home',
    meta: { requiresAuth: true, roles: ['super_admin'] },
    children: [
      {
        path: 'home',
        name: 'AdminHome',
        component: AdminHome
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers
      },
      {
        path: 'ai-config',
        name: 'AdminAIConfig',
        component: AdminAIConfig
      },
      {
        path: 'system',
        name: 'AdminSystem',
        component: AdminSystem
      }
    ]
  },
  
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
    return
  }
  
  // 检查角色权限
  if (to.meta.roles && to.meta.roles.length > 0) {
    if (!userStore.hasRole(to.meta.roles)) {
      // 根据用户角色重定向到对应的首页
      const userRole = userStore.userInfo?.role
      switch (userRole) {
        case 'student':
          next('/student/home')
          break
        case 'parent':
          next('/parent/home')
          break
        case 'teacher':
          next('/teacher/home')
          break
        case 'institution':
          next('/institution/home')
          break
        case 'super_admin':
          next('/admin/home')
          break
        default:
          next('/dashboard')
      }
      return
    }
  }
  
  // 已登录用户访问登录页面，重定向到仪表板
  if ((to.name === 'Login' || to.name === 'Register') && userStore.isLoggedIn) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router