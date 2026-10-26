import {createContext, useContext, type ReactNode} from 'react';
import type {CompositionRegistries} from './registries';

const RegistryContext = createContext<CompositionRegistries>({});

export const ElementRegistryProvider = ({value, children}: {
  value: CompositionRegistries;
  children: ReactNode;
}) => <RegistryContext.Provider value={value}>{children}</RegistryContext.Provider>;

export const useElementRegistries = (): CompositionRegistries => useContext(RegistryContext);
