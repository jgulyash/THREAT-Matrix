import type { BibliographyEntry, Tactic } from '../types/framework';
import { MATRICES, MATRIX_LABELS } from '../lib/constants';

interface Props {
  bibliography: Record<string, BibliographyEntry>;
  bibReverseMap: Record<string, Tactic[]>;
  navigate: (path: string) => void;
}

const TYPE_LABELS: Record<string, string> = {
  government_report: 'Gov Report',
  academic_paper: 'Academic',
  book: 'Book',
  court_document: 'Court Doc',
  after_action_review: 'AAR',
  news_investigation: 'Investigation',
  incident_database: 'Incident DB',
  practitioner_guide: 'Practitioner Guide',
  standard: 'Standard',
};

const MATRIX_ORDER = MATRICES.map((m) => m.key as string);

export function BibliographyView({ bibliography, bibReverseMap, navigate }: Props) {
  const entries = Object.entries(bibliography || {}).sort((a, b) => {
    const typeA = a[1].type || '';
    const typeB = b[1].type || '';
    if (typeA !== typeB) return typeA.localeCompare(typeB);
    return (b[1].date || '').localeCompare(a[1].date || '');
  });

  // Group by matrices[] tag; a multi-tagged entry appears in each of its
  // sections. Untagged entries fall back to a trailing group.
  const sections = MATRIX_ORDER.map((m) => ({
    matrix: m,
    label: MATRIX_LABELS[m] || m,
    entries: entries.filter(([, e]) => (e.matrices || []).includes(m)),
  })).filter((s) => s.entries.length > 0);
  const untagged = entries.filter(([, e]) => !(e.matrices || []).length);
  if (untagged.length > 0) {
    sections.push({ matrix: 'untagged', label: 'Untagged', entries: untagged });
  }

  return (
    <div className="bib-view">
      <div className="bib-title">Bibliography</div>
      <div className="bib-sub">
        {entries.length} sources cited across the framework, grouped by the
        matrix each source informs. Each entry lists the tactics that reference it.
      </div>
      {sections.map(({ matrix, label, entries: sectionEntries }) => (
        <div key={matrix}>
          <div className="dr-section-header">
            <span>{label}</span>
            <span className="dr-section-count">
              {sectionEntries.length} source{sectionEntries.length === 1 ? '' : 's'}
            </span>
          </div>
          {sectionEntries.map(([key, entry]) => {
            const citingTactics = bibReverseMap[key] || [];
            return (
              <div key={`${matrix}-${key}`} id={`bib-${matrix}-${key}`} className="bib-entry">
                <div className="bib-entry-head">
                  <span className="bib-entry-key">{key}</span>
                  <span className="bib-entry-type">
                    {TYPE_LABELS[entry.type] || entry.type}
                  </span>
                </div>
                <div className="bib-entry-title">{entry.title}</div>
                <div className="bib-entry-meta">
                  {entry.author} · {entry.date}
                  {entry.doi ? ` · DOI: ${entry.doi}` : ''}
                </div>
                {entry.url && (
                  <a
                    className="bib-entry-url"
                    href={entry.url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {entry.url}
                  </a>
                )}
                <div className="bib-entry-rel">{entry.relevance_summary}</div>
                {citingTactics.length > 0 && (
                  <div className="bib-entry-cited">
                    <div className="bib-entry-cited-label">
                      Cited by {citingTactics.length} tactic{citingTactics.length === 1 ? '' : 's'}
                    </div>
                    <div className="bib-entry-cited-list">
                      {citingTactics.map((t) => (
                        <a
                          key={t.id}
                          className="bib-entry-cited-pill"
                          href={`#/${t.matrix}/tactic/${t.id}`}
                          onClick={(e) => {
                            e.preventDefault();
                            navigate(`/${t.matrix}/tactic/${t.id}`);
                          }}
                          title={t.name}
                        >
                          {t.id}
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      ))}
    </div>
  );
}
