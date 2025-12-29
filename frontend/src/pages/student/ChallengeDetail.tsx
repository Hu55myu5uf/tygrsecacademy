import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Flag, FileText, Lightbulb, CheckCircle, XCircle, ArrowLeft } from 'lucide-react';
import { challengeService } from '../../services/api';
import ReactMarkdown from 'react-markdown';
import AITutor from '../../components/AITutor';

interface ChallengeDetail {
    id: number;
    title: string;
    description: string;
    instructions: string;
    category: string;
    difficulty: string;
    base_points: number;
    files_url?: string;
    flag_format?: string;
    solved: boolean;
    ai_assistance_enabled: boolean;
}

export default function ChallengeDetail() {
    const { challengeId } = useParams();
    const navigate = useNavigate();
    const [challenge, setChallenge] = useState<ChallengeDetail | null>(null);
    const [flag, setFlag] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [result, setResult] = useState<{ correct: boolean; message: string; points: number } | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (challengeId) {
            loadChallenge(parseInt(challengeId));
        }
    }, [challengeId]);

    const loadChallenge = async (id: number) => {
        try {
            const data = await challengeService.getChallenge(id);
            setChallenge(data);
        } catch (error) {
            console.error('Failed to load challenge:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!challengeId) return;

        setSubmitting(true);
        setResult(null);

        try {
            const response = await challengeService.submitFlag(parseInt(challengeId), flag);
            setResult(response);
            if (response.correct) {
                setFlag('');
                // Reload challenge to update solved status
                loadChallenge(parseInt(challengeId));
            }
        } catch (error: any) {
            setResult({
                correct: false,
                message: error.response?.data?.detail || 'Submission failed',
                points: 0
            });
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) {
        return <div className="flex items-center justify-center h-96">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
        </div>;
    }

    if (!challenge) {
        return <div className="container mx-auto px-6 py-12 text-center">
            <h2 className="text-2xl font-bold mb-4">Challenge not found</h2>
            <button onClick={() => navigate('/student/challenges')} className="btn btn-primary">
                Back to Challenges
            </button>
        </div>;
    }

    return (
        <div className="container mx-auto px-6 py-12 max-w-4xl">
            {/* Back button */}
            <button
                onClick={() => navigate('/student/challenges')}
                className="btn btn-secondary mb-6 flex items-center gap-2"
            >
                <ArrowLeft className="w-4 h-4" />
                Back to Challenges
            </button>

            {/* Challenge Header */}
            <div className="card p-8 mb-6">
                <div className="flex items-start justify-between mb-4">
                    <div>
                        <h1 className="text-3xl font-bold mb-3">{challenge.title}</h1>
                        <div className="flex items-center gap-3">
                            <span className="badge badge-primary">{challenge.difficulty}</span>
                            <span className="text-gray-400 uppercase text-sm">{challenge.category.replace('_', ' ')}</span>
                            <span className="text-primary-400 font-bold">{challenge.base_points} points</span>
                        </div>
                    </div>
                    {challenge.solved && (
                        <div className="bg-green-500/10 px-4 py-2 rounded-lg flex items-center gap-2">
                            <CheckCircle className="w-5 h-5 text-green-400" />
                            <span className="text-green-400 font-bold">Solved</span>
                        </div>
                    )}
                </div>

                <p className="text-gray-300 text-lg">{challenge.description}</p>
            </div>

            {/* Instructions */}
            <div className="card p-8 mb-6">
                <div className="flex items-center gap-2 mb-4">
                    <FileText className="w-5 h-5 text-primary-400" />
                    <h2 className="text-xl font-bold">Instructions</h2>
                </div>
                <div className="prose prose-invert max-w-none">
                    <ReactMarkdown>{challenge.instructions || 'No additional instructions provided.'}</ReactMarkdown>
                </div>

                {challenge.files_url && (
                    <div className="mt-6">
                        <a
                            href={challenge.files_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="btn btn-outline"
                        >
                            Download Challenge Files
                        </a>
                    </div>
                )}
            </div>

            {/* Flag Submission */}
            {!challenge.solved && (
                <div className="card p-8 mb-6">
                    <div className="flex items-center gap-2 mb-4">
                        <Flag className="w-5 h-5 text-primary-400" />
                        <h2 className="text-xl font-bold">Submit Flag</h2>
                    </div>

                    {challenge.flag_format && (
                        <p className="text-sm text-gray-400 mb-4">
                            Flag format: <code className="bg-gray-800 px-2 py-1 rounded">{challenge.flag_format}</code>
                        </p>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <input
                            type="text"
                            value={flag}
                            onChange={(e) => setFlag(e.target.value)}
                            placeholder="Enter your flag here..."
                            className="input w-full font-mono"
                            required
                        />
                        <button
                            type="submit"
                            disabled={submitting}
                            className="btn btn-primary"
                        >
                            {submitting ? 'Submitting...' : 'Submit Flag'}
                        </button>
                    </form>

                    {result && (
                        <div className={`mt-4 p-4 rounded-lg border flex items-start gap-3 ${result.correct
                            ? 'bg-green-500/10 border-green-500/30'
                            : 'bg-red-500/10 border-red-500/30'
                            }`}>
                            {result.correct ? (
                                <CheckCircle className="w-5 h-5 text-green-400 shrink-0 mt-0.5" />
                            ) : (
                                <XCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
                            )}
                            <div>
                                <p className={result.correct ? 'text-green-300' : 'text-red-300'}>
                                    {result.message}
                                </p>
                                {result.correct && result.points > 0 && (
                                    <p className="text-green-400 font-bold mt-1">+{result.points} points!</p>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* AI Tutor - for all challenges, especially those with AI assistance */}
            <AITutor
                contextType="challenge"
                contextId={parseInt(challengeId || '0')}
                contextTitle={challenge.title}
            />
        </div>
    );
}
