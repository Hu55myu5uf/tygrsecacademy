import { useEffect, useState } from 'react';
import { RefreshCw, ExternalLink, Maximize2, Globe, AlertTriangle } from 'lucide-react';

interface GuacamoleViewerProps {
    guacamoleUrl: string;
    instanceId: number;
    onClose?: () => void;
}

export default function GuacamoleViewer({ guacamoleUrl, instanceId, onClose }: GuacamoleViewerProps) {
    const [isLoading, setIsLoading] = useState(true);
    const [isFullscreen, setIsFullscreen] = useState(false);
    const [iframeError, setIframeError] = useState(false);

    // Detect if this is a direct browser lab (not Guacamole VNC)
    const isDirectBrowserLab = guacamoleUrl && !guacamoleUrl.includes('guacamole');

    // Default Guacamole login credentials (configured in user-mapping.xml)
    const guacUser = 'tygr';
    const guacPass = 'tygrsec123';

    const handleIframeLoad = () => {
        setIsLoading(false);
    };

    const handleIframeError = () => {
        setIframeError(true);
        setIsLoading(false);
    };

    const toggleFullscreen = () => {
        setIsFullscreen(!isFullscreen);
    };

    const openInNewTab = () => {
        window.open(guacamoleUrl || 'http://localhost:8085/guacamole', '_blank');
    };

    // For direct browser labs that block iframes, show open in new tab interface
    if (isDirectBrowserLab) {
        return (
            <div className={`h-full w-full bg-gradient-to-br from-gray-900 to-gray-800 rounded-lg overflow-hidden border border-gray-700 shadow-2xl flex flex-col items-center justify-center`}>
                <div className="text-center max-w-md p-8">
                    <div className="w-20 h-20 rounded-full bg-primary-500/20 flex items-center justify-center mx-auto mb-6">
                        <Globe className="w-10 h-10 text-primary-400" />
                    </div>
                    <h2 className="text-2xl font-bold text-white mb-4">Browser-Based Lab Ready</h2>
                    <p className="text-gray-300 mb-6">
                        This lab runs directly in your browser. Click the button below to open it in a new tab for the best experience.
                    </p>
                    <button
                        onClick={openInNewTab}
                        className="bg-primary-600 hover:bg-primary-700 text-white font-bold py-3 px-6 rounded-lg flex items-center gap-2 mx-auto transition-all transform hover:scale-105 shadow-lg"
                    >
                        <ExternalLink className="w-5 h-5" />
                        Open Lab in New Tab
                    </button>
                    <div className="mt-6 text-gray-400 text-sm">
                        <p>Lab URL: <code className="bg-gray-700 px-2 py-1 rounded text-primary-300">{guacamoleUrl}</code></p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className={`h-full w-full bg-black rounded-lg overflow-hidden border border-gray-800 shadow-2xl ${isFullscreen ? 'fixed inset-0 z-50' : ''}`}>
            {/* Header Bar */}
            <div className="bg-gray-900 px-4 py-2 flex items-center justify-between border-b border-gray-800">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                    <span className="ml-2 text-xs text-gray-400 font-mono">Kali Linux Desktop - VNC</span>
                </div>
                <div className="flex items-center gap-2">
                    <button
                        onClick={toggleFullscreen}
                        className="p-1 hover:bg-gray-700 rounded text-gray-400 hover:text-white transition-colors"
                        title={isFullscreen ? "Exit Fullscreen" : "Fullscreen"}
                    >
                        <Maximize2 className="w-4 h-4" />
                    </button>
                    <button
                        onClick={openInNewTab}
                        className="p-1 hover:bg-gray-700 rounded text-gray-400 hover:text-white transition-colors"
                        title="Open in New Tab"
                    >
                        <ExternalLink className="w-4 h-4" />
                    </button>
                    <span className="text-xs text-gray-500">
                        <span className="w-2 h-2 rounded-full bg-green-500 inline-block mr-1 animate-pulse"></span>
                        Connected
                    </span>
                </div>
            </div>

            {/* Loading Overlay */}
            {isLoading && (
                <div className="absolute inset-0 bg-black/80 flex items-center justify-center z-10">
                    <div className="text-center">
                        <RefreshCw className="w-8 h-8 text-primary-400 animate-spin mx-auto mb-4" />
                        <p className="text-gray-300">Connecting to remote desktop...</p>
                        <p className="text-xs text-gray-500 mt-2">This may take a moment</p>
                    </div>
                </div>
            )}

            {/* Guacamole iframe */}
            <iframe
                src={guacamoleUrl || 'http://localhost:8085/guacamole'}
                className="w-full h-[calc(100%-40px)] border-0"
                onLoad={handleIframeLoad}
                onError={handleIframeError}
                allow="clipboard-read; clipboard-write"
                title="Remote Desktop"
            />

            {/* Login Instructions Overlay (shows briefly) */}
            <div className="absolute bottom-4 right-4 bg-gray-800/90 rounded-lg p-3 text-xs text-gray-300 max-w-xs">
                <p className="font-bold text-primary-400 mb-1">Login Credentials:</p>
                <p>Username: <code className="bg-gray-700 px-1 rounded">tygr</code></p>
                <p>Password: <code className="bg-gray-700 px-1 rounded">tygrsec123</code></p>
            </div>
        </div>
    );
}
