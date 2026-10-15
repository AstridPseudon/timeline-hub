import {useMutation} from '@tanstack/react-query';
import { useMemo } from 'react';
import type { UseMutationOptions, UseMutationResult } from '@tanstack/react-query';
import {
  useDeleteResource,
  useListPublicResources,
  useListResources,
  type Resource,
  type SequenceComponentMetadata,
} from '@/features/resources/hooks/useResources.ts';
import {
  createVideoEditorSequenceComponentCatalog,
  type SequenceComponentResource,
  type VideoEditorSequenceComponentCatalog,
} from '@/tools/video-editor/lib/sequence-component-catalog.ts';
import { useOptionalSequenceComponentCatalog } from '@/tools/video-editor/runtime/catalogContexts.tsx';

export { SequenceComponentCatalogProvider } from '@/tools/video-editor/runtime/catalogContexts.tsx';

export type {
  CreateVideoEditorSequenceComponentInput,
  DeleteVideoEditorSequenceComponentInput,
  SequenceComponentResource,
  UpdateVideoEditorSequenceComponentInput,
  VideoEditorSequenceComponentCatalog,
  VideoEditorSequenceComponentCatalogOptions,
} from '@/tools/video-editor/lib/sequence-component-catalog.ts';

export { createVideoEditorSequenceComponentCatalog } from '@/tools/video-editor/lib/sequence-component-catalog.ts';

function toSequenceComponentResource(resource: Resource): SequenceComponentResource {
  const metadata = resource.metadata as SequenceComponentMetadata;
  return {
    ...metadata,
    id: resource.id,
    type: 'sequence-component',
    userId: resource.userId,
    user_id: resource.user_id,
    isPublic: resource.isPublic,
    is_public: resource.is_public ?? metadata.is_public,
    createdAt: resource.createdAt,
    created_at: resource.created_at,
  };
}

function useSupabaseSequenceComponentCatalog(
  userId: string | null | undefined,
  options?: { enabled?: boolean },
): VideoEditorSequenceComponentCatalog {
  const enabled = options?.enabled ?? true;
  // Both legs are user-scoped in practice; with no session (dev local-mode
  // editor) neither should fetch a backend.
  const privateQuery = useListResources('sequence-component', { enabled: enabled && Boolean(userId) });
  const publicQuery = useListPublicResources('sequence-component', { enabled: enabled && Boolean(userId) });
  const deleteComponent = useDeleteSequenceComponentResource();

  const components = useMemo(() => {
    const privateResources = userId ? privateQuery.data ?? [] : [];
    const publicResources = publicQuery.data ?? [];
    const deduped = new Map<string, SequenceComponentResource>();

    for (const resource of [...privateResources, ...publicResources]) {
      deduped.set(resource.id, toSequenceComponentResource(resource));
    }

    return [...deduped.values()];
  }, [privateQuery.data, publicQuery.data, userId]);

  return useMemo(() => createVideoEditorSequenceComponentCatalog({
    components,
    isLoading: privateQuery.isLoading || publicQuery.isLoading,
    isFetching: privateQuery.isFetching || publicQuery.isFetching,
    error: privateQuery.error ?? publicQuery.error ?? null,
    refetch: async () => Promise.all([privateQuery.refetch(), publicQuery.refetch()]),
    deleteComponent: async (variables) => deleteComponent.mutateAsync(variables),
  }), [
    deleteComponent,
    components,
    privateQuery,
    publicQuery,
  ]);
}

export function useResolvedSequenceComponentCatalog(
  userId: string | null | undefined,
  injectedCatalog?: VideoEditorSequenceComponentCatalog | null,
): VideoEditorSequenceComponentCatalog {
  const fallbackCatalog = useSupabaseSequenceComponentCatalog(userId, { enabled: !injectedCatalog });
  const selected=injectedCatalog??fallbackCatalog;
  return useMemo(()=>({...selected,canCreateComponent:false,canUpdateComponent:false,createComponent:undefined,updateComponent:undefined}),[selected]);
}

export function useSequenceResources(userId?: string | null | undefined) {
  const injectedCatalog = useOptionalSequenceComponentCatalog();
  const fallbackCatalog = useSupabaseSequenceComponentCatalog(userId, { enabled: !injectedCatalog });
  const selected=injectedCatalog??fallbackCatalog;
  return useMemo(()=>({...selected,canCreateComponent:false,canUpdateComponent:false,createComponent:undefined,updateComponent:undefined}),[selected]);
}

type CreateVars = { metadata: SequenceComponentMetadata };
type UpdateVars = { id: string; metadata: SequenceComponentMetadata };
type DeleteVars = { id: string };

export function useCreateSequenceComponentResource(): Omit<
  UseMutationResult<Resource, Error, CreateVars, unknown>,
  'mutate' | 'mutateAsync'
> & {
  mutate: UseMutationResult<Resource, Error, CreateVars, unknown>['mutate'];
  mutateAsync: (
    variables: CreateVars,
    options?: UseMutationOptions<Resource, Error, CreateVars, unknown>,
  ) => Promise<Resource>;
} {
  const mutation=useMutation<Resource,Error,CreateVars>({mutationFn:async()=>{
    throw new Error('Custom element code must be authored and admitted through project pack files. Embedded resource source creation/update is unsupported.');
  }});
  return mutation as unknown as ReturnType<typeof useCreateSequenceComponentResource>;
}

export function useUpdateSequenceComponentResource(): Omit<
  UseMutationResult<Resource, Error, UpdateVars, unknown>,
  'mutate' | 'mutateAsync'
> & {
  mutate: UseMutationResult<Resource, Error, UpdateVars, unknown>['mutate'];
  mutateAsync: (
    variables: UpdateVars,
    options?: UseMutationOptions<Resource, Error, UpdateVars, unknown>,
  ) => Promise<Resource>;
} {
  const mutation=useMutation<Resource,Error,UpdateVars>({mutationFn:async()=>{
    throw new Error('Custom element code must be authored and admitted through project pack files. Embedded resource source creation/update is unsupported.');
  }});
  return mutation as unknown as ReturnType<typeof useUpdateSequenceComponentResource>;
}

export function useDeleteSequenceComponentResource(): Omit<
  UseMutationResult<void, Error, DeleteVars, unknown>,
  'mutate' | 'mutateAsync'
> & {
  mutate: UseMutationResult<void, Error, DeleteVars, unknown>['mutate'];
  mutateAsync: (
    variables: DeleteVars,
    options?: UseMutationOptions<void, Error, DeleteVars, unknown>,
  ) => Promise<void>;
} {
  const mutation = useDeleteResource();

  return {
    ...mutation,
    mutate: (variables, options) =>
      mutation.mutate({ id: variables.id, type: 'sequence-component' }, options),
    mutateAsync: (variables, options) =>
      mutation.mutateAsync({ id: variables.id, type: 'sequence-component' }, options),
  };
}
