import { useLayoutEffect, useRef } from 'react';
import { BIB_TYPE_LABELS, MATRIX_KEYS, MATRIX_LABELS, label } from '../lib/constants';
import { bibliography, citedBy } from '../lib/data';
import { safeHttpUrl } from '../lib/links';
import { seg } from '../lib/route';
import { Go } from '../lib/nav';
import { DraftTag } from './DraftTag';

interface Props {
  // Source key from the route (#/references/<key>): scrolled to and highlighted.
  citedKey: string | null;
}

// Stable and unique: one source can sit in several matrix sections, so the
// element id carries both the section and the source key.
const entryId = (matrix: string, key: string) => `bib-${matrix}-${key}`;

const entries = [...bibliography.entries()].sort((a, b) => {
  const typeA = a[1].type || '';
  const typeB = b[1].type || '';
  if (typeA !== typeB) return typeA.localeCompare(typeB);
  return (b[1].date || '').localeCompare(a[1].date || '');
});

// Group by matrices[] tag; a multi-tagged entry appears in each of its
// sections. Untagged entries fall back to a trailing group.
const sections = MATRIX_KEYS.map((m) => ({
  matrix: m as string,
  label: MATRIX_LABELS[m],
  entries: entries.filter(([, e]) => (e.matrices || []).includes(m)),
})).filter((s) => s.entries.length > 0);
const untagged = entries.filter(([, e]) => !(e.matrices || []).some((m) => (MATRIX_KEYS as string[]).includes(m)));
if (untagged.length > 0) {
  sections.push({ matrix: 'untagged', label: 'Untagged', entries: untagged });
}

export function BibliographyView({ citedKey }: Props) {
  const viewRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (!citedKey) return;
    const first = sections.find((s) => s.entries.some(([k]) => k === citedKey));
    const el = first ? document.getElementById(entryId(first.matrix, citedKey)) : null;
    if (!el) return;
    el.scrollIntoView({ block: 'start' });
    el.focus({ preventScroll: true });
  }, [citedKey]);

  return (
    <div className="bib-view" ref={viewRef}>
      <h1 className="bib-title" data-focus-target tabIndex={-1}>
        Bibliography
      </h1>
      <div className="bib-sub">
        {entries.length} sources cited across the framework, grouped by the
        matrix each source informs. Each entry lists the tactics that reference it.
      </div>
      {sections.map(({ matrix, label: sectionLabel, entries: sectionEntries }) => (
        <div key={matrix}>
          <h2 className="dr-section-header">
            <span>
              {sectionLabel}
              <DraftTag matrix={matrix} />
            </span>
            <span className="dr-section-count">
              {sectionEntries.length} source{sectionEntries.length === 1 ? '' : 's'}
            </span>
          </h2>
          {sectionEntries.map(([key, entry]) => {
            const citingTactics = citedBy.get(key) || [];
            const url = safeHttpUrl(entry.url);
            const cited = key === citedKey;
            return (
              <div
                key={`${matrix}-${key}`}
                id={entryId(matrix, key)}
                className={`bib-entry${cited ? ' cited' : ''}`}
                data-bib-key={key}
                tabIndex={-1}
              >
                <div className="bib-entry-head">
                  <Go className="bib-entry-key" to={`/references/${seg(key)}`} title="Link to this source">
                    {key}
                  </Go>
                  <span className="bib-entry-type">{label(BIB_TYPE_LABELS, entry.type)}</span>
                </div>
                <div className="bib-entry-title">{entry.title}</div>
                <div className="bib-entry-meta">
                  {entry.author} · {entry.date}
                  {entry.doi ? ` · DOI: ${entry.doi}` : ''}
                </div>
                {url ? (
                  <a className="bib-entry-url" href={url} target="_blank" rel="noopener noreferrer">
                    {entry.url}
                  </a>
                ) : (
                  entry.url && <span className="bib-entry-url plain">{entry.url}</span>
                )}
                <div className="bib-entry-rel">{entry.relevance_summary}</div>
                {citingTactics.length > 0 && (
                  <div className="bib-entry-cited">
                    <div className="bib-entry-cited-label">
                      Cited by {citingTactics.length} tactic{citingTactics.length === 1 ? '' : 's'}
                    </div>
                    <div className="bib-entry-cited-list">
                      {citingTactics.map((t) => (
                        <Go
                          key={t.id}
                          className="bib-entry-cited-pill"
                          to={`/${t.matrix}/tactic/${seg(t.id)}`}
                          title={t.name}
                        >
                          {t.id}
                        </Go>
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
