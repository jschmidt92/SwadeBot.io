<script setup lang="ts">
import Navbar from './components/Navbar.vue'
</script>

<template>
  <Navbar />
  <div class="container my-3">
    <router-view></router-view>
  </div>
</template>
