import { useEffect, useRef, useState, type FormEvent } from 'react';
import type { Route } from '../lib/route';
import { MATRIX_KEYS, MATRIX_LABELS } from '../lib/constants';
import { COUNTS, FRAMEWORK_LICENSE, FRAMEWORK_VERSION } from '../lib/data';
import { Go } from '../lib/nav';
import { DraftTag } from './DraftTag';

interface Props {
  route: Route;
  theme: 'dark' | 'light';
  setTheme: (t: 'dark' | 'light') => void;
}

const searchHash = (q: string) => `#/search/${encodeURIComponent(q.trim())}`;

function SearchBox({ route }: { route: Route }) {
  const routeQuery = route.view === 'search' ? route.query : '';
  const [value, setValue] = useState(routeQuery);
  const ref = useRef<HTMLInputElement>(null);

  // Follow the URL (back and forward, shared links) unless the user is typing.
  useEffect(() => {
    if (document.activeElement !== ref.current) setValue(routeQuery);
  }, [routeQuery]);

  // "/" focuses search from anywhere outside a text field.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
      const el = document.activeElement;
      const tag = el?.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
      e.preventDefault();
      ref.current?.focus();
      ref.current?.select();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const onChange = (next: string) => {
    setValue(next);
    // Results update as the user types once the search view is open.
    if (route.view === 'search') window.location.replace(searchHash(next));
  };

  const onSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (route.view === 'search') window.location.replace(searchHash(value));
    else window.location.hash = searchHash(value);
  };

  return (
    <form className="topbar-search" role="search" onSubmit={onSubmit}>
      <input
        ref={ref}
        type="search"
        className="search-input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Escape') onChange('');
        }}
        placeholder="Search"
        aria-label="Search tactics, indicators, countermeasures, protocols, actor profiles, and sources"
        title="Search (press / to focus)"
        autoComplete="off"
        spellCheck={false}
        maxLength={200}
      />
    </form>
  );
}

export function TopNav({ route, theme, setTheme }: Props) {
  const isActors =
    route.view === 'actors' || route.view === 'actorDetail' || route.view === 'reservedActor';
  const activeMatrix =
    route.view === 'heatmap' ||
    route.view === 'phase' ||
    route.view === 'tactic' ||
    route.view === 'indicator'
      ? route.matrix
      : null;
  const tab = (active: boolean) => ({
    className: `mtab${active ? ' active' : ''}`,
    'aria-current': active ? ('page' as const) : undefined,
  });
  return (
    <nav className="topbar" aria-label="Primary">
      <Go className="topbar-logo" to="/">
        <em>THREAT</em>&nbsp;Matrix
      </Go>
      <div className="matrix-tabs">
        <Go to="/" {...tab(route.view === 'overview')}>
          Overview
        </Go>
        {MATRIX_KEYS.map((m) => (
          <Go key={m} to={`/${m}`} {...tab(activeMatrix === m)}>
            {MATRIX_LABELS[m]}
            <DraftTag matrix={m} />
          </Go>
        ))}
        <Go to="/actors" {...tab(isActors)}>
          Actor Profiles
        </Go>
        <Go to="/references" {...tab(route.view === 'references')}>
          References
        </Go>
      </div>
      <div className="topbar-spacer" />
      <SearchBox route={route} />
      <span className="topbar-meta">
        {COUNTS.tactics} tactics · {COUNTS.indicators} indicators · {COUNTS.profiles} profiles · {FRAMEWORK_LICENSE}
      </span>
      <span className="badge-v1">v{FRAMEWORK_VERSION}</span>
      <button
        type="button"
        className="theme-toggle"
        onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
        aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
        title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
      >
        <span aria-hidden="true">{theme === 'dark' ? '☀' : '☾'}</span>
      </button>
    </nav>
  );
}
