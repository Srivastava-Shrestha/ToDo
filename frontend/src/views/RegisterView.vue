<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { authStore } from "@/store/auth";

const router = useRouter();
const name = ref("");
const email = ref("");
const password = ref("");
const errorMessage = ref("");
const isSubmitting = ref(false);

async function onSubmit() {
  errorMessage.value = "";
  if (!name.value.trim()) {
    errorMessage.value = "Name is required.";
    return;
  }
  if (!email.value.trim()) {
    errorMessage.value = "Email is required.";
    return;
  }
  if (password.value.length < 6) {
    errorMessage.value = "Password must be at least 6 characters long.";
    return;
  }

  isSubmitting.value = true;
  try {
    await authStore.register(
      name.value.trim(),
      email.value.trim(),
      password.value
    );
    router.push({ name: "todos" });
  } catch (err) {
    errorMessage.value =
      err.response?.data?.error || "Registration failed. Please try again.";
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <div class="auth-wrapper">
    <div class="auth-card">
      <h1 class="auth-title">Create an account</h1>
      <p class="auth-subtitle">Start organizing your tasks with zero clutter.</p>

      <div v-if="errorMessage" class="alert-error" role="alert">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="onSubmit" novalidate>
        <div class="form-group">
          <label class="form-label" for="register-name">Full name</label>
          <input
            id="register-name"
            v-model="name"
            type="text"
            class="input"
            placeholder="Shrestha Srivastava"
            autocomplete="name"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label" for="register-email">Email</label>
          <input
            id="register-email"
            v-model="email"
            type="email"
            class="input"
            placeholder="you@example.com"
            autocomplete="email"
            required
          />
        </div>

        <div class="form-group">
          <label class="form-label" for="register-password">Password</label>
          <input
            id="register-password"
            v-model="password"
            type="password"
            class="input"
            placeholder="At least 6 characters"
            autocomplete="new-password"
            required
          />
        </div>

        <button
          type="submit"
          class="btn btn-primary"
          style="width: 100%; margin-top: 0.4rem"
          :disabled="isSubmitting"
        >
          {{ isSubmitting ? "Creating account..." : "Create account" }}
        </button>
      </form>

      <p class="auth-footer">
        Already have an account?
        <router-link :to="{ name: 'login' }">Sign in</router-link>
      </p>
    </div>
  </div>
</template>
