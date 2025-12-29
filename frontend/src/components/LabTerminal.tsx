
import { useEffect, useRef } from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';
import 'xterm/css/xterm.css';

interface LabTerminalProps {
    instanceId: number;
    onClose?: () => void;
}

export default function LabTerminal({ instanceId, onClose }: LabTerminalProps) {
    const terminalRef = useRef<HTMLDivElement>(null);
    const wsRef = useRef<WebSocket | null>(null);
    const xtermRef = useRef<Terminal | null>(null);

    useEffect(() => {
        if (!terminalRef.current) return;

        // Initialize xterm
        const term = new Terminal({
            cursorBlink: true,
            theme: {
                background: '#0a0a0a',
                foreground: '#f0f0f0',
                cursor: '#00ff00',
            },
            fontFamily: 'Menlo, Monaco, "Courier New", monospace',
            fontSize: 14,
        });

        const fitAddon = new FitAddon();
        term.loadAddon(fitAddon);
        term.open(terminalRef.current);
        fitAddon.fit();
        xtermRef.current = term;

        // Connect to WebSocket
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.hostname}:8000/api/labs/ws/${instanceId}`;
        const ws = new WebSocket(wsUrl);
        wsRef.current = ws;

        ws.onopen = () => {
            term.writeln('\r\n\x1b[32m[+] Connected to TygrSec Lab Environment\x1b[0m\r\n');
            term.writeln('\x1b[90mPreparing your shell...\x1b[0m\r\n');
        };

        ws.onmessage = (event) => {
            term.write(event.data);
        };

        ws.onclose = (event) => {
            term.writeln(`\r\n\x1b[31m[-] Disconnected (Code: ${event.code})\x1b[0m`);
            if (onClose) onClose();
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            term.writeln('\r\n\x1b[31m[!] Connection Error\x1b[0m');
        };

        // Handle terminal input
        term.onData((data) => {
            if (ws.readyState === WebSocket.OPEN) {
                ws.send(data);
            }
        });

        // Handle resize
        const handleResize = () => fitAddon.fit();
        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
            if (ws.readyState === WebSocket.OPEN) {
                ws.close();
            }
            term.dispose();
        };
    }, [instanceId]);

    return (
        <div className="h-full w-full bg-black rounded-lg overflow-hidden border border-gray-800 shadow-2xl">
            <div className="bg-gray-900 px-4 py-2 flex items-center justify-between border-b border-gray-800">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                    <span className="ml-2 text-xs text-gray-400 font-mono">root@tygrsec-lab:~</span>
                </div>
                <div className="text-xs text-gray-500">
                    <span className="w-2 h-2 rounded-full bg-green-500 inline-block mr-1 animate-pulse"></span>
                    Live
                </div>
            </div>
            <div ref={terminalRef} className="h-[calc(100%-40px)] w-full p-1" />
        </div>
    );
}
