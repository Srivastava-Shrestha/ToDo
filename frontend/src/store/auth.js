import { computed, reactive } from "vue";
import api, { TOKEN_STORAGE_KEY, USER_STORAGE_KEY } from "@/services/api";

function loadStoredUser() {
  try {
    const raw = localStorage.getItem(USER_STORAGE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

const state = reactive({
  token: localStorage.getItem(TOKEN_STORAGE_KEY) || null,
  user: loadStoredUser(),
});

function setSession(token, user) {
  state.token = token;
  state.user = user;
  localStorage.setItem(TOKEN_STORAGE_KEY, token);
  localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(user));
}

function clearSession() {
  state.token = null;
  state.user = null;
  localStorage.removeItem(TOKEN_STORAGE_KEY);
  localStorage.removeItem(USER_STORAGE_KEY);
}

export const authStore = {
  state,
  isAuthenticated: computed(() => Boolean(state.token)),

  async register(name, email, password) {
    const { data } = await api.post("/auth/register", {
      name,
      email,
      password,
    });
    setSession(data.token, data.user);
    return data.user;
  },

  async login(email, password) {
    const { data } = await api.post("/auth/login", {
      email,
      password,
    });
    setSession(data.token, data.user);
    return data.user;
  },

  async logout() {
    try {
      if (state.token) {
        await api.post("/auth/logout");
      }
    } catch {
      // Ignore network or expired token errors during sign-out
    } finally {
      clearSession();
    }
  },

  async fetchCurrentUser() {
    if (!state.token) return null;
    try {
      const { data } = await api.get("/auth/me");
      state.user = data.user;
      localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(data.user));
      return data.user;
    } catch {
      clearSession();
      return null;
    }
  },
};
