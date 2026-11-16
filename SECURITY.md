# Security and privacy policy

THREAT Matrix is a published vocabulary (JSON data and schemas), a static
viewer served from GitHub Pages, and a small set of Python scripts. It runs
no server, holds no accounts, and collects no case data. This policy covers
two kinds of report: security vulnerabilities and privacy problems.

## What to report privately

Report these privately, not in a public issue:

- A vulnerability in the published site, the viewer source, the scripts, or
  the CI configuration (for example: a data value that can execute script in
  the viewer, a workflow that can be made to run untrusted code, a dependency
  with a known flaw that affects this project).
- A privacy problem (for example: personal information about a real person
  that appears anywhere in the repository, its history, an issue, or a pull
  request; real case material posted by mistake; text that identifies a
  living private individual).

Ordinary content corrections (a wrong citation, a tactic in the wrong phase,
a broken link) are not security reports. Use the public issue templates for
those.

Reports about a participant's conduct and governance enquiries may use the
same private channel described below.

## How to report

1. **Preferred: GitHub private vulnerability reporting.** On the repository
   page open the **Security** tab and choose **Report a vulnerability**. This
   opens a private advisory that only the maintainers can see. Use it for
   privacy problems as well as vulnerabilities.

   This route works only when private vulnerability reporting is enabled in
   the repository settings (Settings, Code security, Private vulnerability
   reporting). Maintainers: it must be enabled for this policy to work. If
   the **Report a vulnerability** button is missing, it is not enabled; use
   the fallback below.

2. **Fallback: ask for a private channel.** Open a minimal public issue that
   says only that you want to report a security or privacy problem and asks
   for a private channel. Include **no details**: no description of the
   problem, no steps, no names, no links to the affected content. A
   maintainer will reply with a private way to send the details.

Do not put the details of a vulnerability or any personal information in a
public issue, pull request, discussion, or commit message. Public issues are
indexed by search engines and are effectively permanent, including their
edit history.

## What to include (in the private report only)

- What you found and where (file, URL, or commit).
- How to reproduce it, or what makes you think it is a problem.
- For a privacy problem: where the information appears. Do not repeat the
  personal information itself more than is needed to locate it.

## What to expect

This project is maintained on a best-effort basis and makes no guaranteed
response time. Reports are read, acknowledged when possible, and fixed in
the default branch; the fix is noted in the changelog without identifying
the reporter unless the reporter asks to be credited. There is no bug
bounty.

If personal information has been posted publicly, removing it from the
current files does not remove it from git history, forks, or search engine
caches. Tell the maintainers as early as possible so that the wider cleanup
can be requested from GitHub.

## Never post real case data

This project describes behavior relevant to threat assessment. It must not
receive information about real cases. Do not post, in any public channel of
this repository: details of a real incident that are not already in
published public sources; names or identifying details of any person
(subjects of concern, victims, witnesses, employees, investigators); open or
recent investigations; or confidential material belonging to an employer or
client. Use fictionalized examples, or cite published public sources.

## Supported versions

Fixes are made on the default branch and published with the next release.
Earlier releases are not patched.
