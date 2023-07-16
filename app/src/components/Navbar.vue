<script setup lang="ts">
import DiscordBtn from './DiscordBtn.vue'

let theme = 'dark'
let label = 'Toggle Light Mode'

function toggleTheme() {  
  const element = document.body
  const label = document.getElementById('flexSwitchLabel')

  element.dataset.bsTheme = element.dataset.bsTheme === 'light' ? 'dark' : 'light'

  if (label !== null) {
    label.innerHTML = element.dataset.bsTheme === 'light' ? "Toggle Dark Mode" : "Toggle Light Mode"
  }
}
</script>

<template>
  <nav class="navbar navbar-dark navbar-expand-lg bg-dark">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">SwadeBot App</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/about">About</router-link>
          </li>
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
              Characters
            </a>
            <ul class="dropdown-menu">
              <router-link class="dropdown-item" to="/characters">View Characters</router-link>
              <router-link class="dropdown-item" to="/characters/create">Create Character</router-link>
            </ul>
          </li>
        </ul>
        <div class="d-flex flex-row align-items-center">
          <div class="form-check form-switch form-check-reverse me-2">
            <input class="form-check-input p-2 bg-dark" type="checkbox" id="flexSwitchCheckChecked" :checked="theme === 'dark'" @click="toggleTheme()">
            <label class="form-check-label text-light" for="flexSwitchCheckChecked" id="flexSwitchLabel">{{ label }}</label>
          </div>
          <discord-btn />
        </div>
      </div>
    </div>
  </nav>
</template>