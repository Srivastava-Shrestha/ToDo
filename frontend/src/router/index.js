import { createRouter, createWebHistory } from "vue-router";
import { authStore } from "@/store/auth";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import TodoView from "@/views/TodoView.vue";

const routes = [
  {
    path: "/",
    name: "todos",
    component: TodoView,
    meta: { requiresAuth: true },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { guestOnly: true },
  },
  {
    path: "/register",
    name: "register",
    component: RegisterView,
    meta: { guestOnly: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const isAuthed = authStore.isAuthenticated.value;
  if (to.meta.requiresAuth && !isAuthed) {
    return { name: "login" };
  }
  if (to.meta.guestOnly && isAuthed) {
    return { name: "todos" };
  }
  return true;
});

export default router;
