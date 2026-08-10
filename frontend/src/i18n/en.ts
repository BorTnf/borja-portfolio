import type { Translations } from "@/i18n/types";

export const en: Translations = {
  meta: {
    title: "Borja González - Content & Automation Lead",
  },
  hero: {
    greeting: "Hi",
    name: "I'm Borja",
    roles: ["Content & Automation Lead"],
    tagline: "Get to know me by asking anything.",
  },
  prompts: {
    placeholders: [
      "Ask about my AI experience...",
      "Ask about my projects...",
      "Ask about my teaching background...",
      "Ask me anything...",
    ],
    sendAriaLabel: "Send",
  },
  suggestions: [
    {
      id: "ai",
      label: "Artificial Intelligence",
      question: "Tell me about your AI experience...",
    },
    {
      id: "automation",
      label: "Automation",
      question: "What AI-driven automations have you built?",
    },
    {
      id: "content",
      label: "Content",
      question: "How do you approach content generation and management?",
    },
    {
      id: "marketing",
      label: "Marketing",
      question: "Tell me about your marketing experience...",
    },
    {
      id: "bigdata",
      label: "Big Data",
      question: "What is your experience with Big Data?",
    },
    {
      id: "education",
      label: "Education",
      question: "What is your educational background?",
    },
    {
      id: "experience",
      label: "Experience",
      question: "Summarize your professional experience...",
    },
    {
      id: "projects",
      label: "Projects",
      question: "Show me all your projects...",
    },
  ],
  loading: {
    label: "Architecting Insights",
    status: {
      thinking: "Analyzing your question…",
      synthesizing: "Building the response…",
      done: "Done!",
      followUp: "Looking that up…",
    },
    tools: {
      get_skills: "Skills",
      get_projects: "Projects",
      get_experience: "Experience",
      get_timeline: "Timeline",
      get_education: "Education",
      get_certifications: "Certifications",
      get_languages: "Languages",
      get_soft_skills: "Soft Skills",
      get_contact: "Contact",
    },
  },
  errors: {
    connectionTitle: "Connection issue",
    connectionSummary: "Couldn't reach the backend right now. Please make sure the API is running.",
    rateLimitTitle: "Rate limit exceeded",
    rateLimitSummary: "You have exceeded the limit of 10 questions per minute. Please wait a moment before asking again.",
    downloadCV: "Download Full CV",
  },
  dashboard: {
    askAgain: "Ask again",
    askAgainAriaLabel: "Return to the home screen to ask another question",
  },
  footer: {
    tagline: "© Borja González González · Made with content, automation, and artificial intelligence.",
    getInTouch: "Get in Touch",
    emailCopied: "Email copied!",
  },
  langSwitcher: {
    ariaLabel: "Select language",
  },
  projects: {
    title: "Projects",
    viewDetails: "View details",
    modal: {
      close: "Close project detail",
      returnToPortfolio: "Return to portfolio",
      challenge: "The challenge",
      solution: "The solution",
      results: "Results",
      highlights: "Highlights",
      role: "Role",
      team: "Team & attribution",
    },
  },
};
