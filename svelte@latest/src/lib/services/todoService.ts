// src/lib/services/todoService.ts

/**
 * @file todoService.ts
 * @description Service layer for managing To-Do items via API interactions.
 * Reflects V3 architecture where 'is_current_focus' is a property of a To-Do item.
 */

import { api, type ApiError } from './api';

// --- Interfaces based on V3 API documentation ---

export type TodoStatus = 'pending' | 'in_progress' | 'completed' | 'deferred';
export type TodoPriority = 'low' | 'medium' | 'high';

export interface TodoItem {
  id: number;
  user_id: number;
  title: string;
  description?: string | null;
  due_date?: string | null; // YYYY-MM-DD
  status: TodoStatus;
  priority: TodoPriority;
  is_current_focus: boolean; // NEW: Indicates if item is a current focus
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
  completed_at?: string | null; // ISO 8601
}

// Payload for creating a new To-Do item
// 'is_current_focus' is typically not sent on creation; managed via PUT/update.
export interface CreateTodoPayload {
  title: string;
  description?: string;
  due_date?: string; // YYYY-MM-DD
  status?: TodoStatus;
  priority?: TodoPriority;
  // is_current_focus?: boolean; // Usually defaults to false on backend
}

// Payload for updating an existing To-Do item
export interface UpdateTodoPayload {
  title?: string;
  description?: string | null;
  due_date?: string | null; // YYYY-MM-DD
  status?: TodoStatus;
  priority?: TodoPriority;
  is_current_focus?: boolean; // NEW: To mark/unmark as current focus
}

// --- Service Methods ---

/**
 * Fetches all To-Do items for the authenticated user.
 * API: GET /todo/todos
 * Expected to include 'is_current_focus' field for each item.
 * @returns {Promise<TodoItem[]>} A list of to-do items.
 * @throws {ApiError} If the request fails.
 */
async function getAllTodos(): Promise<TodoItem[]> {
  try {
    const response = await api.get<{data: TodoItem[]}>('/todo/todos');
    return response.data || [];
  } catch (error) {
    console.error('TodoService: Failed to fetch all todos', error);
    throw error;
  }
}

/**
 * Creates a new To-Do item.
 * API: POST /todo/todos
 * 'is_current_focus' will typically default to false on the backend.
 * @param payload - The data for the new to-do item.
 * @returns {Promise<TodoItem>} The newly created to-do item.
 * @throws {ApiError} If the request fails.
 */
async function createTodo(payload: CreateTodoPayload): Promise<TodoItem> {
  try {
    const response = await api.post<{data: TodoItem}>('/todo/todos', payload);
    return response.data;
  } catch (error) {
    console.error('TodoService: Failed to create todo', error);
    throw error;
  }
}

/**
 * Fetches a specific To-Do item by its ID.
 * API: GET /todo/todos/<int:todo_id>
 * Expected to include 'is_current_focus' field.
 * @param todoId - The ID of the to-do item to fetch.
 * @returns {Promise<TodoItem | null>} The to-do item, or null if not found.
 * @throws {ApiError} If the request fails (other than 404).
 */
async function getTodoById(todoId: number): Promise<TodoItem | null> {
  try {
    const response = await api.get<{data: TodoItem}>(`/todo/todos/${todoId}`);
    return response.data;
  } catch (error: any) {
    if (error.status === 404) {
      console.warn(`TodoService: Todo item with ID ${todoId} not found.`);
      return null;
    }
    console.error(`TodoService: Failed to fetch todo with ID ${todoId}`, error);
    throw error;
  }
}

/**
 * Updates an existing To-Do item.
 * API: PUT /todo/todos/<int:todo_id>
 * This method is now also used to toggle the 'is_current_focus' status.
 * @param todoId - The ID of the to-do item to update.
 * @param payload - The data to update. Only provided fields will be changed.
 * @returns {Promise<TodoItem>} The updated to-do item.
 * @throws {ApiError} If the request fails.
 */
async function updateTodo(todoId: number, payload: UpdateTodoPayload): Promise<TodoItem> {
  try {
    const response = await api.put<{data: TodoItem}>(`/todo/todos/${todoId}`, payload);
    return response.data;
  } catch (error) {
    console.error(`TodoService: Failed to update todo with ID ${todoId}`, error);
    throw error;
  }
}

/**
 * Deletes a specific To-Do item.
 * API: DELETE /todo/todos/<int:todo_id>
 * @param todoId - The ID of the to-do item to delete.
 * @returns {Promise<void>}
 * @throws {ApiError} If the request fails.
 */
async function deleteTodo(todoId: number): Promise<void> {
  try {
    await api.delete(`/todo/todos/${todoId}`);
  } catch (error) {
    console.error(`TodoService: Failed to delete todo with ID ${todoId}`, error);
    throw error;
  }
}

export const todoService = {
  getAllTodos,
  createTodo,
  getTodoById,
  updateTodo,
  deleteTodo,
};
