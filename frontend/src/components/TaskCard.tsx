"use client";

/**
 * TaskCard component.
 *
 * Displays a single task with toggle, edit, and delete functionality.
 * Supports inline editing mode.
 */

import { useState } from "react";
import { Task } from "@/types/api";


interface TaskCardProps {
  task: Task;
  onToggle: (taskId: number) => void;
  onUpdate: (taskId: number, description: string) => void;
  onDelete: (taskId: number) => void;
  isLoading?: boolean;
}


export default function TaskCard({
  task,
  onToggle,
  onUpdate,
  onDelete,
  isLoading = false,
}: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editingDescription, setEditingDescription] = useState(task.description);
  const [error, setError] = useState<string | null>(null);

  const handleStartEdit = () => {
    setIsEditing(true);
    setEditingDescription(task.description);
    setError(null);
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditingDescription(task.description);
    setError(null);
  };

  const handleSaveEdit = () => {
    setError(null);

    if (!editingDescription.trim()) {
      setError("Task description cannot be empty");
      return;
    }

    onUpdate(task.id, editingDescription.trim());
    setIsEditing(false);
  };

  const handleDelete = () => {
    if (confirm("Are you sure you want to delete this task?")) {
      onDelete(task.id);
    }
  };

  const cardClassName = task.is_complete
    ? "bg-gray-50 rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition"
    : "bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition";

  return (
    <div className={cardClassName}>
      {isEditing ? (
        // Edit mode
        <div>
          <div className="flex gap-3 mb-2">
            <input
              type="text"
              value={editingDescription}
              onChange={(e) => setEditingDescription(e.target.value)}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
              disabled={isLoading}
              autoFocus
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSaveEdit();
                } else if (e.key === "Escape") {
                  handleCancelEdit();
                }
              }}
            />
            <button
              onClick={handleSaveEdit}
              disabled={isLoading}
              className="px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              Save
            </button>
            <button
              onClick={handleCancelEdit}
              disabled={isLoading}
              className="px-4 py-2 bg-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed transition"
            >
              Cancel
            </button>
          </div>
          {error && (
            <div className="text-sm text-red-600 mt-1">{error}</div>
          )}
        </div>
      ) : (
        // View mode
        <div className="flex items-center gap-3">
          {/* Checkbox */}
          <input
            type="checkbox"
            checked={task.is_complete}
            onChange={() => onToggle(task.id)}
            disabled={isLoading}
            className="h-5 w-5 text-indigo-600 rounded border-gray-300 focus:ring-indigo-500 cursor-pointer disabled:cursor-not-allowed"
            title={task.is_complete ? "Mark as incomplete" : "Mark as complete"}
          />

          {/* Task description */}
          <span
            className={`flex-1 ${
              task.is_complete ? "text-gray-500 line-through" : "text-gray-900"
            }`}
          >
            {task.description}
          </span>

          {/* Action buttons */}
          <div className="flex gap-2">
            {!task.is_complete && (
              <button
                onClick={handleStartEdit}
                disabled={isLoading}
                className="px-3 py-1 text-sm text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 rounded-md transition disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Edit
              </button>
            )}
            <button
              onClick={handleDelete}
              disabled={isLoading}
              className="px-3 py-1 text-sm text-red-600 hover:text-red-700 hover:bg-red-50 rounded-md transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Delete
            </button>
          </div>
        </div>
      )}

      {/* Task metadata (timestamps) */}
      <div className="mt-2 text-xs text-gray-400 flex gap-4">
        <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
        {task.updated_at !== task.created_at && (
          <span>Updated: {new Date(task.updated_at).toLocaleDateString()}</span>
        )}
      </div>
    </div>
  );
}
