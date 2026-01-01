/**
 * API client for backend communication.
 *
 * Provides type-safe functions for all API endpoints with automatic
 * token management and error handling.
 */

import axios, { AxiosInstance, AxiosError } from "axios";
import {
  RegisterRequest,
  LoginRequest,
  TokenResponse,
  RefreshTokenRequest,
  User,
  Task,
  TaskCreate,
  TaskUpdate,
  TaskListResponse,
  APIError,
} from "@/types/api";


// ============================================================================
// Constants
// ============================================================================

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";


// ============================================================================
// Axios Instance
// ============================================================================

/**
 * Axios instance with base configuration.
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000, // 10 second timeout
});


// ============================================================================
// Token Management
// ============================================================================

/**
 * Set the access token for authenticated requests.
 * Adds Authorization header to all subsequent requests.
 */
export function setAuthToken(token: string | null): void {
  if (token) {
    apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  } else {
    delete apiClient.defaults.headers.common["Authorization"];
  }
}

/**
 * Get the current auth token from axios instance.
 */
export function getAuthToken(): string | null {
  const authHeader = apiClient.defaults.headers.common["Authorization"];
  if (typeof authHeader === "string" && authHeader.startsWith("Bearer ")) {
    return authHeader.substring(7);
  }
  return null;
}


// ============================================================================
// Error Handling
// ============================================================================

/**
 * Extract error message from API error response.
 */
export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<APIError>;
    if (axiosError.response?.data?.detail) {
      return axiosError.response.data.detail;
    }
    if (axiosError.message) {
      return axiosError.message;
    }
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "An unexpected error occurred";
}


// ============================================================================
// Authentication API
// ============================================================================

/**
 * Register a new user account.
 *
 * @param data - Registration request data
 * @returns Created user data
 * @throws APIError on validation or conflict errors
 */
export async function register(data: RegisterRequest): Promise<User> {
  const response = await apiClient.post<User>("/api/auth/register", data);
  return response.data;
}

/**
 * Login user and retrieve tokens.
 *
 * @param data - Login credentials
 * @returns Access and refresh tokens
 * @throws APIError on invalid credentials
 */
export async function login(data: LoginRequest): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>("/api/auth/login", data);
  return response.data;
}

/**
 * Logout user (client-side token removal).
 *
 * @returns Success message
 * @throws APIError if not authenticated
 */
export async function logout(): Promise<{ message: string }> {
  const response = await apiClient.post<{ message: string }>("/api/auth/logout");
  return response.data;
}

/**
 * Refresh access token using refresh token.
 *
 * @param data - Refresh token request
 * @returns New access token and same refresh token
 * @throws APIError if refresh token is invalid or expired
 */
export async function refreshToken(
  data: RefreshTokenRequest
): Promise<TokenResponse> {
  const response = await apiClient.post<TokenResponse>("/api/auth/refresh", data);
  return response.data;
}


// ============================================================================
// Task API
// ============================================================================

/**
 * Get all tasks for the authenticated user.
 *
 * @returns List of tasks with total count
 * @throws APIError if not authenticated
 */
export async function getTasks(): Promise<TaskListResponse> {
  const response = await apiClient.get<TaskListResponse>("/api/tasks");
  return response.data;
}

/**
 * Get a specific task by ID.
 *
 * @param taskId - Task ID
 * @returns Task object
 * @throws APIError if task not found or unauthorized
 */
export async function getTask(taskId: number): Promise<Task> {
  const response = await apiClient.get<Task>(`/api/tasks/${taskId}`);
  return response.data;
}

/**
 * Create a new task.
 *
 * @param data - Task creation data
 * @returns Created task object
 * @throws APIError on validation errors
 */
export async function createTask(data: TaskCreate): Promise<Task> {
  const response = await apiClient.post<Task>("/api/tasks", data);
  return response.data;
}

/**
 * Update a task's description.
 *
 * @param taskId - Task ID
 * @param data - Task update data
 * @returns Updated task object
 * @throws APIError if task not found, unauthorized, or validation errors
 */
export async function updateTask(taskId: number, data: TaskUpdate): Promise<Task> {
  const response = await apiClient.put<Task>(`/api/tasks/${taskId}`, data);
  return response.data;
}

/**
 * Delete a task.
 *
 * @param taskId - Task ID
 * @throws APIError if task not found or unauthorized
 */
export async function deleteTask(taskId: number): Promise<void> {
  await apiClient.delete(`/api/tasks/${taskId}`);
}

/**
 * Toggle a task's completion status.
 *
 * @param taskId - Task ID
 * @returns Updated task object with toggled status
 * @throws APIError if task not found or unauthorized
 */
export async function toggleTask(taskId: number): Promise<Task> {
  const response = await apiClient.patch<Task>(`/api/tasks/${taskId}/toggle`);
  return response.data;
}


// ============================================================================
// Export API Client
// ============================================================================

export default apiClient;
