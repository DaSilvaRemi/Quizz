import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue'
import QuestionsManager from '../views/QuestionsManager.vue'
import ScorePage from '../views/ScorePage.vue'
import AdminLogin from '../views/AdminLogin.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/new-quiz',
      name: 'newQuiz',
      component: NewQuizPage
    },
    {
      path: '/questions',
      name: 'questions',
      component: QuestionsManager
    },
    {
      path: '/score',
      name: 'score',
      component: ScorePage
    },
    {
      path: '/login',
      name: 'login',
      component: AdminLogin
    },
  ]
})

export default router
