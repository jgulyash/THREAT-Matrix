// Guarded storage access. Browsers throw on any touch of localStorage when
// site data is blocked; a stored preference must never be able to blank the
// site, so every read and write goes through here.
export function readPref(key: string): string | null {
  try {
    return window.localStorage.getItem(key);
  } catch {
    return null;
  }
}

export function writePref(key: string, value: string | null): void {
  try {
    if (value === null) window.localStorage.removeItem(key);
    else window.localStorage.setItem(key, value);
  } catch {
    // Storage unavailable: the preference lasts for this page load only.
  }
}
