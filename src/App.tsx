import { useCallback, useEffect, useRef, useState } from 'react';
import { isMatrixView, parseLocation, type Route } from './lib/route';
import { MATRIX_LABELS, PHASE_NAMES } from './lib/constants';
import { actorById, tacticById } from './lib/data';
import { readPref, writePref } from './lib/storage';
import { FilterContext } from './lib/nav';
import { OverlayProvider } from './lib/overlay';
import { TopNav } from './components/TopNav';
import { FilterBar } from './components/FilterBar';
import { HeatMapGrid } from './components/HeatMapGrid';
import { SplitView } from './components/SplitView';
import { ActorProfilesView } from './components/ActorProfilesView';
import { ActorDetailView } from './components/ActorDetailView';
import { IndicatorDetail } from './components/IndicatorDetail';
import { BibliographyView } from './components/BibliographyView';
import { SearchView } from './components/SearchView';
import { ErrorBoundary } from './components/ErrorBoundary';
import { NotFoundView, ReservedActorView } from './components/NoticeViews';
import { Footer, LandingNotice, MatrixHeader } from './components/LandingNotice';
import { OverlayToggle } from './components/overlay/OverlayToggle';

type Theme = 'dark' | 'light';
const THEME_KEY = 'threat-matrix-theme';

const applyTheme = (t: Theme) => {
  if (t === 'light') document.documentElement.setAttribute('data-theme', 'light');
  else document.documentElement.removeAttribute('data-theme');
};

const PRODUCT = 'THREAT Matrix';

// Each route names itself in the document title: view name, then the product.
function titleFor(r: Route): string {
  const view = (() => {
    switch (r.view) {
      case 'overview':
        return 'Overview';
      case 'heatmap':
        return `${MATRIX_LABELS[r.matrix]} matrix`;
      case 'phase':
        return `${PHASE_NAMES[r.phase]} · ${MATRIX_LABELS[r.matrix]}`;
      case 'tactic':
        return `${r.tacticId} ${tacticById.get(r.tacticId)?.name || ''}`.trim();
      case 'indicator':
        return `Indicator ${r.indicatorId}`;
      case 'actors':
        return 'Actor Profiles';
      case 'actorDetail':
        return `${r.actorId} ${actorById.get(r.actorId)?.name || ''}`.trim();
      case 'reservedActor':
        return `${r.actorId} (reserved identifier)`;
      case 'references':
        return r.citedKey ? `Source ${r.citedKey}` : 'References';
      case 'search':
        return r.query ? `Search: ${r.query}` : 'Search';
      default:
        return 'Not found';
    }
  })();
  return `${view} | ${PRODUCT}`;
}

// The route path without the filter query: focus moves only when this changes.
const pathKey = () => window.location.hash.split('?')[0];

export default function App() {
  const [loc, setLoc] = useState(() => parseLocation());
  const [theme, setThemeState] = useState<Theme>(() =>
    readPref(THEME_KEY) === 'light' ? 'light' : 'dark'
  );
  const mainRef = useRef<HTMLElement>(null);
  const lastPath = useRef(pathKey());

  const setTheme = useCallback((t: Theme) => {
    setThemeState(t);
    writePref(THEME_KEY, t);
    applyTheme(t);
  }, []);

  useEffect(() => {
    applyTheme(theme);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => {
    const h = () => setLoc(parseLocation());
    window.addEventListener('hashchange', h);
    return () => window.removeEventListener('hashchange', h);
  }, []);

  const { route, filters } = loc;

  useEffect(() => {
    document.title = titleFor(route);
  }, [route]);

  // After a navigation, move keyboard focus to the new view's heading so the
  // next Tab continues from the content that just appeared. Typing in the
  // search field and views that focus a specific entry keep their own focus.
  useEffect(() => {
    const key = pathKey();
    if (key === lastPath.current) return;
    lastPath.current = key;
    const main = mainRef.current;
    if (!main) return;
    const active = document.activeElement;
    if (active instanceof HTMLInputElement && active.type === 'search') return;
    const ownFocus =
      (route.view === 'references' && route.citedKey) || (route.view === 'tactic' && route.focusId);
    if (ownFocus) return;
    main.scrollTop = 0;
    window.scrollTo(0, 0);
    const target = main.querySelector<HTMLElement>('[data-focus-target]') || main;
    target.focus({ preventScroll: true });
  }, [loc]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <FilterContext.Provider value={filters}>
      <OverlayProvider>
        <div className="app-root">
          <button type="button" className="skip-link" onClick={() => mainRef.current?.focus()}>
            Skip to content
          </button>
          <TopNav route={route} theme={theme} setTheme={setTheme} />
          {isMatrixView(route) && <FilterBar route={route} filters={filters} />}
          <main className="main-content" ref={mainRef} tabIndex={-1}>
            <ErrorBoundary>
              {route.view === 'overview' && (
                <>
                  <LandingNotice />
                  <HeatMapGrid scope={null} compact={false} route={route} />
                </>
              )}
              {route.view === 'heatmap' && (
                <>
                  <MatrixHeader matrix={route.matrix} />
                  <HeatMapGrid scope={route.matrix} compact={false} route={route} />
                </>
              )}
              {(route.view === 'phase' || route.view === 'tactic') && <SplitView route={route} />}
              {route.view === 'indicator' && <IndicatorDetail indicatorId={route.indicatorId} />}
              {route.view === 'actors' && <ActorProfilesView />}
              {route.view === 'actorDetail' && <ActorDetailView actorId={route.actorId} />}
              {route.view === 'reservedActor' && (
                <ReservedActorView actorId={route.actorId} reason={route.reason} />
              )}
              {route.view === 'references' && <BibliographyView citedKey={route.citedKey} />}
              {route.view === 'search' && <SearchView query={route.query} />}
              {route.view === 'notFound' && <NotFoundView what={route.what} />}
            </ErrorBoundary>
          </main>
          <Footer>
            <OverlayToggle />
          </Footer>
        </div>
      </OverlayProvider>
    </FilterContext.Provider>
  );
}
