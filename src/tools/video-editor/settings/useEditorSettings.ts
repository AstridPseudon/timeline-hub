import { useEffect, useMemo, useRef, useState } from 'react';

type Setter<T> = T | ((current: T) => T);

/**
 * A localStorage-backed value. Only an explicit `setValue` is written back: mounting with the default
 * (or with a record that merely lacks newer fields) must not turn that default into a saved choice.
 */
export function useEditorSettings<T>(storageKey: string, initialValue: T, debounceMs = 200) {
  const initial = useMemo(() => {
    try {
      const stored = window.localStorage.getItem(storageKey);
      return stored ? (JSON.parse(stored) as T) : initialValue;
    } catch {
      return initialValue;
    }
  }, [initialValue, storageKey]);

  const [value, setValueState] = useState<T>(initial);
  const changedByCaller = useRef(false);

  useEffect(() => {
    if (!changedByCaller.current) return undefined;
    const timeout = window.setTimeout(() => {
      window.localStorage.setItem(storageKey, JSON.stringify(value));
    }, debounceMs);

    return () => {
      window.clearTimeout(timeout);
    };
  }, [debounceMs, storageKey, value]);

  const setValue = (update: Setter<T>) => {
    changedByCaller.current = true;
    setValueState((current) => (typeof update === 'function' ? (update as (current: T) => T)(current) : update));
  };

  return [value, setValue] as const;
}
