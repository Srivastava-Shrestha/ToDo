<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { authStore } from "@/store/auth";

const router = useRouter();
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const isSubmitting = ref(false);

async function onSubmit() {
  errorMessage.value = "";
  if (!email.value.trim() || !password.value) {
    errorMessage.value = "Please enter both your email and password.";
    return;
  }

  isSubmitting.value = true;
  try {
    await authStore.login(email.value.trim(), password.value);
    router.push({ name: "todos" });
  } catch (err) {
    errorMessage.value =
      err.response?.data?.error || "Unable to sign in. Please check your credentials.";
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h1 class="auth-title">Welcome back</h1>
      <p class="auth-subtitle">Sign in to access your workspace tasks.</p>

      <div v-if="errorMessage" class="alert-error" role="alert">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="onSubmit" novalidate>
        <div class="form-group">
          <label class="form-label" for="login-email">Email</label>
          <input
            id="login-email"
            v-model="email"
            type="email"
            class="input"
            placeholder="you@example.com"
            autocomplete="email"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label" for="login-password">Password</label>
          <input
            id="login-password"
            v-model="password"
            type="password"
            class="input"
            placeholder="••••••••"
            autocomplete="current-password"
            required
          />
        </div>

        <button
          type="submit"
          class="btn btn-primary"
          style="width: 100%; margin-top: 0.4rem"
          :disabled="isSubmitting"
        >
          {{ isSubmitting ? "Signing in..." : "Sign in" }}
        </button>
      </form>

      <p class="auth-footer">
        Don't have an account?
        <router-link :to="{ name: 'register' }">Create one</router-link>
      </p>
    </div>
  </div>
</template>
