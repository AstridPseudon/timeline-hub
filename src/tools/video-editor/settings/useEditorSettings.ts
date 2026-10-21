import { useEffect, useMemo, useState } from 'react';

type Setter<T> = T | ((current: T) => T);

interface EditorSettingsOptions {
  debounceMs?: number;
  /** False keeps the value in memory only: nothing is read from or written to localStorage (the tour's demo timeline). */
  persist?: boolean;
}

export function useEditorSettings<T>(storageKey: string, initialValue: T, { debounceMs = 200, persist = true }: EditorSettingsOptions = {}) {
  const initial = useMemo(() => {
    if (!persist) return initialValue;
    try {
      const stored = window.localStorage.getItem(storageKey);
      return stored ? (JSON.parse(stored) as T) : initialValue;
    } catch {
      return initialValue;
    }
  }, [initialValue, persist, storageKey]);

  const [value, setValueState] = useState<T>(initial);

  useEffect(() => {
    if (!persist) return;
    const timeout = window.setTimeout(() => {
      window.localStorage.setItem(storageKey, JSON.stringify(value));
    }, debounceMs);

    return () => {
      window.clearTimeout(timeout);
    };
  }, [debounceMs, persist, storageKey, value]);

  const setValue = (update: Setter<T>) => {
    setValueState((current) => (typeof update === 'function' ? (update as (current: T) => T)(current) : update));
  };

  return [value, setValue] as const;
}
