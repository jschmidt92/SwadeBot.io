import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import { characterRoutes } from '@/modules/character'
import { encounterRoutes } from '@/modules/encounter'
import { monsterRoutes } from '@/modules/monster'
import { useAuthStore } from '@/stores/auth.store'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    ...characterRoutes,
    ...encounterRoutes,
    ...monsterRoutes
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const token = localStorage.getItem('token')

  if (token) {
    authStore.setToken(token)
    authStore.setAuthenticated(true)
  } else {
    authStore.setToken('')
    authStore.setAuthenticated(false)
  }

  next()
})

export default router
