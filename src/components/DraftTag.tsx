import { isDraft } from '../lib/data';

// Marks a matrix whose maturity is "draft" wherever that matrix is named.
export function DraftTag({ matrix }: { matrix: string }) {
  if (!isDraft(matrix)) return null;
  return (
    <span className="type-level-tag draft-tag" title="Draft matrix: content is under review and may change.">
      draft
    </span>
  );
}
