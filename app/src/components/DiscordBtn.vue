<template>
  <div>
    <button class="btn btn-outline-light" v-if="authStore.isAuthenticated" @click="authStore.logout">Logout</button>
    <button class="btn btn-outline-light" v-else @click="authStore.loginWithDiscord">Login with Discord</button>
  </div>
</template>


<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth.store'

const authStore = useAuthStore()

onMounted(async () => {
  authStore.retrieveTokenAndDiscordId()
})
</script>
