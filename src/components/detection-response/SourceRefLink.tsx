import { bibliography } from '../../lib/data';
import { seg } from '../../lib/route';
import { Go } from '../../lib/nav';

interface Props {
  refKey: string;
}

// A citation chip. The source key is part of the route, so the References
// view scrolls to and highlights the cited entry on arrival.
export function SourceRefLink({ refKey }: Props) {
  if (!bibliography.has(refKey)) {
    return (
      <span className="dr-tag source-link unresolved" title="This source key has no entry in the bibliography">
        {refKey}
      </span>
    );
  }
  return (
    <Go className="dr-tag source-link" to={`/references/${seg(refKey)}`} title={`Source: ${refKey}`}>
      {refKey}
    </Go>
  );
}
