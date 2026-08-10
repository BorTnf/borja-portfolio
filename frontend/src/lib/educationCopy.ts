import type { Locale } from "@/i18n/types";

interface EducationCopy {
  degree?: string;
  fieldOfStudy?: string;
  status?: string;
  highlights?: string[];
}

const EDUCATION_EN: Record<string, EducationCopy> = {
  // English copy for each education "id" in backend/app/data/education.json goes here.
};

export function localizeEducationFields<
  T extends {
    id: string;
    degree: string;
    fieldOfStudy: string;
    status: string;
    highlights: string[];
  },
>(item: T, locale: Locale): T {
  if (locale !== "en") return item;
  const copy = EDUCATION_EN[item.id];
  if (!copy) return item;
  return {
    ...item,
    degree: copy.degree ?? item.degree,
    fieldOfStudy: copy.fieldOfStudy ?? item.fieldOfStudy,
    status: copy.status ?? (item.status === "completed" ? "Completed" : item.status),
    highlights: copy.highlights ?? item.highlights,
  } as T;
}
