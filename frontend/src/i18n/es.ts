import type { Translations } from "@/i18n/types";

export const es: Translations = {
  meta: {
    title: "Borja González - Responsable de Contenidos y Automatización",
  },
  hero: {
    greeting: "Hola",
    name: "Soy Borja",
    roles: ["Responsable de Contenidos y Automatización"],
    tagline: "Conoce mi perfil preguntando lo que quieras.",
  },
  prompts: {
    placeholders: [
      "Pregúntame sobre mi experiencia en IA...",
      "Pregúntame sobre mis proyectos...",
      "Pregúntame sobre mi docencia...",
      "Pregúntame lo que quieras...",
    ],
    sendAriaLabel: "Enviar",
  },
  suggestions: [
    {
      id: "ai",
      label: "Inteligencia Artificial",
      question: "Cuéntame sobre tu experiencia con IA...",
    },
    {
      id: "automation",
      label: "Automatización",
      question: "¿Qué automatizaciones con IA has desarrollado?",
    },
    {
      id: "content",
      label: "Contenidos",
      question: "¿Cómo trabajas la generación y gestión de contenidos?",
    },
    {
      id: "marketing",
      label: "Marketing",
      question: "Cuéntame sobre tu experiencia en marketing...",
    },
    {
      id: "bigdata",
      label: "Big Data",
      question: "¿Qué experiencia tienes con Big Data?",
    },
    {
      id: "education",
      label: "Educación",
      question: "¿Cuál es tu formación académica?",
    },
    {
      id: "experience",
      label: "Experiencia",
      question: "Resume tu experiencia profesional...",
    },
    {
      id: "projects",
      label: "Proyectos",
      question: "Muéstrame todos tus proyectos...",
    },
  ],
  loading: {
    label: "Arquitectando insights",
    status: {
      thinking: "Analizando tu pregunta…",
      synthesizing: "Armando la respuesta…",
      done: "¡Listo!",
      followUp: "Consultando…",
    },
    tools: {
      get_skills: "Skills",
      get_projects: "Proyectos",
      get_experience: "Experiencia",
      get_timeline: "Timeline",
      get_education: "Educación",
      get_certifications: "Certificaciones",
      get_languages: "Idiomas",
      get_soft_skills: "Habilidades blandas",
      get_contact: "Contacto",
    },
  },
  errors: {
    connectionTitle: "Problema de conexión",
    connectionSummary:
      "No pudimos conectar con el backend en este momento. Verifica que la API esté en ejecución.",
    rateLimitTitle: "Límite de preguntas superado",
    rateLimitSummary: "Has superado el límite de 10 preguntas por minuto. Por favor, espera un momento antes de volver a preguntar.",
    downloadCV: "Descargar CV Completo",
  },
  dashboard: {
    askAgain: "Volver a preguntar",
    askAgainAriaLabel: "Volver a la pantalla inicial para hacer otra pregunta",
  },
  footer: {
    tagline: "© Borja González González · Hecho con contenidos, automatización e inteligencia (artificial).",
    getInTouch: "Contacto",
    emailCopied: "¡Email copiado!",
  },
  langSwitcher: {
    ariaLabel: "Seleccionar idioma",
  },
  projects: {
    title: "Proyectos",
    viewDetails: "Ver detalles",
    modal: {
      close: "Cerrar detalle del proyecto",
      returnToPortfolio: "Volver al portfolio",
      challenge: "El desafío",
      solution: "La solución",
      results: "Resultados",
      highlights: "Puntos clave",
      role: "Rol",
      team: "Equipo y atribución",
    },
  },
};
