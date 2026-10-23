import { createRoot } from 'react-dom/client';
import { WelcomeFlow } from './WelcomeFlow.tsx';
import '@/index.css';

export function renderWelcome(root: HTMLElement): void {
  createRoot(root).render(<WelcomeFlow />);
}
