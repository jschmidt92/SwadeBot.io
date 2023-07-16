<script setup lang="ts">
import banner from '@/assets/banner.jpg'
import avatar from '@/assets/avatar.jpg'

defineProps<{ to: any, name: string }>()
</script>

<template>
  <div class="card position-relative rounded-0 mb-1">
    <img :src="banner" class="card-img-top rounded-0" alt="Character Banner" style="object-fit: cover; height: 8rem !important;">
    <div class="card-avatar position-absolute p-2 rounded-circle">
      <div class="d-flex align-items-center">
        <img :src="avatar" class="rounded-circle me-2" alt="Character Avatar" style="width: 4rem; height: 4rem;">
        <h5 class="card-title mb-0 text-light">{{ name }}</h5>
      </div>
    </div>
    <div class="card-footer" style="z-index: 10 !important;">
      <div class="d-flex justify-content-around">
        <RouterLink class="link-dark text-decoration-none" :to="to">View</RouterLink>
        <RouterLink class="link-dark text-decoration-none" :to="to">Update</RouterLink>
        <RouterLink class="link-dark text-decoration-none" :to="to">Delete</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  position: relative;
}

.card-avatar {
  position: absolute;
  bottom: 45px; /* Adjust this as needed */
  left: 5px; /* Adjust this as needed */
}
</style>



