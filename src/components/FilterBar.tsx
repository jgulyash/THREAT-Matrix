interface Props {
  cpnFilter: boolean;
  setCpnFilter: (fn: (v: boolean) => boolean) => void;
}

export function FilterBar({ cpnFilter, setCpnFilter }: Props) {
  return (
    <div className="filterbar">
      <span className="fb-label">Filter</span>
      <div className="fb-sep" />
      <span
        className={`fb-chip${cpnFilter ? ' amber-active' : ' dim'}`}
        onClick={() => setCpnFilter((v) => !v)}
        title="Show only Cyber-Physical Nexus tactics"
      >
        ⌖ CPN
      </span>
      <div className="fb-sep" />
      <span className="fb-chip v11" title="Actor filter launches in V1.1">
        Actor ▾<span className="v11-badge">V1.1</span>
      </span>
    </div>
  );
}
