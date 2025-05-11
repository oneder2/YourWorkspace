// File: backup/lib/store/todoStore.ts.txt
// Description: Manages the state for todo items, including fetching from and updating to the backend.
// Corrected import for payload types and service method names.

import { writable, get, derived } from 'svelte/store';
// Correctly import specific payload types and the TodoItem type
import type { TodoItem, CreateTodoPayload, UpdateTodoPayload } from '$lib/services/todoService'; 
import { todoService } from '$lib/services/todoService'; // Assuming todoService is an instance

export interface TodoStoreState {
  todos: TodoItem[];
  isLoading: boolean;
  error: string | null;
}

class MainTodoStore {
  private readonly _store = writable<TodoStoreState>({
    todos: [],
    isLoading: false,
    error: null,
  });

  // Expose store's subscribe method for Svelte components
  subscribe = this._store.subscribe;

  // --- Private Helper Methods ---
  private _updateTodoItemInStore(updatedItem: TodoItem) {
    this._store.update(state => {
      const index = state.todos.findIndex(t => t.id === updatedItem.id);
      if (index !== -1) {
        const newTodos = [...state.todos];
        newTodos[index] = updatedItem;
        return { ...state, todos: newTodos };
      }
      return state; 
    });
  }

  private _removeTodoItemFromStore(id: number) {
    this._store.update(state => ({
      ...state,
      todos: state.todos.filter(t => t.id !== id),
    }));
  }

  private _setLoading(isLoading: boolean) {
    this._store.update(state => ({ ...state, isLoading }));
  }

  private _setError(error: string | null) {
    this._store.update(state => ({ ...state, error }));
  }

  // --- Public Methods ---

  /**
   * Loads all todo items from the backend and updates the store.
   */
  async loadAllTodos(): Promise<void> {
    if (get(this._store).isLoading) return;
    this._setLoading(true);
    this._setError(null);
    try {
      // Corrected method name: getAllTodos instead of getTodos
      const fetchedTodos = await todoService.getAllTodos(); 
      this._store.update(state => ({
        ...state,
        todos: fetchedTodos || [], 
      }));
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Failed to load todos';
      console.error('Error loading todos:', message);
      this._setError(message);
    } finally {
      this._setLoading(false);
    }
  }

  /**
   * Adds a new todo item.
   * @param payload - The data for the new todo item, using CreateTodoPayload.
   * @returns The created TodoItem or null if an error occurred.
   */
  async addTodo(payload: CreateTodoPayload): Promise<TodoItem | null> { // Use CreateTodoPayload
    this._setLoading(true);
    this._setError(null);
    try {
      const newTodo = await todoService.createTodo(payload);
      if (newTodo) {
        this._store.update(state => ({
          ...state,
          todos: [...state.todos, newTodo],
        }));
        return newTodo;
      }
      return null;
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : 'Failed to add todo';
      console.error('Error adding todo:', message);
      this._setError(message);
      return null;
    } finally {
      this._setLoading(false);
    }
  }

  /**
   * Updates an existing todo item.
   * @param id - The ID of the todo item to update.
   * @param payload - The partial data to update the todo item with, using UpdateTodoPayload.
   * Note: UpdateTodoPayload from service might be more specific.
   * Here, we allow partial updates including completed_at and is_current_focus which might not be in UpdateTodoPayload.
   * It's better if UpdateTodoPayload itself includes these optional fields if they can be updated.
   * For now, using Partial<UpdateTodoPayload & { completed_at... }> for flexibility.
   */
  async updateTodo(id: number, payload: Partial<UpdateTodoPayload & { completed_at?: string | null, is_current_focus?: boolean }>): Promise<TodoItem | null> { // Use UpdateTodoPayload
    this._setLoading(true);
    this._setError(null);
    try {
      // The todoService.updateTodo will expect a payload conforming to what its UpdateTodoPayload allows.
      // We need to ensure the payload sent here is compatible.
      // If UpdateTodoPayload is strict, we might need to adjust how completed_at/is_current_focus are handled,
      // potentially by having more specific service methods if the backend API is structured that way.
      const updatedTodo = await todoService.updateTodo(id, payload as UpdateTodoPayload); // Cast if necessary, ensure compatibility
      if (updatedTodo) {
        this._updateTodoItemInStore(updatedTodo);
        return updatedTodo;
      }
      return null;
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : `Failed to update todo with ID ${id}`;
      console.error(`Error updating todo ${id}:`, message);
      this._setError(message);
      return null;
    } finally {
      this._setLoading(false);
    }
  }


  /**
   * Removes a todo item by its ID.
   * @param id - The ID of the todo item to remove.
   */
  async removeTodo(id: number): Promise<void> {
    this._setLoading(true);
    this._setError(null);
    try {
      await todoService.deleteTodo(id);
      this._removeTodoItemFromStore(id);
    } catch (e: unknown) {
      const message = e instanceof Error ? e.message : `Failed to delete todo with ID ${id}`;
      console.error(`Error deleting todo ${id}:`, message);
      this._setError(message);
    } finally {
      this._setLoading(false);
    }
  }

  /**
   * Retrieves a single todo item by its ID.
   * @param id - The ID of the todo item.
   * @returns The TodoItem or undefined if not found.
   */
  async getTodoById(id: number): Promise<TodoItem | undefined> {
    const existingTodo = get(this._store).todos.find(t => t.id === id);
    if (existingTodo) {
      return existingTodo;
    }
    // To fetch if not found:
    // this._setLoading(true);
    // try {
    //   const todo = await todoService.getTodoById(id); // Assuming todoService has getTodoById
    //   if (todo) this._updateTodoItemInStore(todo); 
    //   return todo;
    // } catch (e) { /* handle error */ } finally { this._setLoading(false); }
    return undefined;
  }

  // --- Derived Stores (Read-only access for components) ---
  get todos() {
    return derived(this._store, $s => $s.todos);
  }

  get isLoading() {
    return derived(this._store, $s => $s.isLoading);
  }

  get error() {
    return derived(this._store, $s => $s.error);
  }
}

// Create a singleton instance of the store
export const todoStore = new MainTodoStore();

// --- Additional Derived Stores for UI Logic ---

export const currentFocusTodos = derived(
  todoStore, 
  $todoStoreState => $todoStoreState.todos.filter(todo => todo.is_current_focus && !todo.completed_at)
);

export const otherActiveTodos = derived(
  todoStore, 
  $todoStoreState => $todoStoreState.todos.filter(todo => !todo.completed_at && !todo.is_current_focus)
);

export const completedTodos = derived(
  todoStore, 
  $todoStoreState => $todoStoreState.todos.filter(todo => !!todo.completed_at)
);
