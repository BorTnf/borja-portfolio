import type { Locale } from "@/i18n/types";
import type { PortfolioProject } from "@/lib/projectCatalog";

type ProjectTextFields = Pick<
  PortfolioProject,
  "name" | "summary" | "description" | "problem" | "solution" | "result" | "highlights"
> & {
  linkLabels?: Record<string, string>;
  mediaAlts?: string[];
};

/** Copy en inglés para el board/modal de proyectos (el JSON fuente está en español). */
const PROJECT_EN: Record<string, ProjectTextFields> = {
  // English copy for each project "id" in backend/app/data/projects.json goes here.
};

export function localizeProject(project: PortfolioProject, locale: Locale): PortfolioProject {
  if (locale !== "en") return project;

  const copy = PROJECT_EN[project.id];
  if (!copy) return project;

  return {
    ...project,
    name: copy.name,
    summary: copy.summary,
    description: copy.description,
    problem: copy.problem,
    solution: copy.solution,
    result: copy.result,
    highlights: copy.highlights,
    links: project.links.map((link) => ({
      ...link,
      label: copy.linkLabels?.[link.label] ?? link.label,
    })),
    media: project.media.map((item, index) => ({
      ...item,
      alt: copy.mediaAlts?.[index] ?? item.alt,
    })),
  };
}
