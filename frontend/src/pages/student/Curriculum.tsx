import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { curriculumService, progressService } from '../../services/api';
import { Book, ChevronRight, Lock, ArrowLeft, CheckCircle } from 'lucide-react';
import StudentProfileHeader from '../../components/StudentProfileHeader';

interface Module {
    id: number;
    title: string;
    description: string;
    is_published: boolean;
    // Progress fields (optional as they come from separate API)
    progress?: {
        completion_percentage: number;
        is_completed: boolean;
    };
}

interface Tier {
    id: number;
    tier_number: number;
    name: string;
    description: string;
    modules: Module[];
    is_unlocked?: boolean;
    completion_percentage?: number;
}

export default function Curriculum() {
    const [tiers, setTiers] = useState<Tier[]>([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            // Parallel fetch for speed
            const [tiersData, progressData] = await Promise.all([
                curriculumService.getTiers(),
                progressService.getMyProgress()
            ]);

            // Merge progress into tiers
            const mergedTiers = tiersData.map((tier: Tier) => {
                // Find tier unlock status
                const tierProgress = progressData.overall.current_tier >= tier.tier_number;

                // Merge module progress
                const enrichedModules = tier.modules.map((mod: Module) => {
                    const modProgress = progressData.modules.find((m: any) => m.module_id === mod.id);
                    return {
                        ...mod,
                        progress: modProgress ? {
                            completion_percentage: modProgress.completion_percent,
                            is_completed: modProgress.is_completed
                        } : { completion_percentage: 0, is_completed: false }
                    };
                });

                return {
                    ...tier,
                    modules: enrichedModules,
                    is_unlocked: tierProgress
                };
            });

            setTiers(mergedTiers);
        } catch (error) {
            console.error('Failed to load curriculum data:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-cyber-darker text-white p-8">
            <div className="max-w-4xl mx-auto">
                <header className="mb-12">
                    <button
                        onClick={() => navigate('/student/dashboard')}
                        className="btn btn-secondary mb-4 flex items-center gap-2"
                    >
                        <ArrowLeft className="w-4 h-4" />
                    </button>
                    <StudentProfileHeader />
                    <h1 className="text-4xl font-bold gradient-text mb-4">Curriculum</h1>
                    <p className="text-gray-400 text-lg">
                        Master cybersecurity from fundamentals to advanced exploitation.
                    </p>
                </header>

                <div className="space-y-8">
                    {tiers.map((tier: Tier) => (
                        <div key={tier.id} className={`card p-6 border-l-4 ${tier.is_unlocked !== false ? 'border-primary-500' : 'border-gray-600 opacity-75'}`}>
                            <div className="flex items-center justify-between mb-6">
                                <div>
                                    <span className="text-sm font-bold text-primary-400 uppercase tracking-wider">
                                        Tier {tier.tier_number}
                                    </span>
                                    <h2 className="text-2xl font-bold mt-1 flex items-center gap-3">
                                        {tier.name}
                                        {tier.is_unlocked === false && <Lock className="w-5 h-5 text-gray-500" />}
                                    </h2>
                                    <p className="text-gray-400 mt-2">{tier.description}</p>
                                </div>
                            </div>

                            <div className="grid gap-4">
                                {tier.modules.map((module) => {
                                    const isLocked = !module.is_published || tier.is_unlocked === false;

                                    return (
                                        <div
                                            key={module.id}
                                            onClick={() => !isLocked && navigate(`/student/modules/${module.id}`)}
                                            className={`
                                                group p-4 rounded-lg border bg-gray-800/50 
                                                transition-all duration-300 relative overflow-hidden
                                                ${!isLocked
                                                    ? 'border-gray-700 hover:border-primary-500/50 hover:bg-gray-800 cursor-pointer'
                                                    : 'border-gray-800 opacity-50 cursor-not-allowed'}
                                            `}
                                        >
                                            {/* Progress Bar Background */}
                                            {!isLocked && module.progress && module.progress.completion_percentage > 0 && (
                                                <div
                                                    className="absolute bottom-0 left-0 h-1 bg-primary-500 transition-all duration-1000"
                                                    style={{ width: `${module.progress.completion_percentage}%` }}
                                                />
                                            )}

                                            <div className="flex items-center justify-between">
                                                <div className="flex items-center gap-4">
                                                    <div className={`
                                                        w-10 h-10 rounded-full flex items-center justify-center relative
                                                        ${module.progress?.is_completed ? 'bg-green-500/20 text-green-400' :
                                                            !isLocked ? 'bg-primary-500/20 text-primary-400' : 'bg-gray-700 text-gray-500'}
                                                    `}>
                                                        {module.progress?.is_completed ? <CheckCircle className="w-5 h-5" /> : <Book className="w-5 h-5" />}
                                                    </div>
                                                    <div>
                                                        <h3 className={`font-bold ${!isLocked ? 'group-hover:text-primary-400' : ''} transition-colors`}>
                                                            {module.title}
                                                        </h3>
                                                        <div className="flex items-center gap-3">
                                                            <p className="text-sm text-gray-400">{module.description}</p>
                                                            {!isLocked && module.progress && module.progress.completion_percentage > 0 && (
                                                                <span className="text-xs text-primary-400 font-bold">
                                                                    {Math.round(module.progress.completion_percentage)}%
                                                                </span>
                                                            )}
                                                        </div>
                                                    </div>
                                                </div>

                                                <div className="text-gray-500">
                                                    {!isLocked ? (
                                                        <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                                                    ) : (
                                                        <Lock className="w-4 h-4" />
                                                    )}
                                                </div>
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}
