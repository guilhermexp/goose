import React, { useEffect, useState, useRef, useCallback } from 'react';
import './AndroidPreview.css';

interface AndroidPreviewProps {
  deviceId?: string;
  serverUrl?: string;
  width?: number;
  onDeviceClick?: (x: number, y: number) => void;
}

interface DeviceInfo {
  id: string;
  model: string;
}

export const AndroidPreview: React.FC<AndroidPreviewProps> = ({
  deviceId = 'emulator-5554',
  serverUrl = 'ws://localhost:8765',
  width = 300,
  onDeviceClick,
}) => {
  const [screenshot, setScreenshot] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [devices, setDevices] = useState<DeviceInfo[]>([]);
  const [selectedDevice, setSelectedDevice] = useState(deviceId);
  const wsRef = useRef<WebSocket | null>(null);
  const imgRef = useRef<HTMLImageElement>(null);

  // Buscar lista de dispositivos
  const fetchDevices = useCallback(async () => {
    try {
      const response = await fetch(`http://localhost:8765/devices`);
      const data = await response.json();
      setDevices(data.devices || []);
      if (data.devices?.length > 0 && !selectedDevice) {
        setSelectedDevice(data.devices[0].id);
      }
    } catch (e) {
      console.error('Erro ao buscar devices:', e);
    }
  }, [selectedDevice]);

  // Conectar WebSocket
  useEffect(() => {
    fetchDevices();

    if (!selectedDevice) return;

    const ws = new WebSocket(`${serverUrl}/ws/${selectedDevice}`);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket conectado');
      setIsConnected(true);
      setError(null);
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'frame' && data.image) {
          setScreenshot(`data:image/png;base64,${data.image}`);
        }
      } catch (e) {
        console.error('Erro ao processar mensagem:', e);
      }
    };

    ws.onerror = (e) => {
      console.error('WebSocket erro:', e);
      setError('Erro de conexão');
      setIsConnected(false);
    };

    ws.onclose = () => {
      console.log('WebSocket desconectado');
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [selectedDevice, serverUrl, fetchDevices]);

  // Handler de clique na tela
  const handleScreenClick = (e: React.MouseEvent<HTMLImageElement>) => {
    if (!imgRef.current || !wsRef.current) return;

    const rect = imgRef.current.getBoundingClientRect();
    const scaleX = 1080 / rect.width; // Resolução do emulador
    const scaleY = 2400 / rect.height;

    const x = Math.round((e.clientX - rect.left) * scaleX);
    const y = Math.round((e.clientY - rect.top) * scaleY);

    // Envia comando de clique
    wsRef.current.send(JSON.stringify({
      command: 'click',
      x,
      y
    }));

    onDeviceClick?.(x, y);
  };

  // Enviar tecla
  const sendKey = (key: string) => {
    if (!wsRef.current) return;
    wsRef.current.send(JSON.stringify({
      command: 'key',
      key
    }));
  };

  if (error && !isConnected) {
    return (
      <div className="android-preview android-preview-error">
        <div className="android-preview-header">
          <span className="status-dot disconnected" />
          <span>Android Preview</span>
        </div>
        <div className="android-preview-content">
          <p className="error-message">{error}</p>
          <p className="error-hint">
            Inicie o servidor de preview:
            <code>cd android/preview && uv run server.py</code>
          </p>
          <button
            className="retry-button"
            onClick={() => window.location.reload()}
          >
            Tentar novamente
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="android-preview">
      <div className="android-preview-header">
        <span className={`status-dot ${isConnected ? 'connected' : 'connecting'}`} />
        <select
          value={selectedDevice}
          onChange={(e) => setSelectedDevice(e.target.value)}
          className="device-select"
        >
          {devices.map((d) => (
            <option key={d.id} value={d.id}>
              {d.model} ({d.id})
            </option>
          ))}
          {devices.length === 0 && (
            <option value="">Nenhum dispositivo</option>
          )}
        </select>
      </div>

      <div className="android-preview-screen">
        {screenshot ? (
          <img
            ref={imgRef}
            src={screenshot}
            alt="Android Screen"
            width={width}
            onClick={handleScreenClick}
            className="android-screen-img"
          />
        ) : (
          <div className="android-screen-loading" style={{ width }}>
            <div className="loading-spinner" />
            <p>Conectando...</p>
          </div>
        )}
      </div>

      <div className="android-preview-controls">
        <button
          className="control-btn"
          onClick={() => sendKey('back')}
          title="Voltar"
        >
          ◀
        </button>
        <button
          className="control-btn"
          onClick={() => sendKey('home')}
          title="Home"
        >
          ○
        </button>
        <button
          className="control-btn"
          onClick={() => sendKey('recent')}
          title="Recentes"
        >
          □
        </button>
      </div>

      <div className="android-preview-footer">
        <span className="fps-indicator">
          {isConnected ? '~10 FPS' : 'Offline'}
        </span>
      </div>
    </div>
  );
};

export default AndroidPreview;
