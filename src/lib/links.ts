// External link targets, kept in one place.
export const REPO_URL = 'https://github.com/jgulyash/THREAT-Matrix';
const BLOB = `${REPO_URL}/blob/main`;
const TREE = `${REPO_URL}/tree/main`;

export const LINKS = {
  repository: REPO_URL,
  methodology: `${BLOB}/docs/METHODOLOGY.md`,
  limitations: `${BLOB}/docs/METHODOLOGY.md#limitations-and-intended-use`,
  caseWorksheet: `${BLOB}/examples/case-record-worksheet.md`,
  experimentalScoring: `${TREE}/examples/experimental-scoring`,
};

// A URL from the data is rendered as a link only if it parses and its scheme
// is http or https. Anything else (javascript:, data:, relative, malformed)
// is shown as plain text.
export function safeHttpUrl(url: unknown): string | null {
  if (typeof url !== 'string' || !url) return null;
  try {
    const u = new URL(url);
    return u.protocol === 'http:' || u.protocol === 'https:' ? u.href : null;
  } catch {
    return null;
  }
}
