<script setup>
import Navbar from "@/components/Navbar.vue";
</script>

<template>
  <div class="app-shell">
    <Navbar />
    <main class="main-container">
      <router-view />
    </main>
  </div>
</template>
