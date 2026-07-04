import type { Route } from '../lib/route';
import frameworkData from '../../docs/data/framework.json';

interface Props {
  route: Route;
  navigate: (path: string) => void;
  theme: 'dark' | 'light';
  setTheme: (t: 'dark' | 'light') => void;
}

export function TopNav({ route, navigate, theme, setTheme }: Props) {
  const isActors = route.view === 'actors' || route.view === 'actorDetail';
  const isReferences = route.view === 'references';
  const isPerson = !isActors && !isReferences && route.view !== 'stub';
  const stubs: Array<['facility' | 'organization' | 'infrastructure', string]> = [
    ['facility', 'Facility'],
    ['organization', 'Organization'],
    ['infrastructure', 'Infrastructure'],
  ];
  return (
    <nav className="topbar">
      <a
        className="topbar-logo"
        href="#/person"
        onClick={(e) => { e.preventDefault(); navigate('/person'); }}
      >
        <em>THREAT</em>&nbsp;Matrix
      </a>
      <div className="matrix-tabs">
        <a
          className={`mtab${isPerson ? ' active' : ''}`}
          href="#/person"
          onClick={(e) => { e.preventDefault(); navigate('/person'); }}
        >
          Person
        </a>
        {stubs.map(([m, l]) => (
          <a
            key={m}
            className={`mtab stub${route.view === 'stub' && route.matrix === m ? ' active' : ''}`}
            href={`#/${m}`}
            onClick={(e) => { e.preventDefault(); navigate(`/${m}`); }}
          >
            {l}
          </a>
        ))}
        <a
          className={`mtab${isActors ? ' active' : ''}`}
          href="#/actors"
          onClick={(e) => { e.preventDefault(); navigate('/actors'); }}
        >
          Actor Profiles
        </a>
        <a
          className={`mtab${isReferences ? ' active' : ''}`}
          href="#/references"
          onClick={(e) => { e.preventDefault(); navigate('/references'); }}
        >
          References
        </a>
      </div>
      <div className="topbar-spacer" />
      <span className="topbar-meta">154 tactics · 27 profiles · MIT</span>
      <span className="badge-v1">v{frameworkData.version}</span>
      <button
        className="theme-toggle"
        onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
        title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
      >
        {theme === 'dark' ? '☀' : '☾'}
      </button>
    </nav>
  );
}
