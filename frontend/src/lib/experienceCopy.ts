import type { Locale } from "@/i18n/types";

interface ExperienceCopy {
  role?: string;
  summary?: string;
  highlights?: string[];
}

const EXPERIENCE_EN: Record<string, ExperienceCopy> = {
  // English copy for each experience "id" in backend/app/data/experience.json goes here.
};

export function localizeExperienceFields<
  T extends {
    id: string;
    role: string;
    summary: string;
    highlights: string[];
  },
>(item: T, locale: Locale): T {
  if (locale !== "en") return item;
  const copy = EXPERIENCE_EN[item.id];
  if (!copy) return item;
  return {
    ...item,
    role: copy.role ?? item.role,
    summary: copy.summary ?? item.summary,
    highlights: copy.highlights ?? item.highlights,
  } as T;
}
