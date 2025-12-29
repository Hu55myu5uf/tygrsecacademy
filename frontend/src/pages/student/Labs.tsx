
import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Terminal, Clock, Shield, ArrowRight, AlertTriangle } from 'lucide-react';
import { labService } from '../../services/api';

interface Lab {
    id: number;
    title: string;
    description: string;
    difficulty: string;
    category: string;
    estimated_minutes: number;
}

export default function Labs() {
    const [labs, setLabs] = useState<Lab[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchLabs = async () => {
            try {
                const data = await labService.getLabs();
                setLabs(data);
            } catch (err) {
                setError('Failed to load labs. Please try again later.');
            } finally {
                setLoading(false);
            }
        };

        fetchLabs();
    }, []);

    const getDifficultyColor = (diff: string) => {
        switch (diff.toLowerCase()) {
            case 'beginner': return 'text-green-400 bg-green-400/10';
            case 'intermediate': return 'text-yellow-400 bg-yellow-400/10';
            case 'advanced': return 'text-red-400 bg-red-400/10';
            default: return 'text-gray-400 bg-gray-400/10';
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen pt-24 pb-12 px-6 flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen pt-24 pb-12 px-6">
            <div className="container mx-auto">
                <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                    <div>
                        <h1 className="text-3xl font-bold gradient-text mb-2">Hands-on Labs</h1>
                        <p className="text-gray-400">Practice your skills in safe, isolated environments</p>
                    </div>
                </div>

                {error && (
                    <div className="mb-8 p-4 bg-red-500/10 border border-red-500/30 rounded-lg flex items-center gap-2 text-red-400">
                        <AlertTriangle className="w-5 h-5" />
                        {error}
                    </div>
                )}

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {labs.map((lab) => (
                        <div key={lab.id} className="card group hover:border-primary-500/50 transition-all duration-300">
                            <div className="p-6">
                                <div className="flex justify-between items-start mb-4">
                                    <div className={`text-xs font-bold px-2 py-1 rounded uppercase tracking-wider ${getDifficultyColor(lab.difficulty)}`}>
                                        {lab.difficulty}
                                    </div>
                                    <Shield className="w-5 h-5 text-gray-500 group-hover:text-primary-400 transition-colors" />
                                </div>

                                <h3 className="text-xl font-bold text-white mb-2 group-hover:text-primary-400 transition-colors">
                                    {lab.title}
                                </h3>
                                <p className="text-gray-400 text-sm mb-4 line-clamp-2">
                                    {lab.description}
                                </p>

                                <div className="flex items-center gap-4 text-xs text-gray-500 mb-6">
                                    <div className="flex items-center gap-1">
                                        <Clock className="w-3 h-3" />
                                        {lab.estimated_minutes} mins
                                    </div>
                                    <div className="flex items-center gap-1">
                                        <Terminal className="w-3 h-3" />
                                        {lab.category}
                                    </div>
                                </div>

                                <Link
                                    to={`/student/labs/${lab.id}`}
                                    className="btn btn-primary w-full flex items-center justify-center gap-2 group-hover:translate-x-1 transition-transform"
                                >
                                    Start Lab <ArrowRight className="w-4 h-4" />
                                </Link>
                            </div>
                        </div>
                    ))}
                </div>

                {labs.length === 0 && !error && (
                    <div className="text-center py-12 text-gray-500">
                        <Terminal className="w-16 h-16 mx-auto mb-4 opacity-20" />
                        <h3 className="text-xl font-bold mb-2">No Labs </h3>
                        <p>Check back later for new training environments.</p>
                    </div>
                )}
            </div>
        </div>
    );
}
