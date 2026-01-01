"use client";

/**
 * Dashboard page (/dashboard).
 *
 * Main authenticated page where users can view, create, update,
 * delete, and toggle their tasks. Protected route - requires login.
 */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/contexts/AuthContext";
import { useTasks, useCreateTask, useUpdateTask, useDeleteTask, useToggleTask } from "@/hooks/useTasks";
import Navbar from "@/components/Navbar";
import TaskCard from "@/components/TaskCard";


export default function DashboardPage() {
  const { isAuthenticated, isLoading: authLoading } = useAuth();
  const { tasks, isLoading: tasksLoading, error: tasksError, refetch } = useTasks();
  const { createTask, isLoading: createLoading } = useCreateTask();
  const { updateTask } = useUpdateTask();
  const { deleteTask } = useDeleteTask();
  const { toggleTask } = useToggleTask();
  const router = useRouter();

  const [newTaskDescription, setNewTaskDescription] = useState("");
  const [error, setError] = useState<string | null>(null);

  // Redirect to login if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [authLoading, isAuthenticated, router]);

  // Show loading state while checking authentication
  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  // Don't render if not authenticated (will redirect)
  if (!isAuthenticated) {
    return null;
  }

  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!newTaskDescription.trim()) {
      setError("Task description cannot be empty");
      return;
    }

    const task = await createTask({ description: newTaskDescription.trim() });
    if (task) {
      setNewTaskDescription("");
      refetch();
    }
  };

  const handleToggleTask = async (taskId: number) => {
    const updatedTask = await toggleTask(taskId);
    if (updatedTask) {
      refetch();
    }
  };

  const handleUpdateTask = async (taskId: number, description: string) => {
    const updatedTask = await updateTask(taskId, { description });
    if (updatedTask) {
      refetch();
    }
  };

  const handleDeleteTask = async (taskId: number) => {
    const success = await deleteTask(taskId);
    if (success) {
      refetch();
    }
  };

  // Filter tasks
  const incompleteTasks = tasks.filter(task => !task.is_complete);
  const completedTasks = tasks.filter(task => task.is_complete);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <Navbar />

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">My Tasks</h2>
          <p className="text-gray-600">
            {tasks.length} total task{tasks.length !== 1 ? "s" : ""} ({incompleteTasks.length} active, {completedTasks.length} completed)
          </p>
        </div>

        {/* Create Task Form */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Create New Task</h3>
          <form onSubmit={handleCreateTask} className="flex gap-3">
            <input
              type="text"
              value={newTaskDescription}
              onChange={(e) => setNewTaskDescription(e.target.value)}
              placeholder="Enter task description..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition"
              disabled={createLoading}
            />
            <button
              type="submit"
              disabled={createLoading}
              className="px-6 py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-300 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              {createLoading ? "Adding..." : "Add Task"}
            </button>
          </form>
          {error && (
            <div className="mt-3 text-sm text-red-600">{error}</div>
          )}
        </div>

        {/* Tasks Error */}
        {tasksError && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {tasksError}
          </div>
        )}

        {/* Tasks Loading */}
        {tasksLoading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Loading tasks...</p>
          </div>
        )}

        {/* Tasks List */}
        {!tasksLoading && (
          <div className="space-y-6">
            {/* Active Tasks */}
            {incompleteTasks.length > 0 && (
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Active Tasks</h3>
                <div className="space-y-3">
                  {incompleteTasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onToggle={handleToggleTask}
                      onUpdate={handleUpdateTask}
                      onDelete={handleDeleteTask}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Completed Tasks */}
            {completedTasks.length > 0 && (
              <div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Completed Tasks</h3>
                <div className="space-y-3">
                  {completedTasks.map((task) => (
                    <TaskCard
                      key={task.id}
                      task={task}
                      onToggle={handleToggleTask}
                      onUpdate={handleUpdateTask}
                      onDelete={handleDeleteTask}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Empty State */}
            {tasks.length === 0 && (
              <div className="text-center py-12 bg-white rounded-lg shadow-sm border border-gray-200">
                <div className="text-5xl mb-4">📝</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No tasks yet</h3>
                <p className="text-gray-600">Create your first task to get started!</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}
