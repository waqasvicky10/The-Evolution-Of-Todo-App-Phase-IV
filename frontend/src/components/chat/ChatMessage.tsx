"use client";

import React from "react";

/**
 * ChatMessage component.
 * 
 * Displays individual chat messages from user or assistant.
 */

export interface Message {
    id?: string;
    role: "user" | "assistant";
    content: string;
    timestamp?: string;
}

interface ChatMessageProps {
    message: Message;
}

export default function ChatMessage({ message }: ChatMessageProps) {
    const isUser = message.role === "user";

    return (
        <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-6`}>
            <div className={`max-w-[80%] flex ${isUser ? "flex-row-reverse" : "flex-row"}`}>
                {/* Avatar */}
                <div className={`flex-shrink-0 h-10 w-10 rounded-full flex items-center justify-center text-white font-bold shadow-sm ${isUser ? "bg-indigo-600 ml-3" : "bg-gray-400 mr-3"
                    }`}>
                    {isUser ? "U" : "AI"}
                </div>

                {/* Bubble */}
                <div className={`flex flex-col ${isUser ? "items-end" : "items-start"}`}>
                    <div className={`p-4 rounded-2xl shadow-sm text-sm ${isUser
                            ? "bg-indigo-600 text-white rounded-tr-none"
                            : "bg-white border border-gray-100 text-gray-800 rounded-tl-none"
                        }`}>
                        <div className="whitespace-pre-wrap leading-relaxed">
                            {message.content}
                        </div>
                    </div>
                    {message.timestamp && (
                        <span className="text-[10px] text-gray-400 mt-1 px-1">
                            {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
}
