import type { ReactNode } from 'react';
import { useState } from 'react';
import { PlusCircle, Wrench } from 'lucide-react';
import { Button } from '@/shared/components/ui/button.tsx';
import { useProjectSelectionContext } from '@/shared/contexts/ProjectContext.tsx';
import type { Project } from '@/types/project.ts';
import { CreateProjectModal } from '@/shared/components/GlobalHeader/CreateProjectModal.tsx';
import { ProjectSettingsModal } from '@/shared/components/modals/ProjectSettingsModal.tsx';

type ProjectSummary = {
  project_id: string;
  slug?: string;
  name: string;
  metadata?: Record<string, unknown>;
};

interface ProjectHeaderActionsProps {
  selectedProject: ProjectSummary | null;
  onProjectCreated?: () => void;
  onProjectUpdated?: () => void;
  disabled?: boolean;
  confirmNavigation?: () => boolean;
}

function toProject(summary: ProjectSummary | null, contextProject: Project | null): Project | null {
  if (!summary) return null;
  const id = summary.project_id;
  if (contextProject?.id !== id) contextProject = null;
  const aspectRatio = typeof summary.metadata?.aspect_ratio === 'string'
    ? summary.metadata.aspect_ratio
    : typeof summary.metadata?.aspectRatio === 'string'
      ? summary.metadata.aspectRatio
      : contextProject?.aspectRatio;
  return {
    id,
    name: summary.name,
    user_id: contextProject?.user_id ?? 'local-user',
    ...(aspectRatio ? { aspectRatio } : {}),
    createdAt: contextProject?.createdAt,
  };
}

function ProjectActionButton({
  label,
  onClick,
  disabled,
  children,
}: {
  label: string;
  onClick: () => void;
  disabled?: boolean;
  children: ReactNode;
}) {
  return (
    <Button
      type="button"
      variant="ghost"
      size="icon"
      className="h-7 w-7 shrink-0 rounded-md border border-border/70 bg-card/80 text-muted-foreground hover:bg-accent hover:text-foreground"
      onClick={onClick}
      disabled={disabled}
      title={label}
      aria-label={label}
    >
      {children}
    </Button>
  );
}

export function ProjectHeaderActions({
  selectedProject,
  onProjectCreated,
  onProjectUpdated,
  disabled = false,
  confirmNavigation,
}: ProjectHeaderActionsProps) {
  const { project: contextProject } = useProjectSelectionContext();
  const [isCreateProjectModalOpen, setIsCreateProjectModalOpen] = useState(false);
  const [isProjectSettingsModalOpen, setIsProjectSettingsModalOpen] = useState(false);
  const project = toProject(selectedProject, contextProject);

  return (
    <>
      <div className="flex shrink-0 items-center gap-1" data-testid="astrid-project-actions">
        <ProjectActionButton
          label="Project settings"
          onClick={() => setIsProjectSettingsModalOpen(true)}
          disabled={disabled || !project}
        >
          <Wrench className="h-3.5 w-3.5" />
        </ProjectActionButton>
        <Button
          type="button"
          variant="ghost"
          size="sm"
          className="h-7 shrink-0 gap-1.5 rounded-md border border-border/70 bg-card/80 px-2 text-xs text-muted-foreground hover:bg-accent hover:text-foreground"
          onClick={() => setIsCreateProjectModalOpen(true)}
          aria-label="New project"
          disabled={disabled}
        >
          <PlusCircle className="h-3.5 w-3.5" aria-hidden="true" />
          <span>New project</span>
        </Button>
      </div>

      <CreateProjectModal
        isOpen={isCreateProjectModalOpen}
        onOpenChange={setIsCreateProjectModalOpen}
        onProjectCreated={onProjectCreated}
        confirmNavigation={confirmNavigation}
      />
      <ProjectSettingsModal
        isOpen={isProjectSettingsModalOpen}
        onOpenChange={(open) => {
          setIsProjectSettingsModalOpen(open);
          if (!open) onProjectUpdated?.();
        }}
        project={project}
      />
    </>
  );
}
