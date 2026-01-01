"use client";

/**
 * Custom hooks for task API operations.
 *
 * Provides React hooks with loading states, error handling,
 * and automatic re-fetching for task CRUD operations.
 */

import { useState, useEffect, useCallback } from "react";
import {
  getTasks,
  createTask as apiCreateTask,
  updateTask as apiUpdateTask,
  deleteTask as apiDeleteTask,
  toggleTask as apiToggleTask,
  getErrorMessage,
} from "@/lib/api";
import { Task, TaskCreate, TaskUpdate } from "@/types/api";


// ============================================================================
// useTasks Hook
// ============================================================================

/**
 * Hook to fetch and manage all tasks for the authenticated user.
 *
 * @returns Tasks array, loading state, error, and refetch function
 */
export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await getTasks();
      setTasks(response.tasks);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  return {
    tasks,
    isLoading,
    error,
    refetch: fetchTasks,
  };
}


// ============================================================================
// useCreateTask Hook
// ============================================================================

/**
 * Hook to create a new task.
 *
 * @returns Create function, loading state, error, and success state
 */
export function useCreateTask() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const createTask = useCallback(async (data: TaskCreate): Promise<Task | null> => {
    try {
      setIsLoading(true);
      setError(null);
      setSuccess(false);
      const task = await apiCreateTask(data);
      setSuccess(true);
      return task;
    } catch (err) {
      setError(getErrorMessage(err));
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setError(null);
    setSuccess(false);
  }, []);

  return {
    createTask,
    isLoading,
    error,
    success,
    reset,
  };
}


// ============================================================================
// useUpdateTask Hook
// ============================================================================

/**
 * Hook to update a task's description.
 *
 * @returns Update function, loading state, error, and success state
 */
export function useUpdateTask() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const updateTask = useCallback(
    async (taskId: number, data: TaskUpdate): Promise<Task | null> => {
      try {
        setIsLoading(true);
        setError(null);
        setSuccess(false);
        const task = await apiUpdateTask(taskId, data);
        setSuccess(true);
        return task;
      } catch (err) {
        setError(getErrorMessage(err));
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const reset = useCallback(() => {
    setError(null);
    setSuccess(false);
  }, []);

  return {
    updateTask,
    isLoading,
    error,
    success,
    reset,
  };
}


// ============================================================================
// useDeleteTask Hook
// ============================================================================

/**
 * Hook to delete a task.
 *
 * @returns Delete function, loading state, error, and success state
 */
export function useDeleteTask() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const deleteTask = useCallback(async (taskId: number): Promise<boolean> => {
    try {
      setIsLoading(true);
      setError(null);
      setSuccess(false);
      await apiDeleteTask(taskId);
      setSuccess(true);
      return true;
    } catch (err) {
      setError(getErrorMessage(err));
      return false;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setError(null);
    setSuccess(false);
  }, []);

  return {
    deleteTask,
    isLoading,
    error,
    success,
    reset,
  };
}


// ============================================================================
// useToggleTask Hook
// ============================================================================

/**
 * Hook to toggle a task's completion status.
 *
 * @returns Toggle function, loading state, and error
 */
export function useToggleTask() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const toggleTask = useCallback(async (taskId: number): Promise<Task | null> => {
    try {
      setIsLoading(true);
      setError(null);
      const task = await apiToggleTask(taskId);
      return task;
    } catch (err) {
      setError(getErrorMessage(err));
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setError(null);
  }, []);

  return {
    toggleTask,
    isLoading,
    error,
    reset,
  };
}
