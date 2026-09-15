import React from 'react';
import type { Citation } from './ChatMessage';

interface CitationBadgeProps {
  citation: Citation;
  index: number;
}

export const CitationBadge: React.FC<CitationBadgeProps> = ({ citation, index }) => {
  if (citation.url) {
    return (
      <a
        href={citation.url}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex items-center justify-center px-1.5 py-0.5 mx-1 text-xs font-semibold rounded bg-[var(--color-secondary-container)] text-[var(--color-on-secondary-container)] hover:bg-[var(--color-secondary)] hover:text-[var(--color-on-secondary)] transition-colors"
        title={citation.title}
        aria-label={`Citation ${index}: ${citation.title}`}
      >
        [{index}]
      </a>
    );
  }
  return (
    <span
      className="inline-flex items-center justify-center px-1.5 py-0.5 mx-1 text-xs font-semibold rounded bg-[var(--color-surface-variant)] text-[var(--color-on-surface-variant)] cursor-help"
      title={citation.title}
      aria-label={`Citation ${index}: ${citation.title}`}
    >
      [{index}]
    </span>
  );
};
