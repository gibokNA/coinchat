import { createRouter, createWebHistory } from 'vue-router'
import Main_Page from '../components/Main_Page.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Main_Page
    }
  ]
})

export default router
