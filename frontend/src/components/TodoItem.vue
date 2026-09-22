<script setup>
import { ref } from "vue";

const props = defineProps({
  todo: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["toggle", "update", "delete"]);

const isEditing = ref(false);
const editTitle = ref("");
const editDescription = ref("");
const editPriority = ref("medium");
const editDueDate = ref("");
const isSaving = ref(false);

function startEdit() {
  editTitle.value = props.todo.title;
  editDescription.value = props.todo.description || "";
  editPriority.value = props.todo.priority || "medium";
  editDueDate.value = props.todo.due_date || "";
  isEditing.value = true;
}

function cancelEdit() {
  isEditing.value = false;
}

async function saveEdit() {
  const trimmed = editTitle.value.trim();
  if (!trimmed || isSaving.value) return;

  isSaving.value = true;
  try {
    await emit("update", props.todo.id, {
      title: trimmed,
      description: editDescription.value.trim(),
      priority: editPriority.value,
      due_date: editDueDate.value || null,
    });
    isEditing.value = false;
  } finally {
    isSaving.value = false;
  }
}

function formatDueDate(isoDate) {
  if (!isoDate) return "";
  const [year, month, day] = isoDate.split("-").map(Number);
  const dt = new Date(year, month - 1, day);
  return dt.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}
</script>

<template>
  <article class="todo-item" :class="{ 'is-completed': todo.is_completed }">
    <div v-if="!isEditing" class="todo-row">
      <button
        type="button"
        class="checkbox-btn"
        :class="{ checked: todo.is_completed }"
        :aria-label="
          todo.is_completed ? 'Mark task incomplete' : 'Mark task complete'
        "
        @click="emit('toggle', todo.id)"
      >
        <span v-if="todo.is_completed" style="font-size: 0.7rem">✓</span>
      </button>

      <div class="todo-body">
        <div class="todo-title">{{ todo.title }}</div>
        <p v-if="todo.description" class="todo-description">
          {{ todo.description }}
        </p>

        <div class="todo-badges">
          <span class="badge" :class="`badge-priority-${todo.priority}`">
            {{ todo.priority.charAt(0).toUpperCase() + todo.priority.slice(1) }}
          </span>

          <span
            v-if="todo.due_date"
            class="badge"
            :class="todo.is_overdue ? 'badge-overdue' : 'badge-due'"
          >
            {{ todo.is_overdue ? "Overdue · " : "Due "
            }}{{ formatDueDate(todo.due_date) }}
          </span>
        </div>
      </div>

      <div class="todo-actions">
        <button type="button" class="btn btn-ghost" @click="startEdit">
          Edit
        </button>
        <button
          type="button"
          class="btn btn-danger-ghost"
          @click="emit('delete', todo.id)"
        >
          Delete
        </button>
      </div>
    </div>

    <form v-else @submit.prevent="saveEdit" @keydown.esc="cancelEdit">
      <div class="form-group" style="margin-bottom: 0.6rem">
        <input
          v-model="editTitle"
          type="text"
          class="input"
          placeholder="Task title"
          maxlength="200"
          required
        />
      </div>

      <div class="form-group" style="margin-bottom: 0.6rem">
        <textarea
          v-model="editDescription"
          rows="2"
          class="textarea"
          placeholder="Notes (optional)"
          maxlength="2000"
        />
      </div>

      <div class="composer-meta" style="margin-top: 0.5rem; padding-top: 0.5rem">
        <div class="composer-controls">
          <select v-model="editPriority" class="compact-select">
            <option value="low">Low priority</option>
            <option value="medium">Medium priority</option>
            <option value="high">High priority</option>
          </select>

          <input v-model="editDueDate" type="date" class="compact-date" />
        </div>

        <div style="display: flex; gap: 0.45rem">
          <button type="button" class="btn btn-secondary" @click="cancelEdit">
            Cancel
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="!editTitle.trim() || isSaving"
          >
            {{ isSaving ? "Saving..." : "Save" }}
          </button>
        </div>
      </div>
    </form>
  </article>
</template>
