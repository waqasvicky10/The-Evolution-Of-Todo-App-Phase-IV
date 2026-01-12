"use client";

/**
 * SmartTaskCreator component.
 *
 * AI-powered task creation with intelligent suggestions,
 * analysis, and description improvements.
 */

import { useState, useEffect } from "react";
import { useTaskAnalysis, useTaskImprovement, useAIStatus } from "@/hooks/useAI";

interface SmartTaskCreatorProps {
  onCreateTask: (description: string, metadata?: any) => Promise<void>;
  isLoading?: boolean;
}

export default function SmartTaskCreator({ onCreateTask, isLoading = false }: SmartTaskCreatorProps) {
  const [description, setDescription] = useState("");
  const [showAIFeatures, setShowAIFeatures] = useState(false);
  const [useImprovedDescription, setUseImprovedDescription] = useState(false);

  const { status: aiStatus, checkStatus } = useAIStatus();
  const { analysis, analyzeTask, isLoading: analyzing } = useTaskAnalysis();
  const { improvement, improveTask, isLoading: improving } = useTaskImprovement();

  useEffect(() => {
    checkStatus();
  }, [checkStatus]);

  const handleAnalyze = async () => {
    if (description.trim()) {
      await analyzeTask(description.trim());
      await improveTask(description.trim());
      setShowAIFeatures(true);
    }
  };

  const handleCreateTask = async () => {
    const finalDescription = useImprovedDescription && improvement?.improved 
      ? improvement.improved 
      : description.trim();

    const metadata = analysis ? {
      category: analysis.category,
      priority: analysis.priority,
      estimated_duration: analysis.estimated_duration,
      ai_tags: JSON.stringify(analysis.tags),
      ai_suggestions: JSON.stringify(analysis.suggestions)
    } : undefined;

    await onCreateTask(finalDescription, metadata);
    
    // Reset form
    setDescription("");
    setShowAIFeatures(false);
    setUseImprovedDescription(false);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'text-red-600 bg-red-50';
      case 'medium': return 'text-yellow-600 bg-yellow-50';
      case 'low': return 'text-green-600 bg-green-50';
      default: return 'text-gray-600 bg-gray-50';
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

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Create New Task</h3>
        {aiStatus?.available && (
          <div className="flex items-center text-sm text-green-600">
            <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
            AI Powered
          </div>
        )}
      </div>

      {/* Task Input */}
      <div className="space-y-4">
        <div>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Describe your task... (AI will help optimize it)"
            className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition resize-none"
            rows={3}
            disabled={isLoading}
          />
          <div className="flex justify-between items-center mt-2">
            <span className="text-xs text-gray-500">
              {description.length}/500 characters
            </span>
            {aiStatus?.available && description.trim() && !showAIFeatures && (
              <button
                onClick={handleAnalyze}
                disabled={analyzing || improving}
                className="text-sm text-indigo-600 hover:text-indigo-700 font-medium disabled:opacity-50"
              >
                {analyzing || improving ? "Analyzing..." : "✨ Enhance with AI"}
              </button>
            )}
          </div>
        </div>

        {/* AI Analysis Results */}
        {showAIFeatures && (analysis || improvement) && (
          <div className="border border-indigo-200 rounded-lg p-4 bg-indigo-50">
            <h4 className="font-medium text-indigo-900 mb-3">🤖 AI Analysis</h4>
            
            {/* Improved Description */}
            {improvement && improvement.improved !== improvement.original && (
              <div className="mb-4">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-sm font-medium text-gray-700">Improved Description:</span>
                  <label className="flex items-center text-sm">
                    <input
                      type="checkbox"
                      checked={useImprovedDescription}
                      onChange={(e) => setUseImprovedDescription(e.target.checked)}
                      className="mr-2 rounded"
                    />
                    Use improved version
                  </label>
                </div>
                <div className="bg-white p-3 rounded border">
                  <p className="text-gray-900">{improvement.improved}</p>
                </div>
              </div>
            )}

            {/* Analysis Details */}
            {analysis && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                <div>
                  <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Category</span>
                  <div className="flex items-center mt-1">
                    <span className="mr-2">{getCategoryIcon(analysis.category)}</span>
                    <span className="text-sm font-medium capitalize">{analysis.category}</span>
                  </div>
                </div>
                
                <div>
                  <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Priority</span>
                  <div className="mt-1">
                    <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full capitalize ${getPriorityColor(analysis.priority)}`}>
                      {analysis.priority}
                    </span>
                  </div>
                </div>
                
                {analysis.estimated_duration && (
                  <div>
                    <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Duration</span>
                    <div className="mt-1">
                      <span className="text-sm font-medium">⏱️ {analysis.estimated_duration}</span>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Tags */}
            {analysis?.tags && analysis.tags.length > 0 && (
              <div className="mb-4">
                <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">Tags</span>
                <div className="flex flex-wrap gap-2 mt-1">
                  {analysis.tags.map((tag, index) => (
                    <span
                      key={index}
                      className="inline-flex px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded-full"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Suggestions */}
            {analysis?.suggestions && analysis.suggestions.length > 0 && (
              <div>
                <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">AI Suggestions</span>
                <ul className="mt-1 space-y-1">
                  {analysis.suggestions.map((suggestion, index) => (
                    <li key={index} className="text-sm text-gray-600 flex items-start">
                      <span className="text-indigo-500 mr-2">•</span>
                      {suggestion}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex gap-3 justify-end">
          {showAIFeatures && (
            <button
              onClick={() => {
                setShowAIFeatures(false);
                setUseImprovedDescription(false);
              }}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition"
            >
              Cancel AI
            </button>
          )}
          
          <button
            onClick={handleCreateTask}
            disabled={!description.trim() || isLoading}
            className="px-6 py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 focus:ring-4 focus:ring-indigo-300 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {isLoading ? "Creating..." : showAIFeatures ? "Create Smart Task" : "Create Task"}
          </button>
        </div>
      </div>
    </div>
  );
}