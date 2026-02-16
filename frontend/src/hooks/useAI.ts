"use client";

/**
 * Custom hooks for AI-powered features.
 *
 * Provides React hooks for AI task analysis, suggestions, and improvements.
 */

import { useState, useCallback } from "react";
import axios from "axios";

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL || "").replace(/\/$/, "");

// ============================================================================
// Types
// ============================================================================

export interface TaskAnalysis {
  category: string;
  priority: string;
  tags: string[];
  estimated_duration?: string;
  suggestions: string[];
}

export interface TaskSuggestion {
  description: string;
  category: string;
  priority: string;
  estimated_duration?: string;
  reasoning?: string;
}

export interface AIStatus {
  available: boolean;
  message: string;
}

// ============================================================================
// useAIStatus Hook
// ============================================================================

export function useAIStatus() {
  const [status, setStatus] = useState<AIStatus | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const checkStatus = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      const response = await axios.get(`${API_BASE_URL}/api/ai/status`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });

      setStatus(response.data);
    } catch (err) {
      setError("Failed to check AI status");
      setStatus({ available: false, message: "AI service unavailable" });
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    status,
    isLoading,
    error,
    checkStatus,
  };
}

// ============================================================================
// useTaskAnalysis Hook
// ============================================================================

export function useTaskAnalysis() {
  const [analysis, setAnalysis] = useState<TaskAnalysis | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const analyzeTask = useCallback(async (description: string, userContext: Record<string, any> = {}) => {
    try {
      setIsLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Authentication required");
      }

      const response = await axios.post(
        `${API_BASE_URL}/api/ai/analyze-task`,
        {
          description,
          user_context: userContext,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      setAnalysis(response.data);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Failed to analyze task";
      setError(errorMessage);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setAnalysis(null);
    setError(null);
  }, []);

  return {
    analysis,
    isLoading,
    error,
    analyzeTask,
    reset,
  };
}

// ============================================================================
// useTaskSuggestions Hook
// ============================================================================

export function useTaskSuggestions() {
  const [suggestions, setSuggestions] = useState<TaskSuggestion[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const getSuggestions = useCallback(async (count: number = 5, userContext: Record<string, any> = {}) => {
    try {
      setIsLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Authentication required");
      }

      const response = await axios.post(
        `${API_BASE_URL}/api/ai/suggest-tasks`,
        {
          count,
          user_context: userContext,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      setSuggestions(response.data);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Failed to get task suggestions";
      setError(errorMessage);
      return [];
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setSuggestions([]);
    setError(null);
  }, []);

  return {
    suggestions,
    isLoading,
    error,
    getSuggestions,
    reset,
  };
}

// ============================================================================
// useTaskImprovement Hook
// ============================================================================

export function useTaskImprovement() {
  const [improvement, setImprovement] = useState<{ original: string; improved: string } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const improveTask = useCallback(async (description: string) => {
    try {
      setIsLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Authentication required");
      }

      const response = await axios.post(
        `${API_BASE_URL}/api/ai/improve-task`,
        { description },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      setImprovement(response.data);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Failed to improve task description";
      setError(errorMessage);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setImprovement(null);
    setError(null);
  }, []);

  return {
    improvement,
    isLoading,
    error,
    improveTask,
    reset,
  };
}

// ============================================================================
// useSmartTaskCreation Hook
// ============================================================================

export function useSmartTaskCreation() {
  const [smartTask, setSmartTask] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createSmartTask = useCallback(async (description: string, userContext: Record<string, any> = {}) => {
    try {
      setIsLoading(true);
      setError(null);

      const token = localStorage.getItem("access_token");
      if (!token) {
        throw new Error("Authentication required");
      }

      const response = await axios.post(
        `${API_BASE_URL}/api/ai/smart-create`,
        {
          description,
          user_context: userContext,
        },
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      setSmartTask(response.data);
      return response.data;
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || "Failed to create smart task";
      setError(errorMessage);
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setSmartTask(null);
    setError(null);
  }, []);

  return {
    smartTask,
    isLoading,
    error,
    createSmartTask,
    reset,
  };
}