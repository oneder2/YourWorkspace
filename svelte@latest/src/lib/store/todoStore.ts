// src/lib/store/todoStore.ts

/**
 * @file todoStore.ts
 * @description Manages the state for To-Do items, including fetching from and updating to the backend.
 * Reflects V3 architecture where 'is_current_focus' is a property of a To-Do item.
 */

import { writable, derived, type Writable, type Readable, get } from 'svelte/store';
import {
  todoService,
  type TodoItem,
  type CreateTodoPayload,
  type UpdateTodoPayload
} from '$lib/services/todoService';
import type { ApiError } from '$lib/services/api';

// Main state interface for the writable part of the store
export interface TodoStoreState {
  todos: TodoItem[];
  isLoading: boolean;
  error: string | null;
  maxFocusItems: number;
}

// Interface for the main store object's methods (excluding derived stores)
export interface MainTodoStore extends Writable<TodoStoreState> {
  loadAllTodos: () => Promise<void>;
  addTodo: (payload: CreateTodoPayload) => Promise<TodoItem | null>;
  editTodo: (todoId: number, payload: UpdateTodoPayload) => Promise<TodoItem | null>;
  removeTodo: (todoId: number) => Promise<void>;
  toggleCompleteStatus: (todoId: number, currentStatus: TodoItem['status']) => Promise<TodoItem | null>;
  toggleCurrentFocus: (todoId: number) => Promise<TodoItem | null>;
}

const initialState: TodoStoreState = {
  todos: [],
  isLoading: false,
  error: null,
  maxFocusItems: 3,
};

// This is the core writable store holding the primary state
const mainTodoWritable: Writable<TodoStoreState> = writable<TodoStoreState>(initialState);

// --- Store Methods ---
async function loadAllTodos(): Promise<void> {
  mainTodoWritable.update(state => ({ ...state, isLoading: true, error: null }));
  try {
    const fetchedTodos = await todoService.getAllTodos();

    // Sort todos once before updating the store to avoid multiple re-renders
    const sortedTodos = fetchedTodos.sort((a, b) => {
      // First sort by current focus status
      if (a.is_current_focus && !b.is_current_focus) return -1;
      if (!a.is_current_focus && b.is_current_focus) return 1;

      // Then by completion status
      if (a.status !== 'completed' && b.status === 'completed') return -1;
      if (a.status === 'completed' && b.status !== 'completed') return 1;

      // Then by creation date (newest first)
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    });

    mainTodoWritable.set({
      ...get(mainTodoWritable),
      todos: sortedTodos,
      isLoading: false,
      error: null
    });
  } catch (err) {
    const error = err as ApiError;
    console.error('TodoStore: Error fetching todos', error);
    mainTodoWritable.set({
      ...get(mainTodoWritable),
      todos: [],
      isLoading: false,
      error: error.message || 'Failed to fetch todos'
    });
  }
}

async function addTodo(payload: CreateTodoPayload): Promise<TodoItem | null> {
  mainTodoWritable.update(state => ({ ...state, isLoading: true, error: null }));
  try {
    const newTodo = await todoService.createTodo(payload);
    mainTodoWritable.update(state => ({
      ...state,
      todos: [newTodo, ...state.todos].sort((a,b) => {
          if (a.is_current_focus && !b.is_current_focus) return -1;
          if (!a.is_current_focus && b.is_current_focus) return 1;
          return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
      }),
      isLoading: false,
    }));
    return newTodo;
  } catch (err) {
    const error = err as ApiError;
    console.error('TodoStore: Error adding todo', error);
    mainTodoWritable.update(state => ({ ...state, isLoading: false, error: error.message || 'Failed to add todo' }));
    return null;
  }
}

async function editTodo(todoId: number, payload: UpdateTodoPayload): Promise<TodoItem | null> {
  mainTodoWritable.update(state => ({ ...state, isLoading: true, error: null }));
  try {
    const updatedTodo = await todoService.updateTodo(todoId, payload);
    mainTodoWritable.update(state => ({
      ...state,
      todos: state.todos.map(todo => (todo && todo.id === todoId ? updatedTodo : todo)),
      isLoading: false,
    }));
    return updatedTodo;
  } catch (err) {
    const error = err as ApiError;
    console.error('TodoStore: Error editing todo', error);
    mainTodoWritable.update(state => ({ ...state, isLoading: false, error: error.message || `Failed to update todo ${todoId}` }));
    return null;
  }
}

async function toggleCurrentFocus(todoId: number): Promise<TodoItem | null> {
  const currentState = get(mainTodoWritable);

  // Simple null check
  if (!currentState || !currentState.todos) {
    console.error('TodoStore: Invalid state or todos array not found');
    return null;
  }

  const targetTodo = currentState.todos.find(t => t && t.id === todoId);

  if (!targetTodo) {
    console.error(`TodoStore: Todo item with ID ${todoId} not found for toggling focus.`);
    mainTodoWritable.update(state => ({ ...state, isLoading: false, error: `Todo item ${todoId} not found.` }));
    return null;
  }

  const currentlyFocusedItems = currentState.todos.filter(t => t && t.is_current_focus && t.id !== todoId && t.status !== 'completed');
  const newFocusState = !targetTodo.is_current_focus;

  if (newFocusState && currentlyFocusedItems.length >= currentState.maxFocusItems) {
    const message = `Cannot set more than ${currentState.maxFocusItems} items as current focus. Please remove another item from focus first.`;
    console.warn(message);
    mainTodoWritable.update(state => ({ ...state, isLoading: false, error: message }));
    return null;
  }

  mainTodoWritable.update(state => ({ ...state, isLoading: true, error: null }));
  try {
    const updatedTodo = await todoService.updateTodo(todoId, { is_current_focus: newFocusState });
    mainTodoWritable.update(state => ({
      ...state,
      todos: state.todos.map(todo => (todo && todo.id === todoId ? updatedTodo : todo)),
      isLoading: false,
      error: null,
    }));
    return updatedTodo;
  } catch (err) {
    const error = err as ApiError;
    console.error('TodoStore: Error toggling current focus', error);
    mainTodoWritable.update(state => ({ ...state, isLoading: false, error: error.message || `Failed to toggle focus for item ${todoId}.` }));
    return null;
  }
}

async function removeTodo(todoId: number): Promise<void> {
  mainTodoWritable.update(state => ({ ...state, isLoading: true, error: null }));
  try {
    await todoService.deleteTodo(todoId);
    mainTodoWritable.update(state => ({
      ...state,
      todos: state.todos.filter(todo => todo && todo.id !== todoId),
      isLoading: false,
    }));
  } catch (err) {
    const error = err as ApiError;
    console.error('TodoStore: Error removing todo', error);
    mainTodoWritable.update(state => ({ ...state, isLoading: false, error: error.message || `Failed to delete todo ${todoId}` }));
  }
}

async function toggleCompleteStatus(todoId: number, currentItemStatus: TodoItem['status']): Promise<TodoItem | null> {
  const newStatus: TodoItem['status'] = currentItemStatus === 'completed' ? 'pending' : 'completed';
  const payload: UpdateTodoPayload = { status: newStatus };

  const currentState = get(mainTodoWritable);
  if (currentState && currentState.todos) {
    const currentItem = currentState.todos.find(t => t && t.id === todoId);
    if (newStatus === 'completed' && currentItem?.is_current_focus) {
        payload.is_current_focus = false;
    }
  }
  return editTodo(todoId, payload);
}

// --- Derived Stores (Exported Separately) ---
export const currentFocusTodos: Readable<TodoItem[]> = derived(
  mainTodoWritable,
  $mainTodoState => {
    if (!$mainTodoState || !$mainTodoState.todos) {
      return [];
    }
    return $mainTodoState.todos
      .filter(todo => todo && todo.is_current_focus && todo.status !== 'completed')
      .sort((a, b) => new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime());
  }
);

export const otherActiveTodos: Readable<TodoItem[]> = derived(
  mainTodoWritable,
  $mainTodoState => {
    if (!$mainTodoState || !$mainTodoState.todos) {
      return [];
    }
    return $mainTodoState.todos
      .filter(todo => todo && !todo.is_current_focus && todo.status !== 'completed')
      .sort((a: TodoItem, b: TodoItem) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
  }
);

export const completedTodos: Readable<TodoItem[]> = derived(
  mainTodoWritable,
  $mainTodoState => {
    if (!$mainTodoState || !$mainTodoState.todos) {
      return [];
    }
    return $mainTodoState.todos
      .filter(todo => todo && todo.status === 'completed')
      .sort((a: TodoItem, b: TodoItem) => {
          const dateA = a.completed_at ? new Date(a.completed_at).getTime() : 0;
          const dateB = b.completed_at ? new Date(b.completed_at).getTime() : 0;
          return dateB - dateA;
      });
  }
);

// Export the main store object containing methods and the core writable store's capabilities
export const todoStore: MainTodoStore = {
  subscribe: mainTodoWritable.subscribe,
  set: mainTodoWritable.set,
  update: mainTodoWritable.update,
  loadAllTodos,
  addTodo,
  editTodo,
  removeTodo,
  toggleCompleteStatus,
  toggleCurrentFocus,
};
