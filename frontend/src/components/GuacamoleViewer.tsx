import { useEffect, useState } from 'react';
import { RefreshCw, ExternalLink, Maximize2 } from 'lucide-react';

interface GuacamoleViewerProps {
    guacamoleUrl: string;
    instanceId: number;
    onClose?: () => void;
}

export default function GuacamoleViewer({ guacamoleUrl, instanceId, onClose }: GuacamoleViewerProps) {
    const [isLoading, setIsLoading] = useState(true);
    const [isFullscreen, setIsFullscreen] = useState(false);

    // Default Guacamole login credentials (configured in user-mapping.xml)
    const guacUser = 'tygr';
    const guacPass = 'tygrsec123';

    // Build the auto-login URL
    const getGuacamoleAutoLoginUrl = () => {
        // Guacamole authentication endpoint
        const baseUrl = guacamoleUrl || 'http://localhost:8085/guacamole';
        // Return the main client URL - user will need to login manually for now
        return `${baseUrl}/#/client/S2FsaSBBdHRhY2sgTWFjaGluZQBjAG15c3Fs`;
    };

    const handleIframeLoad = () => {
        setIsLoading(false);
    };

    const toggleFullscreen = () => {
        setIsFullscreen(!isFullscreen);
    };

    const openInNewTab = () => {
        window.open(guacamoleUrl || 'http://localhost:8085/guacamole', '_blank');
    };

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
