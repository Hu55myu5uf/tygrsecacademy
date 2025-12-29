import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Play, Square, RefreshCw, Terminal as TerminalIcon, AlertTriangle, Monitor } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { labService } from '../../services/api';
import LabTerminal from '../../components/LabTerminal';
import GuacamoleViewer from '../../components/GuacamoleViewer';
import AITutor from '../../components/AITutor';

interface LabInstance {
    instance_id: number;
    status: string;
    container_id?: string;
    lab_type?: string;
    guacamole_url?: string;
}

interface LabDetails {
    id: number;
    title: string;
    description: string;
    content: string;
    difficulty: string;
    estimated_minutes: number;
    lab_type?: string;
    guacamole_url?: string;
}

export default function LabEnvironment() {
    const { labId } = useParams();
    const [lab, setLab] = useState<LabDetails | null>(null);
    const [instance, setInstance] = useState<LabInstance | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [isTerminalActive, setIsTerminalActive] = useState(false);

    useEffect(() => {
        if (labId) {
            loadLabDetails();
        }
    }, [labId]);

    const loadLabDetails = async () => {
        try {
            const data = await labService.getLab(parseInt(labId!));
            setLab(data);
        } catch (err) {
            setError('Failed to load lab details');
        }
    };

    const handleStartLab = async () => {
        if (!labId) return;
        setLoading(true);
        setError('');
        try {
            const data = await labService.startLab(parseInt(labId));
            setInstance(data);
            setIsTerminalActive(true);
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Failed to start lab');
        } finally {
            setLoading(false);
        }
    };

    const handleStopLab = async () => {
        if (!instance) return;
        setLoading(true);
        try {
            await labService.stopLab(instance.instance_id);
            setInstance(null);
            setIsTerminalActive(false);
        } catch (err) {
            console.error('Failed to stop lab:', err);
        } finally {
            setLoading(false);
        }
    };

    if (error && !lab) return (
        <div className="p-8 text-center text-red-400">
            <AlertTriangle className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <h2 className="text-xl font-bold mb-2">Error Loading Lab</h2>
            <p>{error}</p>
        </div>
    );

    if (!lab) return <div className="p-8 text-center animate-pulse">Loading lab environment...</div>;

    return (
        <div className="h-[calc(100vh-64px)] flex flex-col md:flex-row overflow-hidden bg-cyber-darker">
            {/* Sidebar / Info Panel */}
            <div className="w-full md:w-1/3 lg:w-1/4 bg-gray-900 border-r border-gray-800 p-6 overflow-y-auto">
                <div className="mb-8">
                    <span className="text-xs font-bold text-primary-400 bg-primary-500/10 px-2 py-1 rounded uppercase tracking-wider">
                        {lab.difficulty}
                    </span>
                    <h1 className="text-2xl font-bold mt-4 mb-2">{lab.title}</h1>
                    <p className="text-gray-400 text-sm mb-4">{lab.description}</p>
                    <div className="text-xs text-gray-500">
                        ⏱️ {lab.estimated_minutes} minutes
                    </div>
                </div>

                {/* Controls */}
                <div className="card p-4 mb-8 bg-gray-800/50">
                    <div className="flex items-center justify-between mb-4">
                        <span className="text-sm font-bold text-gray-300">Lab Control</span>
                        {instance && (
                            <span className="flex items-center text-xs text-green-400">
                                <span className="w-2 h-2 rounded-full bg-green-400 mr-2 animate-pulse"></span>
                                Running
                            </span>
                        )}
                    </div>

                    {!instance ? (
                        <button
                            onClick={handleStartLab}
                            disabled={loading}
                            className="btn btn-primary w-full flex items-center justify-center gap-2"
                        >
                            {loading ? <RefreshCw className="animate-spin w-4 h-4" /> : <Play className="w-4 h-4" />}
                            Start Lab Instance
                        </button>
                    ) : (
                        <button
                            onClick={handleStopLab}
                            disabled={loading}
                            className="btn btn-danger w-full flex items-center justify-center gap-2"
                        >
                            <Square className="w-4 h-4" />
                            Terminate Lab
                        </button>
                    )}

                    {error && (
                        <div className="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded text-xs text-red-300 flex items-start gap-2">
                            <AlertTriangle className="w-4 h-4 shrink-0" />
                            {error}
                        </div>
                    )}
                </div>

                {/* Lab Guide */}
                <div className="prose prose-invert prose-sm max-w-none">
                    <ReactMarkdown>{lab.content || ''}</ReactMarkdown>
                </div>
            </div>

            {/* Terminal/Desktop Area */}
            <div className="flex-1 bg-black p-4 relative">
                {isTerminalActive && instance ? (
                    // Render based on lab type
                    instance.lab_type === 'guacamole' ? (
                        <GuacamoleViewer
                            guacamoleUrl={instance.guacamole_url || 'http://localhost:8085/guacamole'}
                            instanceId={instance.instance_id}
                        />
                    ) : (
                        <LabTerminal instanceId={instance.instance_id} />
                    )
                ) : (
                    <div className="h-full flex flex-col items-center justify-center text-gray-500">
                        {lab.lab_type === 'guacamole' ? (
                            <Monitor className="w-16 h-16 mb-4 opacity-20" />
                        ) : (
                            <TerminalIcon className="w-16 h-16 mb-4 opacity-20" />
                        )}
                        <h2 className="text-xl font-bold mb-2">
                            {lab.lab_type === 'guacamole' ? 'Desktop Offline' : 'Terminal Offline'}
                        </h2>
                        <p className="max-w-md text-center">
                            {lab.lab_type === 'guacamole'
                                ? 'Start the lab to access a full Kali Linux desktop with DVWA target.'
                                : 'Start the lab instance to access the secure terminal environment.'
                            }
                        </p>
                    </div>
                )}
            </div>

            {/* AI Tutor */}
            <AITutor
                contextType="lab"
                contextId={lab.id}
                contextTitle={lab.title}
                contextDescription={lab.content}
            />
        </div>
    );
}
