<script setup>
import { ref } from "vue";

defineProps({
  status: {
    type: String,
    required: true,
  },
  priority: {
    type: String,
    required: true,
  },
  search: {
    type: String,
    required: true,
  },
  counts: {
    type: Object,
    default: () => ({ total: 0, active: 0, completed: 0, overdue: 0 }),
  },
});

const emit = defineEmits([
  "update:status",
  "update:priority",
  "update:search",
  "clear-completed",
]);

const searchInputRef = ref(null);

function focusSearch() {
  searchInputRef.value?.focus();
}

defineExpose({ focusSearch });
</script>

<template>
  <div class="filter-bar">
    <div class="status-tabs" role="tablist" aria-label="Filter tasks by status">
      <button
        type="button"
        class="status-tab"
        :class="{ active: status === 'all' }"
        @click="emit('update:status', 'all')"
      >
        All
        <span class="tab-count">{{ counts.total }}</span>
      </button>

      <button
        type="button"
        class="status-tab"
        :class="{ active: status === 'active' }"
        @click="emit('update:status', 'active')"
      >
        Active
        <span class="tab-count">{{ counts.active }}</span>
      </button>

      <button
        type="button"
        class="status-tab"
        :class="{ active: status === 'completed' }"
        @click="emit('update:status', 'completed')"
      >
        Done
        <span class="tab-count">{{ counts.completed }}</span>
      </button>
    </div>

    <div class="filter-controls">
      <select
        :value="priority"
        class="compact-select"
        aria-label="Filter by priority"
        @change="emit('update:priority', $event.target.value)"
      >
        <option value="all">All priorities</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>

      <input
        ref="searchInputRef"
        :value="search"
        type="search"
        class="input search-input"
        placeholder="Search tasks..."
        aria-label="Search tasks"
        @input="emit('update:search', $event.target.value)"
      />

      <button
        v-if="counts.completed > 0"
        type="button"
        class="btn btn-danger-ghost"
        @click="emit('clear-completed')"
      >
        Clear done
      </button>
    </div>
  </div>
</template>
