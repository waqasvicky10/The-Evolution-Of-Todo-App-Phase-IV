/**
 * TypeScript type definitions for API models.
 *
 * These types mirror the backend Pydantic schemas to provide
 * type safety for API requests and responses.
 */


// ============================================================================
// User Types
// ============================================================================

/**
 * User response from API.
 * Returned after registration and in user profile endpoints.
 */
export interface User {
  id: number;
  email: string;
  created_at: string;
}


// ============================================================================
// Authentication Types
// ============================================================================

/**
 * User registration request.
 */
export interface RegisterRequest {
  email: string;
  password: string;
  password_confirmation: string;
}

/**
 * User login request.
 */
export interface LoginRequest {
  email: string;
  password: string;
}

/**
 * Token response from login and refresh endpoints.
 */
export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

/**
 * Refresh token request.
 */
export interface RefreshTokenRequest {
  refresh_token: string;
}


// ============================================================================
// Task Types
// ============================================================================

/**
 * Task object returned from API.
 */
export interface Task {
  id: number;
  description: string;
  is_complete: boolean;
  user_id: number;
  created_at: string;
  updated_at: string;
}

/**
 * Task creation request.
 */
export interface TaskCreate {
  description: string;
}

/**
 * Task update request.
 */
export interface TaskUpdate {
  description: string;
}

/**
 * Task list response from GET /api/tasks.
 */
export interface TaskListResponse {
  tasks: Task[];
  total: number;
}


// ============================================================================
// Error Types
// ============================================================================

/**
 * API error response structure.
 * FastAPI returns errors in this format.
 */
export interface APIError {
  detail: string;
}

/**
 * Validation error detail from FastAPI.
 */
export interface ValidationErrorDetail {
  loc: (string | number)[];
  msg: string;
  type: string;
}

/**
 * Validation error response (422 status).
 */
export interface ValidationError {
  detail: ValidationErrorDetail[];
}
