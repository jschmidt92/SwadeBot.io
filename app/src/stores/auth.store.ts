import { defineStore } from 'pinia'

const BASE_URL = 'http://135.135.196.140/api'
// const BASE_URL = 'http://swadebot.api:8000/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    token: '',
    discordId: '',
  }),
  getters: {
    hasToken: (state) => {
      return !!state.token
    }
  },
  actions: {
    async loginWithDiscord() {
      try {
        window.location.href = "https://discord.com/api/oauth2/authorize?client_id=1127048736758050878&redirect_uri=http%3A%2F%2F135.135.196.140%2Fapi%2Foauth%2Fcallback&response_type=code&scope=identify"
      } catch (error) {
        console.error(error)
      }
    },
    logout() {
      this.setAuthenticated(false)
      localStorage.removeItem('token')
      localStorage.removeItem('discordId')
      window.location.href = '/'
    },
    setAuthenticated(authenticated: boolean) {
      this.isAuthenticated = authenticated
    },
    setToken(token: string) {
      this.token = token
      this.isAuthenticated = true
      localStorage.setItem('token', token)
    },
    setDiscordId(discordId: string) {
      this.discordId = discordId
      localStorage.setItem('discordId', discordId)
    },
    retrieveTokenAndDiscordId() {
      const url = new URL(window.location.href)
      const token = url.searchParams.get('token')
      const discordId = url.searchParams.get('discord_id')
      if (token) {
        this.setToken(token)
      }
      if (discordId) {
        this.setDiscordId(discordId)
      }
    },
    getUsername: async function (): Promise<string | null> {
      const id = localStorage.getItem('discordId')
      if (!id) {
        console.error('No Discord ID found in local storage.')
        return null
      }

      const response = await fetch(`${BASE_URL}/users/${id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`
        }
      })

      if (!response.ok) {
        console.error('Failed to get username:', response)
        return null
      }

      const user = await response.json()
      return user.username
    }
  }
})