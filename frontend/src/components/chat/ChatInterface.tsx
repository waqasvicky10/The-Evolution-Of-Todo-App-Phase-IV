"use client";

import React, { useState, useEffect, useRef } from "react";
import ChatMessage, { Message } from "./ChatMessage";
import ChatInput from "./ChatInput";
import axios from "axios";
import { useAuth } from "@/contexts/AuthContext";

/**
 * ChatInterface component.
 * 
 * Orchestrates the chat experience within the Next.js app.
 */

const API_BASE_URL = (process.env.NEXT_PUBLIC_API_BASE_URL || "").replace(/\/$/, "");

export default function ChatInterface() {
    const { user, accessToken } = useAuth();
    const [messages, setMessages] = useState<Message[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isLoading]);

    // Load conversation history on mount
    useEffect(() => {
        const loadHistory = async () => {
            if (!accessToken) return;

            try {
                const response = await axios.get(`${API_BASE_URL}/api/chat/history`, {
                    headers: { Authorization: `Bearer ${accessToken}` },
                    timeout: 30000  // 30 second timeout
                });
                setMessages(response.data.messages || []);
            } catch (err: any) {
                // Silently fail - history is optional, 404 is OK for now
                if (err.response?.status !== 404) {
                    console.error("Failed to load chat history:", err);
                }
                // Don't show error for missing history endpoint
            }
        };

        loadHistory();
    }, [accessToken]);

    const handleSendMessage = async (content: string) => {
        if (!accessToken) {
            setError("Please log in to chat.");
            return;
        }

        const userMessage: Message = {
            role: "user",
            content,
            timestamp: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setIsLoading(true);
        setError(null);

        try {
            const response = await axios.post(
                `${API_BASE_URL}/api/chat`,
                { message: content },
                { headers: { Authorization: `Bearer ${accessToken}` } }
            );

            const assistantMessage: Message = {
                role: "assistant",
                content: response.data.response,
                timestamp: new Date().toISOString(),
            };

            setMessages((prev) => [...prev, assistantMessage]);
        } catch (err: any) {
            console.error("Chat error:", err);
            const errorMessage = err.response?.data?.detail || "Something went wrong. Please try again.";
            setError(errorMessage);

            // Add a system message showing the error
            setMessages((prev) => [...prev, {
                role: "assistant",
                content: "I'm sorry, I'm having trouble connecting to the backend. Please make sure the Chat API and MCP Server are running.",
                timestamp: new Date().toISOString(),
            }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-[calc(100vh-160px)] max-w-5xl mx-auto bg-gray-50/50 rounded-2xl border border-gray-100 shadow-inner overflow-hidden">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-6 scroll-smooth">
                {messages.length === 0 && !isLoading && !error && (
                    <div className="flex flex-col items-center justify-center h-full text-center p-10">
                        <div className="bg-indigo-100 p-4 rounded-full mb-4">
                            <svg className="h-10 w-10 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
                            </svg>
                        </div>
                        <h3 className="text-xl font-semibold text-gray-900 mb-2">Welcome to AI Chat!</h3>
                        <p className="text-gray-500 max-w-sm">
                            I'm your todo assistant. You can ask me to add tasks, show your list, mark items as complete, or delete them.
                        </p>
                    </div>
                )}

                {messages.map((msg, index) => (
                    <ChatMessage key={index} message={msg} />
                ))}

                {isLoading && (
                    <div className="flex justify-start mb-6 animate-pulse">
                        <div className="h-10 w-10 bg-gray-200 rounded-full mr-3 shadow-none"></div>
                        <div className="p-4 bg-white border border-gray-100 rounded-2xl rounded-tl-none shadow-sm min-w-[100px]">
                            <div className="flex space-x-1">
                                <div className="h-2 w-2 bg-gray-300 rounded-full animate-bounce"></div>
                                <div className="h-2 w-2 bg-gray-300 rounded-full animate-bounce delay-75"></div>
                                <div className="h-2 w-2 bg-gray-300 rounded-full animate-bounce delay-150"></div>
                            </div>
                        </div>
                    </div>
                )}

                {error && (
                    <div className="bg-red-50 text-red-600 p-3 rounded-lg text-sm text-center mb-6">
                        {error}
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
    );
}
