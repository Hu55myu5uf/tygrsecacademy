import { useState, useEffect } from 'react';
import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { curriculumService, progressService } from '../../services/api';
import { PlayCircle, Lock, ArrowLeft, Clock, CheckCircle } from 'lucide-react';

interface ContentBlock {
    id: number;
    type: string;
}

interface Lesson {
    id: number;
    title: string;
    description: string;
    duration_minutes: number;
    is_published: boolean;
    content_blocks: ContentBlock[];
    // Enriched field
    is_completed?: boolean;
}

interface Module {
    id: number;
    title: string;
    description: string;
    estimated_hours: number;
    lessons: Lesson[];
}

export default function ModuleDetail() {
    const { moduleId } = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    const [module, setModule] = useState<Module | null>(null);
    const [progress, setProgress] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    // Check if we came from a tier page
    const fromTier = (location.state as any)?.fromTier;

    useEffect(() => {
        if (moduleId) {
            loadData(parseInt(moduleId));
        }
    }, [moduleId]);

    const loadData = async (id: number) => {
        try {
            const [moduleData, progressData] = await Promise.all([
                curriculumService.getModule(id),
                progressService.getModuleProgress(id).catch(() => null) // Handle 404 if no progress yet
            ]);

            // Merge progress
            if (progressData && progressData.lessons) {
                moduleData.lessons = moduleData.lessons.map((lesson: Lesson) => {
                    const lessonProg = progressData.lessons.find((l: any) => l.lesson_id === lesson.id);
                    return {
                        ...lesson,
                        is_completed: lessonProg?.is_completed || false
                    };
                });
            }

            setModule(moduleData);
            setProgress(progressData);
        } catch (error) {
            console.error('Failed to load module:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleBack = () => {
        if (fromTier !== undefined) {
            navigate(`/student/tiers/${fromTier}`);
        } else {
            navigate('/student/curriculum');
        }
    };

    if (loading) return (
        <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
        </div>
    );

    if (!module) return <div>Module not found</div>;

    const completionPercent = progress?.completion_percentage || 0;

    return (
        <div className="min-h-screen bg-cyber-darker text-white p-8">
            <div className="max-w-4xl mx-auto">
                <button
                    onClick={handleBack}
                    className="flex items-center text-gray-400 hover:text-white mb-8 transition-colors"
                >
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    {fromTier !== undefined ? `Back to Tier ${fromTier}` : 'Back to Curriculum'}
                </button>

                <header className="mb-12">
                    <div className="flex items-center gap-4 text-sm text-primary-400 font-bold uppercase tracking-wider mb-2">
                        <span>Module</span>
                        <span>•</span>
                        <div className="flex items-center">
                            <Clock className="w-4 h-4 mr-1" />
                            {module.estimated_hours} Hours
                        </div>
                    </div>
                    <h1 className="text-4xl font-bold mb-4">{module.title}</h1>
                    <p className="text-xl text-gray-400">{module.description}</p>

                    {/* Progress Bar */}
                    <div className="mt-6 flex items-center gap-4">
                        <div className="flex-1 bg-gray-800 rounded-full h-3 overflow-hidden">
                            <div
                                className="bg-primary-500 h-full transition-all duration-1000"
                                style={{ width: `${completionPercent}%` }}
                            />
                        </div>
                        <span className="text-primary-400 font-bold">{Math.round(completionPercent)}% Complete</span>
                    </div>
                </header>

                <div className="bg-gray-800/30 rounded-xl border border-gray-700 overflow-hidden">
                    <div className="p-6 border-b border-gray-700">
                        <h2 className="text-xl font-bold">Course Content</h2>
                        <p className="text-gray-400 text-sm mt-1">{module.lessons.length} Lessons</p>
                    </div>

                    <div className="divide-y divide-gray-700">
                        {module.lessons.map((lesson: Lesson, index: number) => (
                            <div
                                key={lesson.id}
                                onClick={() => lesson.is_published && navigate(`/student/lessons/${lesson.id}`)}
                                className={`
                                    group p-6 flex items-center justify-between transition-colors
                                    ${lesson.is_published
                                        ? 'hover:bg-gray-700/50 cursor-pointer'
                                        : 'opacity-50 cursor-not-allowed bg-gray-900/50'}
                                `}
                            >
                                <div className="flex items-center gap-4">
                                    <div className={`
                                        flex-shrink-0 w-8 h-8 rounded-full border flex items-center justify-center text-sm font-bold
                                        ${lesson.is_completed
                                            ? 'bg-green-500/20 border-green-500/50 text-green-400'
                                            : 'bg-gray-800 border-gray-600 text-gray-400'}
                                    `}>
                                        {lesson.is_completed ? <CheckCircle className="w-5 h-5" /> : index + 1}
                                    </div>
                                    <div>
                                        <h3 className={`font-medium text-lg ${lesson.is_published ? 'group-hover:text-primary-400' : ''}`}>
                                            {lesson.title}
                                        </h3>
                                        <div className="flex items-center gap-4 mt-1 text-sm text-gray-500">
                                            <span>{lesson.duration_minutes} min read</span>
                                            {lesson.is_completed && <span className="text-green-500 text-xs">Completed</span>}
                                        </div>
                                    </div>
                                </div>

                                <div>
                                    {lesson.is_published ? (
                                        lesson.is_completed ? (
                                            <div className="px-3 py-1 bg-green-500/10 text-green-400 rounded-full text-xs font-bold border border-green-500/20">
                                                Review
                                            </div>
                                        ) : (
                                            <PlayCircle className="w-6 h-6 text-primary-500 opacity-0 group-hover:opacity-100 transition-opacity" />
                                        )
                                    ) : (
                                        <Lock className="w-5 h-5 text-gray-600" />
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
