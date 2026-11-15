import { COUNTS, FRAMEWORK_LICENSE, FRAMEWORK_VERSION, getMatrix, isDraft } from '../lib/data';
import { LINKS } from '../lib/links';
import { MATRIX_LABELS, type MatrixKey } from '../lib/constants';
import { Go } from '../lib/nav';
import { DraftTag } from './DraftTag';

function ExternalLinks() {
  return (
    <>
      <a href={LINKS.methodology} target="_blank" rel="noopener noreferrer">Methodology</a>
      <a href={LINKS.limitations} target="_blank" rel="noopener noreferrer">Limitations</a>
      <Go to="/references">Sources</Go>
      <a href={LINKS.repository} target="_blank" rel="noopener noreferrer">Repository</a>
    </>
  );
}

// What this is, what it is not, who it is for. Shown on the landing view.
export function LandingNotice() {
  return (
    <section className="intro" aria-label="About THREAT Matrix">
      <p>
        <strong>THREAT Matrix</strong> is an open behavioral vocabulary and evidence index for threat
        assessment: observable behaviors, organized by target and phase, each tied to its sources. It
        is for threat assessment and management teams, protective intelligence analysts, and security
        practitioners who need shared terms for what they observe.
      </p>
      <p>
        It is <strong>not</strong> a risk score, not predictive, not grounds for adverse action against
        any person, and not a substitute for professional judgment.
      </p>
      <p className="intro-meta">
        <span>
          Version {FRAMEWORK_VERSION} · {COUNTS.tactics} tactics · {COUNTS.indicators} indicators ·{' '}
          {COUNTS.sources} sources · {FRAMEWORK_LICENSE}
        </span>
        <ExternalLinks />
      </p>
    </section>
  );
}

// Names the matrix a scoped view is showing, with its scope statement.
export function MatrixHeader({ matrix }: { matrix: MatrixKey }) {
  const info = getMatrix(matrix);
  return (
    <section className="intro" aria-label={`${MATRIX_LABELS[matrix]} matrix`}>
      <p className="intro-title" data-focus-target tabIndex={-1}>
        {MATRIX_LABELS[matrix]} matrix
        <DraftTag matrix={matrix} />
        <span className="intro-count">{info.tactics.length} tactics</span>
      </p>
      {info.scope && <p>{info.scope}</p>}
      {isDraft(matrix) && (
        <p>This matrix is a draft. Its content is still under review and may change between versions.</p>
      )}
    </section>
  );
}

export function Footer({ children }: { children?: React.ReactNode }) {
  return (
    <footer className="site-footer">
      <span className="site-footer-links">
        <span>THREAT Matrix v{FRAMEWORK_VERSION} · {FRAMEWORK_LICENSE}</span>
        <ExternalLinks />
      </span>
      {children}
    </footer>
  );
}
