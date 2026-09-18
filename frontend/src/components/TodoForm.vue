<script setup>
import { ref } from "vue";

const emit = defineEmits(["create"]);

const title = ref("");
const description = ref("");
const priority = ref("medium");
const dueDate = ref("");
const showNotes = ref(false);
const isSubmitting = ref(false);
const titleInputRef = ref(null);

function focusInput() {
  titleInputRef.value?.focus();
}

defineExpose({ focusInput });

async function handleSubmit() {
  const trimmedTitle = title.value.trim();
  if (!trimmedTitle || isSubmitting.value) return;

  isSubmitting.value = true;
  try {
    await emit("create", {
      title: trimmedTitle,
      description: description.value.trim(),
      priority: priority.value,
      due_date: dueDate.value || null,
    });
    title.value = "";
    description.value = "";
    priority.value = "medium";
    dueDate.value = "";
    showNotes.value = false;
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <form class="composer-card" @submit.prevent="handleSubmit">
    <div class="composer-main">
      <input
        ref="titleInputRef"
        v-model="title"
        type="text"
        class="composer-title-input"
        placeholder="Add a new task..."
        maxlength="200"
        required
      />
      <button
        type="button"
        class="btn btn-ghost"
        @click="showNotes = !showNotes"
      >
        {{ showNotes ? "Hide notes" : "+ Notes" }}
      </button>
    </div>

    <div v-if="showNotes" style="margin-top: 0.65rem">
      <textarea
        v-model="description"
        rows="2"
        class="textarea"
        placeholder="Optional notes or details..."
        maxlength="2000"
      />
    </div>

    <div class="composer-meta">
      <div class="composer-controls">
        <select v-model="priority" class="compact-select" aria-label="Task priority">
          <option value="low">Low priority</option>
          <option value="medium">Medium priority</option>
          <option value="high">High priority</option>
        </select>

        <input
          v-model="dueDate"
          type="date"
          class="compact-date"
          aria-label="Due date"
        />
      </div>

      <button
        type="submit"
        class="btn btn-primary"
        :disabled="!title.trim() || isSubmitting"
      >
        {{ isSubmitting ? "Adding..." : "Add task" }}
      </button>
    </div>
  </form>
</template>
