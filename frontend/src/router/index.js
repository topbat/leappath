import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'dashboard', component: () => import('@/pages/Dashboard.vue'), meta: { title: '工作台' } },
  { path: '/login', name: 'login', component: () => import('@/pages/Login.vue'), meta: { title: '登录', plain: true } },

  // 简历中心
  { path: '/resume', redirect: '/resume/list' },
  { path: '/resume/list', name: 'resume-list', component: () => import('@/pages/resume/ResumeList.vue'), meta: { title: '简历中心' } },
  { path: '/resume/create', name: 'resume-create', component: () => import('@/pages/resume/ResumeEdit.vue'), meta: { title: '创建简历' } },
  { path: '/resume/:id', name: 'resume-edit', component: () => import('@/pages/resume/ResumeEdit.vue'), meta: { title: '编辑简历' } },
  { path: '/resume/:id/optimize', name: 'resume-optimize', component: () => import('@/pages/resume/ResumeOptimize.vue'), meta: { title: '简历优化' } },
  { path: '/resume/:id/score', name: 'resume-score', component: () => import('@/pages/resume/ResumeScore.vue'), meta: { title: '简历评分' } },

  // 模拟面试
  { path: '/interview', redirect: '/interview/setup' },
  { path: '/interview/setup', name: 'interview-setup', component: () => import('@/pages/interview/InterviewSetup.vue'), meta: { title: '模拟面试' } },
  { path: '/interview/session/:id', name: 'interview-session', component: () => import('@/pages/interview/InterviewSession.vue'), meta: { title: '面试中' } },
  { path: '/interview/report/:id', name: 'interview-report', component: () => import('@/pages/interview/InterviewReport.vue'), meta: { title: '面试报告' } },
  { path: '/interview/history', name: 'interview-history', component: () => import('@/pages/interview/InterviewHistory.vue'), meta: { title: '面试记录' } },

  // 职位匹配
  { path: '/jobs', redirect: '/jobs/list' },
  { path: '/jobs/list', name: 'jobs-list', component: () => import('@/pages/jobs/JobList.vue'), meta: { title: '职位匹配' } },
  { path: '/jobs/applications', name: 'jobs-applications', component: () => import('@/pages/jobs/Applications.vue'), meta: { title: '投递追踪' } },
  { path: '/jobs/:id', name: 'jobs-detail', component: () => import('@/pages/jobs/JobDetail.vue'), meta: { title: '职位详情' } },

  // 求职规划
  { path: '/plan', name: 'plan', component: () => import('@/pages/plan/Plan.vue'), meta: { title: '求职规划' } },

  // 公司画像
  { path: '/company', redirect: '/company/list' },
  { path: '/company/list', name: 'company-list', component: () => import('@/pages/company/CompanyList.vue'), meta: { title: '公司画像' } },
  { path: '/company/compare', name: 'company-compare', component: () => import('@/pages/company/CompanyCompare.vue'), meta: { title: '公司对比' } },
  { path: '/company/:id', name: 'company-detail', component: () => import('@/pages/company/CompanyDetail.vue'), meta: { title: '公司详情' } },

  // 求职准备
  { path: '/prepare', name: 'prepare', component: () => import('@/pages/prepare/Prepare.vue'), meta: { title: '求职准备' } },

  // 租房选址
  { path: '/rental', name: 'rental', component: () => import('@/pages/rental/Rental.vue'), meta: { title: '租房选址' } },

  // 个人中心
  { path: '/profile', name: 'profile', component: () => import('@/pages/Profile.vue'), meta: { title: '个人中心' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.afterEach((to) => {
  document.title = to.meta?.title ? `${to.meta.title} · 跃途 LeapPath` : '跃途 LeapPath'
})

export default router
