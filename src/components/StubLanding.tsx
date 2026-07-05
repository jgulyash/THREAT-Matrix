import { STUB, MATRIX_LABELS } from '../lib/constants';

interface Props {
  matrix: 'facility' | 'organization' | 'infrastructure';
  version: string;
}

export function StubLanding({ matrix, version }: Props) {
  const label = MATRIX_LABELS[matrix];
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
