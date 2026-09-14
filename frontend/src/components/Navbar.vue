<script setup>
import { useRouter } from "vue-router";
import { authStore } from "@/store/auth";

const router = useRouter();

async function handleLogout() {
  await authStore.logout();
  router.push({ name: "login" });
}
</script>

<template>
  <header class="navbar">
    <div class="navbar-inner">
      <router-link :to="{ name: 'todos' }" class="brand">
        <span class="brand-mark">✓</span>
        <span>ToDo</span>
      </router-link>

      <div v-if="authStore.isAuthenticated.value" class="navbar-user">
        <span v-if="authStore.state.user" class="user-pill">
          {{ authStore.state.user.name }}
        </span>
        <button type="button" class="btn btn-secondary" @click="handleLogout">
          Sign out
        </button>
      </div>
    </div>
  </header>
</template>
