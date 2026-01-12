"use client";

/**
 * TaskSuggestions component.
 *
 * Displays AI-powered task suggestions based on user context
 * and allows quick task creation from suggestions.
 */

import { useState, useEffect } from "react";
import { useTaskSuggestions, useAIStatus } from "@/hooks/useAI";

interface TaskSuggestionsProps {
  onCreateTask: (description: string, metadata?: any) => Promise<void>;
  userContext?: Record<string, any>;
  isVisible?: boolean;
}

export default function TaskSuggestions({ 
  onCreateTask, 
  userContext = {}, 
  isVisible = true 
}: TaskSuggestionsProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const { status: aiStatus } = useAIStatus();
  const { suggestions, isLoading, getSuggestions } = useTaskSuggestions();

  useEffect(() => {
    if (aiStatus?.available && isExpanded) {
      getSuggestions(5, userContext);
    }
  }, [aiStatus, isExpanded, userContext, getSuggestions]);

  const handleCreateFromSuggestion = async (suggestion: any) => {
    const metadata = {
      category: suggestion.category,
      priority: suggestion.priority,
      estimated_duration: suggestion.estimated_duration,
      ai_tags: JSON.stringify([suggestion.category]),
      ai_suggestions: JSON.stringify([suggestion.reasoning || "AI-suggested task"])
    };

    await onCreateTask(suggestion.description, metadata);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-50 border-red-200';
      case 'medium': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'low': return 'text-green-600 bg-green-50 border-green-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'work': return '💼';
      case 'personal': return '👤';
      case 'health': return '🏥';
      case 'learning': return '📚';
      case 'shopping': return '🛒';
      default: return '📝';
    }
  };

  if (!isVisible || !aiStatus?.available) {
    return null;
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200">
      {/* Header */}
      <div 
        className="p-4 cursor-pointer hover:bg-gray-50 transition"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <span className="text-lg mr-2">🤖</span>
            <h3 className="text-lg font-semibold text-gray-900">AI Task Suggestions</h3>
            <span className="ml-2 text-sm text-green-600 bg-green-100 px-2 py-1 rounded-full">
              Smart
            </span>
          </div>
          <div className="flex items-center">
            {suggestions.length > 0 && (
              <span className="text-sm text-gray-500 mr-2">
                {suggestions.length} suggestions
              </span>
            )}
            <svg
              className={`w-5 h-5 text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path d="M19 9l-7 7-7-7"></path>
            </svg>
          </div>
        </div>
      </div>

      {/* Content */}
      {isExpanded && (
        <div className="border-t border-gray-200">
          {isLoading ? (
            <div className="p-6 text-center">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto mb-3"></div>
              <p className="text-gray-600">Generating smart suggestions...</p>
            </div>
          ) : suggestions.length > 0 ? (
            <div className="p-4 space-y-3">
              {suggestions.map((suggestion, index) => (
                <div
                  key={index}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center mb-2">
                        <span className="mr-2">{getCategoryIcon(suggestion.category)}</span>
                        <span className="text-sm font-medium text-gray-500 capitalize">
                          {suggestion.category}
                        </span>
                        <span className={`ml-2 inline-flex px-2 py-1 text-xs font-medium rounded-full capitalize ${getPriorityColor(suggestion.priority)}`}>
                          {suggestion.priority}
                        </span>
                        {suggestion.estimated_duration && (
                          <span className="ml-2 text-xs text-gray-500">
                            ⏱️ {suggestion.estimated_duration}
                          </span>
                        )}
                      </div>
                      
                      <p className="text-gray-900 font-medium mb-2">
                        {suggestion.description}
                      </p>
                      
                      {suggestion.reasoning && (
                        <p className="text-sm text-gray-600 mb-3">
                          💡 {suggestion.reasoning}
                        </p>
                      )}
                    </div>
                  </div>
                  
                  <div className="flex justify-end">
                    <button
                      onClick={() => handleCreateFromSuggestion(suggestion)}
                      className="px-4 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 rounded-lg transition"
                    >
                      + Add Task
                    </button>
                  </div>
                </div>
              ))}
              
              <div className="pt-3 border-t border-gray-100">
                <button
                  onClick={() => getSuggestions(5, userContext)}
                  disabled={isLoading}
                  className="w-full px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-700 hover:bg-gray-50 rounded-lg transition disabled:opacity-50"
                >
                  🔄 Get New Suggestions
                </button>
              </div>
            </div>
          ) : (
            <div className="p-6 text-center">
              <div className="text-4xl mb-3">🤔</div>
              <p className="text-gray-600 mb-3">No suggestions available right now</p>
              <button
                onClick={() => getSuggestions(5, userContext)}
                className="px-4 py-2 text-sm font-medium text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 rounded-lg transition"
              >
                Generate Suggestions
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}