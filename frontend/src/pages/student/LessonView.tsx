import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { curriculumService, progressService } from '../../services/api';
import ReactMarkdown from 'react-markdown';
import { ArrowLeft, CheckCircle, Check } from 'lucide-react';
import ChallengeSubmission from '../../components/ChallengeSubmission';
import AITutor from '../../components/AITutor';

interface ContentBlock {
    id: number;
    type: string;
    quiz_data?: string;
}

interface Lesson {
    id: number;
    module_id: number;
    title: string;
    description: string;
    content_markdown: string;
    content_blocks: ContentBlock[];
    challenge_id?: number;
}

export default function LessonView() {
    const { lessonId } = useParams();
    const navigate = useNavigate();
    const [lesson, setLesson] = useState<Lesson | null>(null);
    const [loading, setLoading] = useState(true);
    const [isCompleted, setIsCompleted] = useState(false);
    const [isCompleting, setIsCompleting] = useState(false);
    const [startTime] = useState(Date.now());

    useEffect(() => {
        if (lessonId) {
            loadLesson(parseInt(lessonId));
            loadProgress(parseInt(lessonId));
        }
    }, [lessonId]);

    const loadLesson = async (id: number) => {
        try {
            const data = await curriculumService.getLesson(id);
            setLesson(data);
            // Mark lesson as started
            await progressService.startLesson(id);
        } catch (error) {
            console.error('Failed to load lesson:', error);
        } finally {
            setLoading(false);
        }
    };

    const loadProgress = async (id: number) => {
        try {
            const progress = await progressService.getLessonProgress(id);
            setIsCompleted(progress.is_completed);
        } catch (error) {
            console.error('Failed to load progress:', error);
        }
    };

    const handleMarkComplete = async () => {
        if (!lessonId || isCompleted) return;

        setIsCompleting(true);
        try {
            const timeSpent = Math.floor((Date.now() - startTime) / 60000); // Minutes
            await progressService.completeLesson(parseInt(lessonId), timeSpent);
            setIsCompleted(true);
        } catch (error) {
            console.error('Failed to mark lesson complete:', error);
        } finally {
            setIsCompleting(false);
        }
    };

    if (loading) return (
        <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
        </div>
    );

    if (!lesson) return <div>Lesson not found</div>;

    return (
        <div className="min-h-screen bg-cyber-darker flex">
            {/* Sidebar (could be added later for navigation) */}

            {/* Main Content */}
            <div className="flex-1 flex flex-col h-screen overflow-hidden">
                {/* Top Bar */}
                <header className="bg-cyber-dark border-b border-gray-700 p-4 flex items-center justify-between">
                    <button
                        onClick={() => navigate(`/student/modules/${lesson.module_id}`)}
                        className="flex items-center text-gray-400 hover:text-white transition-colors"
                    >
                        <ArrowLeft className="w-4 h-4 mr-2" />
                        Back to Module
                    </button>
                    <h1 className="font-bold text-lg max-w-xl truncate">{lesson.title}</h1>
                    <div className="w-24"></div> {/* Spacer for center alignment */}
                </header>

                {/* Content Area */}
                <div className="flex-1 overflow-y-auto p-8 lg:p-12">
                    <div className="max-w-3xl mx-auto">
                        <div className="prose prose-invert prose-lg max-w-none">
                            <ReactMarkdown>{lesson.content_markdown || ''}</ReactMarkdown>
                        </div>

                        {/* Interactive Blocks Placeholder */}
                        {lesson.content_blocks.length > 0 && (
                            <div className="mt-12 border-t border-gray-700 pt-8">
                                <h3 className="text-xl font-bold mb-4">Interactive Content</h3>
                                <div className="space-y-4">
                                    {lesson.content_blocks.map((block: ContentBlock) => (
                                        <div key={block.id} className="card p-4 bg-gray-800 border-gray-700">
                                            <p className="text-sm text-gray-400 uppercase font-bold tracking-wider mb-2">
                                                {block.type} Block
                                            </p>
                                            <p className="text-gray-300">
                                                Interactive {block.type.toLowerCase()} content is currently under development.
                                            </p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {/* Challenge Submission or Navigation Footer */}
                        <div className="mt-16 pb-20">
                            {lesson.challenge_id && !isCompleted ? (
                                <ChallengeSubmission
                                    challengeId={lesson.challenge_id}
                                    onSuccess={async () => {
                                        await handleMarkComplete();
                                        // Optional: Add a delay before navigating or stay on page
                                        setTimeout(() => navigate(`/student/modules/${lesson.module_id}`), 2000);
                                    }}
                                />
                            ) : (
                                <div className="flex justify-end">
                                    <button
                                        onClick={async () => {
                                            await handleMarkComplete();
                                            navigate(`/student/modules/${lesson.module_id}`);
                                        }}
                                        disabled={isCompleting || isCompleted}
                                        className={`btn ${isCompleted ? 'btn-success' : 'btn-primary'} flex items-center disabled:opacity-50`}
                                    >
                                        {isCompleting ? 'Saving...' : (isCompleted ? 'Completed' : 'Mark Complete')}
                                        {isCompleted ? <Check className="ml-2 w-4 h-4" /> : <CheckCircle className="ml-2 w-4 h-4" />}
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>

            {/* AI Tutor */}
            <AITutor
                contextType="lesson"
                contextId={parseInt(lessonId || '0')}
                contextTitle={lesson.title}
            />
        </div>
    );
}
