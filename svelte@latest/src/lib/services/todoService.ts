// src/lib/services/todoService.ts

/**
 * @file todoService.ts
 * @description Service layer for managing To-Do items via API interactions.
 */

import { api, type ApiError } from './api';

// --- Interfaces based on API documentation (prompts/frontend/phase1.txt) ---

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
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601
  completed_at?: string | null; // ISO 8601
}

// Payload for creating a new To-Do item (all fields optional except title as per API)
// However, the API spec says title is required.
// Status and priority have defaults on the backend if not provided.
export interface CreateTodoPayload {
  title: string;
  description?: string;
  due_date?: string; // YYYY-MM-DD
  status?: TodoStatus;
  priority?: TodoPriority;
}

// Payload for updating an existing To-Do item (all fields optional)
export interface UpdateTodoPayload {
  title?: string;
  description?: string | null;
  due_date?: string | null; // YYYY-MM-DD
  status?: TodoStatus;
  priority?: TodoPriority;
}

// --- Service Methods ---

/**
 * Fetches all To-Do items for the authenticated user.
 * API: GET /todo/todos
 * @returns {Promise<TodoItem[]>} A list of to-do items.
 * @throws {ApiError} If the request fails.
 */
async function getAllTodos(): Promise<TodoItem[]> {
  try {
    // This endpoint requires authentication, api.get handles it by default.
    const todos = await api.get<TodoItem[]>('/todo/todos');
    return todos || []; // Return empty array if response is null/undefined
  } catch (error) {
    console.error('TodoService: Failed to fetch all todos', error);
    throw error; // Re-throw for the caller to handle
  }
}

/**
 * Creates a new To-Do item.
 * API: POST /todo/todos
 * @param payload - The data for the new to-do item.
 * @returns {Promise<TodoItem>} The newly created to-do item.
 * @throws {ApiError} If the request fails.
 */
async function createTodo(payload: CreateTodoPayload): Promise<TodoItem> {
  try {
    const newTodo = await api.post<TodoItem>('/todo/todos', payload);
    return newTodo;
  } catch (error) {
    console.error('TodoService: Failed to create todo', error);
    throw error;
  }
}

/**
 * Fetches a specific To-Do item by its ID.
 * API: GET /todo/todos/<int:todo_id>
 * @param todoId - The ID of the to-do item to fetch.
 * @returns {Promise<TodoItem | null>} The to-do item, or null if not found.
 * @throws {ApiError} If the request fails (other than 404).
 */
async function getTodoById(todoId: number): Promise<TodoItem | null> {
  try {
    const todoItem = await api.get<TodoItem>(`/todo/todos/${todoId}`);
    return todoItem;
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
 * @param todoId - The ID of the to-do item to update.
 * @param payload - The data to update. Only provided fields will be changed.
 * @returns {Promise<TodoItem>} The updated to-do item.
 * @throws {ApiError} If the request fails.
 */
async function updateTodo(todoId: number, payload: UpdateTodoPayload): Promise<TodoItem> {
  try {
    const updatedTodo = await api.put<TodoItem>(`/todo/todos/${todoId}`, payload);
    return updatedTodo;
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
    // API returns 204 No Content on success, api.delete handles this by returning null or void
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
