"""
Gradio Todo App - Voice Input Example
This shows how easy it is to add voice input with Gradio
"""

import gradio as gr
import sqlite3
import os
from datetime import datetime
from typing import Optional

# Your existing database functions work here!
DB_PATH = "todo.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def process_chat_message(user_id: int, message: str) -> str:
    """Your existing function - works as-is!"""
    # This is your existing process_chat_message function
    # Just copy it from streamlit_app.py
    message_lower = message.lower().strip()
    
    # Simple intent recognition (your existing code)
    if any(word in message_lower for word in ["add", "create", "new"]):
        # Extract task description
        task_desc = message.replace("add", "").replace("task", "").replace("create", "").strip()
        if task_desc:
            # Create task in database
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (user_id, description, completed, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, task_desc, False, datetime.now().isoformat(), datetime.now().isoformat())
            )
            conn.commit()
            conn.close()
            return f"✅ Task added: {task_desc}"
    
    elif any(word in message_lower for word in ["list", "show", "display"]):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT description, completed FROM tasks WHERE user_id = ?", (user_id,))
        tasks = cursor.fetchall()
        conn.close()
        
        if tasks:
            task_list = "\n".join([f"{'✅' if t[1] else '⏳'} {t[0]}" for t in tasks])
            return f"📋 Your tasks:\n{task_list}"
        else:
            return "📋 No tasks found."
    
    return f"I understood: {message}. (Add your AI agent logic here)"

def process_input(audio_file, text_input, user_id: int = 1):
    """Process voice or text input"""
    if audio_file:
        # Option 1: Use OpenAI Whisper API for transcription
        # transcript = transcribe_with_whisper(audio_file)
        
        # Option 2: Use browser's Web Speech API (already transcribed)
        # For now, we'll use text input as fallback
        if text_input:
            transcript = text_input
        else:
            return "⚠️ Please speak clearly or type your message."
    else:
        transcript = text_input
    
    if not transcript or not transcript.strip():
        return "⚠️ Please provide a voice recording or type your message."
    
    # Use your existing function!
    response = process_chat_message(user_id, transcript.strip())
    return response

# Create Gradio Interface
with gr.Blocks(title="Todo App - Voice Enabled", theme=gr.themes.Soft()) as app:
    gr.Markdown("# 🤖 Todo App - AI Assistant with Voice Input")
    gr.Markdown("**Speak or type your todo commands!**")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🎤 Voice Input")
            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="Record your voice command",
                show_label=True
            )
            
            gr.Markdown("### ✍️ Or Type")
            text_input = gr.Textbox(
                label="Type your message",
                placeholder="e.g., 'add task buy groceries' or 'list my tasks'",
                lines=3
            )
            
            submit_btn = gr.Button("📤 Send", variant="primary", size="lg")
            clear_btn = gr.Button("🗑️ Clear", variant="secondary")
        
        with gr.Column(scale=1):
            gr.Markdown("### 💬 AI Response")
            output = gr.Textbox(
                label="Response",
                lines=15,
                interactive=False,
                show_copy_button=True
            )
            
            gr.Markdown("### 📋 Quick Commands")
            gr.Examples(
                examples=[
                    ["add task buy milk"],
                    ["list my tasks"],
                    ["add task call dentist"],
                    ["show all tasks"],
                ],
                inputs=text_input
            )
    
    # Event handlers
    submit_btn.click(
        fn=lambda audio, text: process_input(audio, text, user_id=1),
        inputs=[audio_input, text_input],
        outputs=output
    )
    
    text_input.submit(
        fn=lambda audio, text: process_input(audio, text, user_id=1),
        inputs=[audio_input, text_input],
        outputs=output
    )
    
    clear_btn.click(
        fn=lambda: ("", "", ""),
        outputs=[audio_input, text_input, output]
    )

if __name__ == "__main__":
    # Initialize database (your existing function)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    
    # Launch app
    # share=True creates a public URL (for testing)
    # Remove share=True for local-only access
    app.launch(
        share=False,  # Set to True for public URL
        server_name="0.0.0.0",
        server_port=7860
    )
