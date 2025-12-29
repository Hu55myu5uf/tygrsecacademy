"""
AI Service using Google Gemini API (new google-genai package)
Handles all AI-powered features: tutoring, hints, analysis, recommendations
"""
import logging
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types
import json
from datetime import datetime

from config import settings
from models.ai_context import AIConversation
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# Initialize Gemini client with the new SDK
client = genai.Client(api_key=settings.GEMINI_API_KEY)


class AIService:
    """AI service for context-aware tutoring and assistance"""
    
    @staticmethod
    async def get_tutor_response(
        user_id: int,
        context_type: str,
        context_id: int,
        user_message: str,
        context_data: Dict[str, Any],
        db: Session,
        conversation_history: Optional[List[AIConversation]] = None
    ) -> Dict[str, Any]:
        """
        Get AI tutor response with context awareness
        
        Args:
            user_id: ID of the user
            context_type: Type of context (lesson, lab, challenge)
            context_id: ID of the context item
            user_message: User's question
            context_data: Additional context (lesson content, lab details, etc.)
            db: Database session
            conversation_history: Previous conversation messages
            
        Returns:
            Dict with response, tokens_used, and response_time
        """
        start_time = datetime.now()
        
        try:
            # Build context prompt
            system_prompt = AIService._build_tutor_system_prompt(context_type, context_data)
            
            # Build conversation contents for Gemini
            contents = []
            
            # Add conversation history if available
            if conversation_history:
                for conv in conversation_history[-5:]:  # Last 5 messages for context
                    contents.append(types.Content(
                        role="user",
                        parts=[types.Part(text=conv.user_message)]
                    ))
                    contents.append(types.Content(
                        role="model", 
                        parts=[types.Part(text=conv.ai_response)]
                    ))
            
            # Combine system prompt with user message
            if not contents:
                full_message = f"{system_prompt}\n\n---\n\nStudent Question: {user_message}"
            else:
                full_message = user_message
            
            # Add current message
            contents.append(types.Content(
                role="user",
                parts=[types.Part(text=full_message)]
            ))
            
            # Get response from Gemini using new SDK
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=contents,
                config=types.GenerateContentConfig(
                    max_output_tokens=settings.GEMINI_MAX_TOKENS,
                    temperature=0.7,
                )
            )
            
            # Extract response text
            ai_response = response.text
            
            # Estimate token usage
            tokens_used = len(full_message.split()) + len(ai_response.split())
            
            # Calculate response time
            response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
            
            # Store conversation in database
            conversation = AIConversation(
                user_id=user_id,
                context_type=context_type,
                context_id=context_id,
                user_message=user_message,
                ai_response=ai_response,
                tokens_used=tokens_used,
                response_time_ms=response_time_ms,
                model_used=settings.GEMINI_MODEL
            )
            db.add(conversation)
            db.commit()
            
            logger.info(f"AI tutor response generated for user {user_id} - {tokens_used} tokens, {response_time_ms}ms")
            
            return {
                "response": ai_response,
                "tokens_used": tokens_used,
                "response_time_ms": response_time_ms
            }
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise Exception(f"AI service error: {str(e)}")
    
    @staticmethod
    def _build_tutor_system_prompt(context_type: str, context_data: Dict[str, Any]) -> str:
        """Build system prompt based on context"""
        base_prompt = """You are an expert cybersecurity instructor and AI tutor for TygrSecAcademy, a professional cybersecurity education platform. Your role is to help students learn cybersecurity concepts through clear explanations, guided problem-solving, and encouragement.

Key principles:
1. Be educational, not just informative - help students understand WHY things work
2. Use analogies and examples to explain complex concepts
3. Encourage critical thinking by asking guiding questions
4. Never give direct answers to challenges or labs - guide students to discover solutions
5. Be supportive and encouraging, especially when students struggle
6. Reference industry best practices and real-world applications
7. Adapt your explanations to the student's apparent skill level"""
        
        if context_type == "lesson":
            lesson_prompt = f"""

Current Context: Lesson
Topic: {context_data.get('title', 'Unknown')}
Content Summary: {context_data.get('description', '')}

Focus on helping the student understand the lesson material. Provide clear explanations, examples, and check understanding."""
            return base_prompt + lesson_prompt
            
        elif context_type == "lab":
            lab_prompt = f"""

Current Context: Hands-on Lab
Lab Title: {context_data.get('title', 'Unknown')}
Objectives: {json.dumps(context_data.get('objectives', []))}

The student is working on a hands-on lab. Guide them through problem-solving WITHOUT giving direct answers. Use the Socratic method - ask questions that lead them to discover solutions themselves. Focus on teaching methodology and approach rather than specific commands or solutions."""
            return base_prompt + lab_prompt
            
        elif context_type == "challenge":
            challenge_prompt = f"""

Current Context: CTF Challenge
Challenge: {context_data.get('title', 'Unknown')}
Category: {context_data.get('category', 'Unknown')}
Difficulty: {context_data.get('difficulty', 'Unknown')}

The student is working on a CTF challenge. You must be VERY careful not to spoil the solution. Provide conceptual guidance, point them to relevant resources, and help them develop their problem-solving approach. NEVER reveal flags, specific exploits, or step-by-step solutions."""
            return base_prompt + challenge_prompt
        
        return base_prompt
    
    @staticmethod
    async def generate_hint(
        hint_level: int,
        context_type: str,
        context_data: Dict[str, Any],
        student_actions: Optional[List[str]] = None
    ) -> str:
        """
        Generate progressive hint based on level
        
        Args:
            hint_level: 1 (gentle), 2 (specific), 3 (direct)
            context_type: lab or challenge
            context_data: Details about the task
            student_actions: Previous actions taken by student
            
        Returns:
            Generated hint text
        """
        try:
            prompt = f"""Generate a hint for a student working on a cybersecurity {context_type}.

Task: {context_data.get('title')}
Description: {context_data.get('description')}
Objectives: {json.dumps(context_data.get('objectives', []))}

Hint Level: {hint_level}
- Level 1: Gentle nudge, point to general concept/area
- Level 2: More specific, mention tool or technique
- Level 3: Direct guidance, but still make them execute

Student's previous actions: {json.dumps(student_actions) if student_actions else 'None yet'}

Generate an appropriate hint for level {hint_level}. Keep it concise (2-3 sentences max)."""
            
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=300,
                )
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Error generating hint: {str(e)}")
            return f"Unable to generate hint at this time. Please review the {context_type} objectives."
    
    @staticmethod
    async def analyze_lab_action(
        action: str,
        lab_context: Dict[str, Any],
        expected_outcome: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze a student's lab action and provide feedback
        
        Args:
            action: The action/command executed
            lab_context: Lab details and objectives
            expected_outcome: Expected result (if available)
            
        Returns:
            Dict with is_correct, feedback, and suggestions
        """
        try:
            prompt = f"""Analyze a student's action in a cybersecurity lab exercise.

Lab: {lab_context.get('title')}
Objectives: {json.dumps(lab_context.get('objectives', []))}
Student Action: {action}
Expected Outcome: {expected_outcome or 'Not specified'}

Provide brief feedback:
1. Is this action productive/correct for achieving the objectives?
2. What would be the likely outcome?
3. One suggestion for improvement or next step

Keep it encouraging and educational. Format as JSON with keys: is_productive, feedback, next_step"""
            
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=400,
                )
            )
            
            # Parse response
            try:
                result = json.loads(response.text)
                return result
            except:
                return {
                    "is_productive": True,
                    "feedback": response.text,
                    "next_step": "Continue exploring"
                }
                
        except Exception as e:
            logger.error(f"Error analyzing lab action: {str(e)}")
            return {
                "is_productive": True,
                "feedback": "Action recorded",
                "next_step": "Continue working through the lab objectives"
            }
    
    @staticmethod
    async def recommend_next_content(
        user_progress: Dict[str, Any],
        available_content: List[Dict[str, Any]]
    ) -> List[int]:
        """
        Recommend next modules/challenges based on user progress
        
        Args:
            user_progress: User's completion data and strengths/weaknesses
            available_content: List of available modules/challenges
            
        Returns:
            List of recommended content IDs in priority order
        """
        try:
            prompt = f"""Based on a student's progress, recommend the next 3-5 learning activities.

Student Progress:
- Current Tier: {user_progress.get('current_tier')}
- Completed Modules: {user_progress.get('modules_completed')}
- Challenges Solved: {user_progress.get('challenges_solved')}
- Strengths: {json.dumps(user_progress.get('strengths', []))}
- Areas for Improvement: {json.dumps(user_progress.get('weaknesses', []))}

Available Content:
{json.dumps(available_content, indent=2)}

Recommend 3-5 items by ID that would best help the student progress. Consider:
1. Building on strengths
2. Addressing weak areas
3. Natural progression path
4. Variety in content types

Return only a JSON array of IDs in priority order: [id1, id2, id3, ...]"""
            
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=200,
                )
            )
            
            # Parse recommended IDs
            try:
                recommended_ids = json.loads(response.text)
                return recommended_ids[:5]  # Max 5 recommendations
            except:
                # Fallback: return first 3 available
                return [item['id'] for item in available_content[:3]]
                
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return []


# Export singleton instance
ai_service = AIService()
