/**
 * Window Docking Module
 * Permite "grampear" a janela do emulador Android à janela do Goose,
 * fazendo com que se movam juntas.
 */

import { BrowserWindow } from 'electron';
import log from './logger';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
let windowManager: any = null;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
let dockedWindow: any = null;
let isDockingEnabled = false;
let lastBounds: { x: number; y: number; width: number; height: number } | null = null;

// Gap entre as janelas (pixels)
const DOCK_GAP = 0;

/**
 * Inicializa o módulo de docking
 */
export async function initWindowDocking(): Promise<boolean> {
  try {
    // Dynamic import porque é um módulo nativo
    const nwm = await import('@johnlindquist/node-window-manager');
    windowManager = nwm.windowManager;
    log.info('[WindowDocking] Module initialized successfully');
    return true;
  } catch (error) {
    log.error('[WindowDocking] Failed to initialize:', error);
    return false;
  }
}

/**
 * Encontra a janela do emulador Android
 * NOTA: O Android Emulator no macOS cria duas janelas:
 * - "Android Emulator - Pixel_7_API_34:5554" (tela principal do celular)
 * - "qemu-system-aarch64" (painel de controles lateral)
 * Queremos a janela principal, não o painel de controles.
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function findEmulatorWindow(): any | null {
  if (!windowManager) {
    log.warn('[WindowDocking] Window manager not initialized');
    return null;
  }

  try {
    const windows = windowManager.getWindows();

    // Debug: lista todas as janelas disponíveis
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const allTitles = windows.map((w: any) => w.getTitle?.() || w.title || 'Unknown');
    log.info(`[WindowDocking] Available windows (${allTitles.length}): ${JSON.stringify(allTitles)}`);

    // Procura janelas qemu-system (emulador Android no macOS)
    // Como há múltiplas janelas qemu, pegamos a MAIOR (tela do celular)
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const qemuWindows = windows.filter((w: any) => {
      const title = (w.getTitle?.() || w.title || '').toLowerCase();
      return title.includes('qemu-system');
    });

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    let emulatorWindow: any = null;

    if (qemuWindows.length > 0) {
      // Ordena por área (width * height) e pega a maior
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      emulatorWindow = qemuWindows.reduce((largest: any, current: any) => {
        try {
          const largestBounds = largest.getBounds?.() || { width: 0, height: 0 };
          const currentBounds = current.getBounds?.() || { width: 0, height: 0 };
          const largestArea = largestBounds.width * largestBounds.height;
          const currentArea = currentBounds.width * currentBounds.height;
          return currentArea > largestArea ? current : largest;
        } catch {
          return largest;
        }
      });
    }

    // Se não encontrar qemu, tenta outras variações
    if (!emulatorWindow) {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      emulatorWindow = windows.find((w: any) => {
        const title = (w.getTitle?.() || w.title || '').toLowerCase();
        return (
          title.includes('android emulator') ||
          title.includes('emulator-') ||
          title.includes('pixel')
        );
      });
    }

    if (emulatorWindow) {
      const title = emulatorWindow.getTitle?.() || emulatorWindow.title || 'Unknown';
      log.info(`[WindowDocking] Found emulator window: "${title}"`);
      return emulatorWindow;
    }

    log.warn('[WindowDocking] Emulator window not found');
    return null;
  } catch (error) {
    log.error('[WindowDocking] Error finding emulator window:', error);
    return null;
  }
}

/**
 * Lista todas as janelas disponíveis (para debug)
 */
export function listAllWindows(): string[] {
  if (!windowManager) return [];

  try {
    const windows = windowManager.getWindows();
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return windows.map((w: any) => {
      const title = w.getTitle?.() || w.title || 'Unknown';
      return `${w.id}: ${title}`;
    });
  } catch (error) {
    log.error('[WindowDocking] Error listing windows:', error);
    return [];
  }
}

/**
 * Ativa o docking da janela do emulador com o Goose
 */
export function enableDocking(mainWindow: BrowserWindow): boolean {
  if (!windowManager) {
    log.error('[WindowDocking] Cannot enable docking - window manager not initialized');
    return false;
  }

  dockedWindow = findEmulatorWindow();
  if (!dockedWindow) {
    log.warn('[WindowDocking] Cannot enable docking - emulator window not found');
    return false;
  }

  isDockingEnabled = true;
  lastBounds = mainWindow.getBounds();

  // Posiciona o emulador ao lado do Goose inicialmente
  syncEmulatorPosition(mainWindow);

  // Monitora movimentos da janela principal
  mainWindow.on('move', () => {
    if (isDockingEnabled) {
      syncEmulatorPosition(mainWindow);
    }
  });

  mainWindow.on('resize', () => {
    if (isDockingEnabled) {
      syncEmulatorPosition(mainWindow);
    }
  });

  log.info('[WindowDocking] Docking enabled');
  return true;
}

/**
 * Desativa o docking
 */
export function disableDocking(): void {
  isDockingEnabled = false;
  dockedWindow = null;
  lastBounds = null;
  log.info('[WindowDocking] Docking disabled');
}

/**
 * Verifica se o docking está ativo
 */
export function isDockingActive(): boolean {
  return isDockingEnabled && dockedWindow !== null;
}

/**
 * Sincroniza a posição do emulador com a janela principal
 */
function syncEmulatorPosition(mainWindow: BrowserWindow): void {
  if (!dockedWindow || !isDockingEnabled) return;

  try {
    const gooseBounds = mainWindow.getBounds();

    // Verifica se realmente houve mudança de posição
    if (lastBounds &&
        lastBounds.x === gooseBounds.x &&
        lastBounds.y === gooseBounds.y &&
        lastBounds.width === gooseBounds.width &&
        lastBounds.height === gooseBounds.height) {
      return;
    }

    lastBounds = gooseBounds;

    // Posiciona o emulador à direita do Goose
    const newX = gooseBounds.x + gooseBounds.width + DOCK_GAP;
    const newY = gooseBounds.y;

    dockedWindow.setBounds({
      x: newX,
      y: newY,
      // Mantém o tamanho original do emulador
      // height: gooseBounds.height // Opcional: igualar altura
    });

    // Traz o emulador para frente
    dockedWindow.bringToTop();

  } catch (error) {
    log.error('[WindowDocking] Error syncing position:', error);
    // Se der erro, tenta encontrar o emulador novamente
    dockedWindow = findEmulatorWindow();
  }
}

/**
 * Reattach - encontra e reconecta ao emulador
 */
export function reattachEmulator(mainWindow: BrowserWindow): boolean {
  dockedWindow = findEmulatorWindow();
  if (dockedWindow && isDockingEnabled) {
    syncEmulatorPosition(mainWindow);
    log.info('[WindowDocking] Reattached to emulator');
    return true;
  }
  return false;
}
