import { STUB } from '../lib/constants';

interface Props {
  matrix: 'facility' | 'organization' | 'system';
  version: string;
}

export function StubLanding({ matrix, version }: Props) {
  const label = matrix.charAt(0).toUpperCase() + matrix.slice(1);
  const s = STUB[matrix];
  const total =
    Object.values(s.phases).reduce((n, v) => n + v, 0) + s.flight + s.claim;
  return (
    <div className="stub-landing">
      <div style={{ textAlign: 'center' }}>
        <div className="stub-landing-label">{version} · Planned</div>
        <div className="stub-landing-title">{label} Matrix</div>
        <div className="stub-landing-sub">
          {total} tactics across 4 phases. Ships in {version}.
        </div>
      </div>
    </div>
  );
}
