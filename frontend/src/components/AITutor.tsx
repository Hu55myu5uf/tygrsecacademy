import { useState, useEffect, useRef } from 'react';
import { MessageSquare, Send, X, Trash2, Lightbulb, Loader2, Bot, User, ChevronDown, ChevronUp } from 'lucide-react';
import { aiService } from '../services/api';
import ReactMarkdown from 'react-markdown';

interface Message {
    id?: number;
    role: 'user' | 'assistant';
    content: string;
    timestamp?: string;
}

interface AITutorProps {
    contextType: 'lesson' | 'lab' | 'challenge';
    contextId: number;
    contextTitle?: string;
}

export default function AITutor({ contextType, contextId, contextTitle }: AITutorProps) {
    const [isOpen, setIsOpen] = useState(false);
    const [isMinimized, setIsMinimized] = useState(false);
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [hintLevel, setHintLevel] = useState(1);
    const [error, setError] = useState<string | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    // Load conversation history when context changes
    useEffect(() => {
        if (isOpen && contextId) {
            loadHistory();
        }
    }, [contextType, contextId, isOpen]);

    // Scroll to bottom when messages change
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Focus input when opened
    useEffect(() => {
        if (isOpen && !isMinimized) {
            inputRef.current?.focus();
        }
    }, [isOpen, isMinimized]);

    const loadHistory = async () => {
        try {
            const history = await aiService.getHistory(contextType, contextId);
            const formattedMessages: Message[] = [];
            history.forEach((item: any) => {
                formattedMessages.push({
                    id: item.id,
                    role: 'user',
                    content: item.user_message,
                    timestamp: item.created_at
                });
                formattedMessages.push({
                    role: 'assistant',
                    content: item.ai_response,
                    timestamp: item.created_at
                });
            });
            setMessages(formattedMessages);
        } catch (err) {
            console.error('Failed to load history:', err);
        }
    };

    const sendMessage = async () => {
        if (!inputValue.trim() || isLoading) return;

        const userMessage = inputValue.trim();
        setInputValue('');
        setError(null);

        // Add user message to chat
        setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
        setIsLoading(true);

        try {
            const response = await aiService.sendMessage(userMessage, contextType, contextId);
            setMessages(prev => [...prev, { role: 'assistant', content: response.response }]);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to get response. Please try again.');
            // Remove the user message if there was an error
            setMessages(prev => prev.slice(0, -1));
            setInputValue(userMessage); // Restore the input
        } finally {
            setIsLoading(false);
        }
    };

    const getHint = async () => {
        if (isLoading || (contextType !== 'lab' && contextType !== 'challenge')) return;

        setError(null);
        setIsLoading(true);

        try {
            const response = await aiService.getHint(contextType, contextId, hintLevel);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: `💡 **Hint (Level ${response.level}):**\n\n${response.hint}`
            }]);
            // Increment hint level for next request (max 3)
            if (hintLevel < 3) {
                setHintLevel(prev => prev + 1);
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to get hint.');
        } finally {
            setIsLoading(false);
        }
    };

    const clearHistory = async () => {
        if (!confirm('Clear all conversation history for this context?')) return;

        try {
            await aiService.clearHistory(contextType, contextId);
            setMessages([]);
            setHintLevel(1);
        } catch (err) {
            console.error('Failed to clear history:', err);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    // Floating button when closed
    if (!isOpen) {
        return (
            <button
                onClick={() => setIsOpen(true)}
                className="fixed bottom-6 right-6 bg-gradient-to-r from-cyan-500 to-blue-600 text-white p-4 rounded-full shadow-lg hover:shadow-cyan-500/25 hover:scale-110 transition-all duration-300 z-50 group"
                title="Open AI Tutor"
            >
                <Bot className="w-6 h-6" />
                <span className="absolute right-full mr-3 bg-gray-900 text-white text-sm px-3 py-1 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                    AI Tutor
                </span>
            </button>
        );
    }

    return (
        <div className={`fixed bottom-6 right-6 bg-gray-900 border border-gray-700 rounded-2xl shadow-2xl shadow-cyan-500/10 z-50 flex flex-col transition-all duration-300 ${isMinimized ? 'w-80 h-14' : 'w-96 h-[32rem]'}`}>
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-700 bg-gradient-to-r from-gray-800 to-gray-900 rounded-t-2xl">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full flex items-center justify-center">
                        <Bot className="w-5 h-5 text-white" />
                    </div>
                    <div className="flex flex-col">
                        <span className="text-white font-semibold text-sm">AI Tutor</span>
                        {contextTitle && !isMinimized && (
                            <span className="text-gray-400 text-xs truncate max-w-[180px]">{contextTitle}</span>
                        )}
                    </div>
                </div>
                <div className="flex items-center gap-1">
                    {!isMinimized && (
                        <button
                            onClick={clearHistory}
                            className="p-1.5 text-gray-400 hover:text-red-400 hover:bg-gray-800 rounded-lg transition-colors"
                            title="Clear history"
                        >
                            <Trash2 className="w-4 h-4" />
                        </button>
                    )}
                    <button
                        onClick={() => setIsMinimized(!isMinimized)}
                        className="p-1.5 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
                    >
                        {isMinimized ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </button>
                    <button
                        onClick={() => setIsOpen(false)}
                        className="p-1.5 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
                    >
                        <X className="w-4 h-4" />
                    </button>
                </div>
            </div>

            {!isMinimized && (
                <>
                    {/* Messages */}
                    <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        {messages.length === 0 && (
                            <div className="text-center text-gray-400 py-8">
                                <Bot className="w-12 h-12 mx-auto mb-3 text-gray-600" />
                                <p className="text-sm">Hi! I'm your AI tutor.</p>
                                <p className="text-xs mt-1">Ask me anything about this {contextType}.</p>
                            </div>
                        )}

                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={`flex gap-2 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                {msg.role === 'assistant' && (
                                    <div className="w-7 h-7 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                                        <Bot className="w-4 h-4 text-white" />
                                    </div>
                                )}
                                <div
                                    className={`max-w-[80%] rounded-2xl px-4 py-2 ${msg.role === 'user'
                                            ? 'bg-cyan-600 text-white rounded-br-sm'
                                            : 'bg-gray-800 text-gray-100 rounded-bl-sm'
                                        }`}
                                >
                                    {msg.role === 'assistant' ? (
                                        <div className="prose prose-invert prose-sm max-w-none">
                                            <ReactMarkdown>{msg.content}</ReactMarkdown>
                                        </div>
                                    ) : (
                                        <p className="text-sm">{msg.content}</p>
                                    )}
                                </div>
                                {msg.role === 'user' && (
                                    <div className="w-7 h-7 bg-gray-700 rounded-full flex items-center justify-center flex-shrink-0">
                                        <User className="w-4 h-4 text-gray-300" />
                                    </div>
                                )}
                            </div>
                        ))}

                        {isLoading && (
                            <div className="flex gap-2 justify-start">
                                <div className="w-7 h-7 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-full flex items-center justify-center">
                                    <Bot className="w-4 h-4 text-white" />
                                </div>
                                <div className="bg-gray-800 rounded-2xl rounded-bl-sm px-4 py-3">
                                    <div className="flex gap-1">
                                        <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                        <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                        <div className="w-2 h-2 bg-cyan-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                    </div>
                                </div>
                            </div>
                        )}

                        {error && (
                            <div className="bg-red-900/30 border border-red-700 text-red-300 text-sm px-4 py-2 rounded-lg">
                                {error}
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>

                    {/* Hint Button (for labs and challenges) */}
                    {(contextType === 'lab' || contextType === 'challenge') && (
                        <div className="px-4 pb-2">
                            <button
                                onClick={getHint}
                                disabled={isLoading}
                                className="w-full flex items-center justify-center gap-2 bg-amber-600/20 hover:bg-amber-600/30 text-amber-400 py-2 rounded-lg text-sm transition-colors disabled:opacity-50"
                            >
                                <Lightbulb className="w-4 h-4" />
                                Get Hint (Level {hintLevel}/3)
                            </button>
                        </div>
                    )}

                    {/* Input */}
                    <div className="p-4 border-t border-gray-700">
                        <div className="flex gap-2">
                            <input
                                ref={inputRef}
                                type="text"
                                value={inputValue}
                                onChange={(e) => setInputValue(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Ask a question..."
                                disabled={isLoading}
                                className="flex-1 bg-gray-800 text-white placeholder-gray-500 px-4 py-2 rounded-xl border border-gray-700 focus:border-cyan-500 focus:outline-none text-sm disabled:opacity-50"
                            />
                            <button
                                onClick={sendMessage}
                                disabled={isLoading || !inputValue.trim()}
                                className="bg-gradient-to-r from-cyan-500 to-blue-600 text-white p-2 rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
                            >
                                {isLoading ? (
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                ) : (
                                    <Send className="w-5 h-5" />
                                )}
                            </button>
                        </div>
                    </div>
                </>
            )}
        </div>
    );
}
