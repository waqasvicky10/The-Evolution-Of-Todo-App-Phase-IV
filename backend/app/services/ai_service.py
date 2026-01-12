"""
AI Service for OpenAI integration.

Provides intelligent task analysis, suggestions, and categorization
using OpenAI's GPT models.
"""

import json
import logging
from typing import List, Dict, Optional, Any
from openai import OpenAI
from pydantic import BaseModel
from ..config import settings

logger = logging.getLogger(__name__)


class TaskSuggestion(BaseModel):
    """Task suggestion from AI."""
    description: str
    category: str
    priority: str  # "high", "medium", "low"
    estimated_duration: Optional[str] = None
    reasoning: Optional[str] = None


class TaskAnalysis(BaseModel):
    """AI analysis of a task."""
    category: str
    priority: str
    tags: List[str]
    estimated_duration: Optional[str] = None
    suggestions: List[str] = []


class AIService:
    """Service for AI-powered task management features."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.client = None
        if settings.OPENAI_API_KEY:
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                self.client = None
        else:
            logger.warning("OpenAI API key not provided - AI features disabled")

    def is_available(self) -> bool:
        """Check if AI service is available."""
        return self.client is not None

    async def analyze_task(self, description: str, user_context: Optional[Dict] = None) -> TaskAnalysis:
        """
        Analyze a task description and provide AI insights.
        
        Args:
            description: Task description to analyze
            user_context: Optional user context for better analysis
            
        Returns:
            TaskAnalysis with category, priority, tags, and suggestions
        """
        if not self.is_available():
            return self._fallback_analysis(description)

        try:
            context_info = ""
            if user_context:
                context_info = f"User context: {json.dumps(user_context)}\n"

            prompt = f"""
            {context_info}
            Analyze this task and provide structured insights:
            Task: "{description}"
            
            Please respond with a JSON object containing:
            {{
                "category": "work|personal|health|learning|shopping|other",
                "priority": "high|medium|low",
                "tags": ["tag1", "tag2", "tag3"],
                "estimated_duration": "15 minutes|30 minutes|1 hour|2 hours|half day|full day",
                "suggestions": ["improvement suggestion 1", "improvement suggestion 2"]
            }}
            
            Consider:
            - Task complexity and urgency for priority
            - Logical categorization based on content
            - Relevant tags for organization
            - Realistic time estimation
            - Helpful suggestions for task completion
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a productivity assistant that analyzes tasks and provides structured insights in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )

            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            
            analysis_data = json.loads(content)
            return TaskAnalysis(**analysis_data)

        except Exception as e:
            logger.error(f"AI task analysis failed: {e}")
            return self._fallback_analysis(description)

    async def suggest_tasks(self, user_context: Dict, count: int = 5) -> List[TaskSuggestion]:
        """
        Generate task suggestions based on user context.
        
        Args:
            user_context: User's current tasks, preferences, and context
            count: Number of suggestions to generate
            
        Returns:
            List of TaskSuggestion objects
        """
        if not self.is_available():
            return self._fallback_suggestions()

        try:
            prompt = f"""
            Based on this user context, suggest {count} productive tasks:
            {json.dumps(user_context, indent=2)}
            
            Please respond with a JSON array of task suggestions:
            [
                {{
                    "description": "Clear, actionable task description",
                    "category": "work|personal|health|learning|shopping|other",
                    "priority": "high|medium|low",
                    "estimated_duration": "15 minutes|30 minutes|1 hour|2 hours",
                    "reasoning": "Why this task would be beneficial"
                }}
            ]
            
            Make suggestions that are:
            - Actionable and specific
            - Relevant to user's context
            - Varied in category and priority
            - Realistic and achievable
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a productivity coach that suggests helpful tasks based on user context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )

            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            if content.startswith("```json"):
                content = content[7:-3]
            elif content.startswith("```"):
                content = content[3:-3]
            
            suggestions_data = json.loads(content)
            return [TaskSuggestion(**suggestion) for suggestion in suggestions_data]

        except Exception as e:
            logger.error(f"AI task suggestions failed: {e}")
            return self._fallback_suggestions()

    async def improve_task_description(self, description: str) -> str:
        """
        Improve a task description to be more clear and actionable.
        
        Args:
            description: Original task description
            
        Returns:
            Improved task description
        """
        if not self.is_available():
            return description

        try:
            prompt = f"""
            Improve this task description to be more clear, specific, and actionable:
            Original: "{description}"
            
            Guidelines:
            - Keep it concise but specific
            - Make it actionable with clear outcome
            - Use active voice
            - Include relevant details
            - Maximum 100 characters
            
            Return only the improved description, no explanation.
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a writing assistant that improves task descriptions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.3
            )

            improved = response.choices[0].message.content.strip()
            return improved if len(improved) <= 100 else description

        except Exception as e:
            logger.error(f"AI task improvement failed: {e}")
            return description

    def _fallback_analysis(self, description: str) -> TaskAnalysis:
        """Provide basic analysis when AI is unavailable."""
        # Simple keyword-based categorization
        description_lower = description.lower()
        
        if any(word in description_lower for word in ['work', 'meeting', 'project', 'deadline', 'report']):
            category = 'work'
        elif any(word in description_lower for word in ['buy', 'shop', 'purchase', 'order']):
            category = 'shopping'
        elif any(word in description_lower for word in ['exercise', 'gym', 'health', 'doctor']):
            category = 'health'
        elif any(word in description_lower for word in ['learn', 'study', 'read', 'course']):
            category = 'learning'
        else:
            category = 'personal'

        # Simple priority detection
        if any(word in description_lower for word in ['urgent', 'asap', 'important', 'critical']):
            priority = 'high'
        elif any(word in description_lower for word in ['later', 'sometime', 'eventually']):
            priority = 'low'
        else:
            priority = 'medium'

        return TaskAnalysis(
            category=category,
            priority=priority,
            tags=[category],
            estimated_duration="30 minutes",
            suggestions=["Break down into smaller steps if needed"]
        )

    def _fallback_suggestions(self) -> List[TaskSuggestion]:
        """Provide basic suggestions when AI is unavailable."""
        return [
            TaskSuggestion(
                description="Review and organize your task list",
                category="personal",
                priority="medium",
                estimated_duration="15 minutes",
                reasoning="Regular organization improves productivity"
            ),
            TaskSuggestion(
                description="Plan tomorrow's priorities",
                category="personal",
                priority="medium",
                estimated_duration="10 minutes",
                reasoning="Planning ahead reduces stress and improves focus"
            ),
            TaskSuggestion(
                description="Take a 5-minute break and stretch",
                category="health",
                priority="low",
                estimated_duration="5 minutes",
                reasoning="Regular breaks improve focus and well-being"
            )
        ]


# Global AI service instance
ai_service = AIService()