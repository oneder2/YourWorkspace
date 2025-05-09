// src/lib/store/todoStore.ts

/**
 * @file todoStore.ts
 * @description Manages the state for To-Do items, including fetching from and updating to the backend.
 */

import { writable, type Writable } from 'svelte/store';
import { todoService, type TodoItem, type CreateTodoPayload, type UpdateTodoPayload } from '$lib/services/todoService';
import type { ApiError } from '$lib/services/api';

// Define the structure for the To-Do store's state
export interface TodoStoreState {
  todos: TodoItem[];
  isLoading: boolean;
  error: string | null; // Can be an ApiError object or a string message
}

// Define the structure for the custom store, including its methods
// CustomTodoStore now correctly includes all Writable<TodoStoreState> properties
// because it extends it, and our exported object will provide them.
export interface CustomTodoStore extends Writable<TodoStoreState> {
  fetchAllTodos: () => Promise<void>;
  addTodo: (payload: CreateTodoPayload) => Promise<TodoItem | null>;
  editTodo: (todoId: number, payload: UpdateTodoPayload) => Promise<TodoItem | null>;
  removeTodo: (todoId: number) => Promise<void>;
  toggleTodoStatus: (todoId: number, currentStatus: TodoItem['status']) => Promise<TodoItem | null>;
}

// Initial state for the store
const initialState: TodoStoreState = {
  todos: [],
  isLoading: false,
  error: null,
};

// Create the writable store instance. This object has subscribe, set, and update.
const { subscribe, set, update }: Writable<TodoStoreState> = writable<TodoStoreState>(initialState);

// --- Store Methods (these are the custom functionalities) ---

async function fetchAllTodos(): Promise<void> {
  update(state => ({ ...state, isLoading: true, error: null }));
  try {
    const fetchedTodos = await todoService.getAllTodos();
    fetchedTodos.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
    set({ todos: fetchedTodos, isLoading: false, error: null }); // Use `set` from the writable store
  } catch (err) {
    const error = err as ApiError;
    console.error('TodoStore: Error fetching todos', error);
    // Use `set` here as well, to reset the state correctly on error
    set({ todos: [], isLoading: false, error: error.message || 'Failed to fetch todos' });
  }
}

async function addTodo(payload: CreateTodoPayload): Promise<TodoItem | null> {
  update(state => ({ ...state, isLoading: true, error: null }));
  try {
    const newTodo = await todoService.createTodo(payload);
    update(state => ({ // Use `update` from the writable store
      ...state,
      todos: [newTodo, ...state.todos],
      isLoading: false,
    }));
    return newTodo;
  } catch (err) {
    const error = err as ApiError;
    console.error('TodoStore: Error adding todo', error);
    update(state => ({ ...state, isLoading: false, error: error.message || 'Failed to add todo' }));
    return null;
  }
}

async function editTodo(todoId: number, payload: UpdateTodoPayload): Promise<TodoItem | null> {
  update(state => ({ ...state, isLoading: true, error: null }));
  try {
    const updatedTodo = await todoService.updateTodo(todoId, payload);
    update(state => ({ // Use `update`
      ...state,
      todos: state.todos.map(todo => (todo.id === todoId ? updatedTodo : todo)),
      isLoading: false,
    }));
    return updatedTodo;
  } catch (err) {
    const error = err as ApiError;
    console.error('TodoStore: Error editing todo', error);
    update(state => ({ ...state, isLoading: false, error: error.message || `Failed to update todo ${todoId}` }));
    return null;
  }
}

async function removeTodo(todoId: number): Promise<void> {
  update(state => ({ ...state, isLoading: true, error: null }));
  try {
    await todoService.deleteTodo(todoId);
    update(state => ({ // Use `update`
      ...state,
      todos: state.todos.filter(todo => todo.id !== todoId),
      isLoading: false,
    }));
  } catch (err) {
    const error = err as ApiError;
    console.error('TodoStore: Error removing todo', error);
    update(state => ({ ...state, isLoading: false, error: error.message || `Failed to delete todo ${todoId}` }));
  }
}

async function toggleTodoStatus(todoId: number, currentStatus: TodoItem['status']): Promise<TodoItem | null> {
  const nextStatus: TodoItem['status'] = currentStatus === 'completed' ? 'pending' : 'completed';
  // This internally calls editTodo, which uses `update`
  return editTodo(todoId, { status: nextStatus });
}


// Export the custom store object.
// It now includes subscribe, set, and update from the original writable store,
// fulfilling the Writable<TodoStoreState> contract part of CustomTodoStore.
export const todoStore: CustomTodoStore = {
  subscribe,
  set,      // Now explicitly included
  update,   // Now explicitly included
  fetchAllTodos,
  addTodo,
  editTodo,
  removeTodo,
  toggleTodoStatus,
};
