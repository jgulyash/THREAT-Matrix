import { useMemo } from 'react';
import { MATRIX_LABELS } from '../lib/constants';
import { MIN_QUERY, SEARCH_KIND_LABELS, search } from '../lib/search';
import { Go } from '../lib/nav';
import { DraftTag } from './DraftTag';

// Results shown per group before the rest are summarized by count.
const GROUP_LIMIT = 60;

export function SearchView({ query }: { query: string }) {
  const q = query.trim();
  const results = useMemo(() => search(q), [q]);
  const tooShort = q.length < MIN_QUERY;

  return (
    <div className="bib-view search-view">
      <h1 className="bib-title" data-focus-target tabIndex={-1}>
        Search
      </h1>
      <div className="bib-sub" data-search-summary role="status" aria-live="polite">
        {tooShort
          ? `Type at least ${MIN_QUERY} characters in the search field. Press / from anywhere to focus it. Search covers tactic names, indicator behavior text, countermeasure and protocol text, actor profile names, sources, and IDs.`
          : results.total === 0
          ? `No results for "${q}".`
          : `${results.total} result${results.total === 1 ? '' : 's'} for "${q}": ${results.groups
              .map((g) => `${g.hits.length} ${SEARCH_KIND_LABELS[g.kind].toLowerCase()}`)
              .join(', ')}.`}
      </div>
      {results.groups.map((g) => (
        <div key={g.kind} data-search-group={g.kind}>
          <h2 className="dr-section-header">
            <span>{SEARCH_KIND_LABELS[g.kind]}</span>
            <span className="dr-section-count">
              {g.hits.length > GROUP_LIMIT ? `first ${GROUP_LIMIT} of ${g.hits.length}` : g.hits.length}
            </span>
          </h2>
          <div className="search-results">
            {g.hits.slice(0, GROUP_LIMIT).map((d) => (
              <Go key={`${d.kind}-${d.id}`} className="ind-related-link" to={d.to}>
                <div className="ind-related-head">
                  <span className="adv-tactic-id">{d.id}</span>
                  <span className="ind-related-tactic">
                    {d.context}
                    {d.matrix && MATRIX_LABELS[d.matrix] && <DraftTag matrix={d.matrix} />}
                  </span>
                </div>
                <div className="ind-related-beh">{d.title}</div>
              </Go>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
