<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import { useRouter } from "vue-router";
import api from "@/services/api";
import { authStore } from "@/store/auth";
import TodoForm from "@/components/TodoForm.vue";
import TodoFilterBar from "@/components/TodoFilterBar.vue";
import TodoItem from "@/components/TodoItem.vue";

const router = useRouter();
const todos = ref([]);
const counts = ref({ total: 0, active: 0, completed: 0, overdue: 0 });
const statusFilter = ref("all");
const priorityFilter = ref("all");
const searchQuery = ref("");
const isLoading = ref(false);
const errorMessage = ref("");
const todoFormRef = ref(null);
const filterBarRef = ref(null);

const hasActiveFilters = computed(
  () =>
    statusFilter.value !== "all" ||
    priorityFilter.value !== "all" ||
    Boolean(searchQuery.value.trim())
);

function resetFilters() {
  statusFilter.value = "all";
  priorityFilter.value = "all";
  searchQuery.value = "";
}

function handleGlobalKeydown(event) {
  const tag = event.target?.tagName?.toLowerCase();
  if (tag === "input" || tag === "textarea" || tag === "select") {
    return;
  }
  if (event.key === "n" && !event.metaKey && !event.ctrlKey) {
    event.preventDefault();
    todoFormRef.value?.focusInput();
  } else if (event.key === "/" && !event.metaKey && !event.ctrlKey) {
    event.preventDefault();
    filterBarRef.value?.focusSearch();
  }
}

async function fetchTodos() {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    const params = {
      status: statusFilter.value,
    };
    if (priorityFilter.value !== "all") {
      params.priority = priorityFilter.value;
    }
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim();
    }

    const { data } = await api.get("/todos", { params });
    todos.value = data.todos;
    if (data.counts) {
      counts.value = data.counts;
    }
  } catch (err) {
    if (err.response?.status === 401) {
      await authStore.logout();
      router.push({ name: "login" });
      return;
    }
    errorMessage.value =
      err.response?.data?.error || "Failed to load tasks. Please try again.";
  } finally {
    isLoading.value = false;
  }
}

async function handleCreateTodo(payload) {
  errorMessage.value = "";
  try {
    await api.post("/todos", payload);
    await fetchTodos();
  } catch (err) {
    errorMessage.value =
      err.response?.data?.error || "Could not create task.";
  }
}

async function handleToggleTodo(todoId) {
  errorMessage.value = "";
  try {
    await api.patch(`/todos/${todoId}/toggle`);
    await fetchTodos();
  } catch (err) {
    errorMessage.value =
      err.response?.data?.error || "Could not update task status.";
  }
}

async function handleUpdateTodo(todoId, payload) {
  errorMessage.value = "";
  try {
    await api.put(`/todos/${todoId}`, payload);
    await fetchTodos();
  } catch (err) {
    errorMessage.value =
      err.response?.data?.error || "Could not save changes to task.";
  }
}

async function handleDeleteTodo(todoId) {
  errorMessage.value = "";
  try {
    await api.delete(`/todos/${todoId}`);
    await fetchTodos();
  } catch (err) {
    errorMessage.value =
      err.response?.data?.error || "Could not delete task.";
  }
}

async function handleClearCompleted() {
  errorMessage.value = "";
  try {
    await api.delete("/todos/completed");
    await fetchTodos();
  } catch (err) {
    errorMessage.value =
      err.response?.data?.error || "Could not clear completed tasks.";
  }
}

watch([statusFilter, priorityFilter, searchQuery], () => {
  fetchTodos();
});

onMounted(async () => {
  window.addEventListener("keydown", handleGlobalKeydown);
  if (!authStore.state.user) {
    await authStore.fetchCurrentUser();
  }
  await fetchTodos();
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleGlobalKeydown);
});
</script>

<template>
  <section>
    <div class="dashboard-header">
      <div>
        <h1 style="font-size: 1.4rem; font-weight: 600; letter-spacing: -0.02em">
          Tasks
        </h1>
        <p style="font-size: 0.85rem; color: var(--text-secondary)">
          {{ counts.active }} remaining · {{ counts.completed }} completed
          <span
            v-if="counts.overdue > 0"
            style="color: var(--danger); font-weight: 500"
          >
            · {{ counts.overdue }} overdue
          </span>
        </p>
      </div>
      <div class="shortcut-hints" aria-hidden="true">
        <span><kbd>N</kbd> New</span>
        <span><kbd>/</kbd> Search</span>
      </div>
    </div>

    <div v-if="errorMessage" class="alert-error" role="alert">
      {{ errorMessage }}
    </div>

    <TodoForm ref="todoFormRef" @create="handleCreateTodo" />

    <TodoFilterBar
      ref="filterBarRef"
      v-model:status="statusFilter"
      v-model:priority="priorityFilter"
      v-model:search="searchQuery"
      :counts="counts"
      @clear-completed="handleClearCompleted"
    />

    <div v-if="isLoading && todos.length === 0" class="empty-state">
      <p class="empty-state-subtitle">Loading tasks...</p>
    </div>

    <div v-else-if="todos.length === 0" class="empty-state">
      <p class="empty-state-title">
        {{
          hasActiveFilters
            ? "No matching tasks found"
            : "Your task list is clear"
        }}
      </p>
      <p class="empty-state-subtitle">
        {{
          hasActiveFilters
            ? "Try adjusting your status, priority, or search filters."
            : "Add a task above or press N to start planning your day."
        }}
      </p>
      <button
        v-if="hasActiveFilters"
        type="button"
        class="btn btn-secondary"
        style="margin-top: 0.85rem"
        @click="resetFilters"
      >
        Reset filters
      </button>
    </div>

    <div v-else class="todo-list">
      <TodoItem
        v-for="todo in todos"
        :key="todo.id"
        :todo="todo"
        @toggle="handleToggleTodo"
        @update="handleUpdateTodo"
        @delete="handleDeleteTodo"
      />
    </div>
  </section>
</template>
