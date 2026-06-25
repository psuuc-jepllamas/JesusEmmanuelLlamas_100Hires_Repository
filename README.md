## My Task Summary

---

### What Tools I Installed

I installed the following:

- Cursor IDE
- Claude Code add-on in Cursor
- Codex add-on in Cursor

---

### What Steps I Completed

1. Install Cursor IDE — [https://cursor.com/](https://cursor.com/)

   *Status: Completed*

2. Add the Claude Code add-on in Cursor (Extensions → search "Claude Code") and log in to it.

   *Status: Completed*

3. Add the Codex add-on in Cursor (Extensions → search "Codex") and log in to it.

   *Status: Completed*

4. Create a public GitHub repository (if you don't have a GitHub account yet, create one at [https://github.com/](https://github.com/))

   *Status: Completed*

5. Open the repository in Cursor

   *Status: Completed*

6. Create a README.md file that describes what tools I installed, what steps I completed, and what issues I ran into and how I solved them.

   *Status: Completed*

7. Commit and push to GitHub

   *Status: Completed*

8. Reply to this email with the link to your README.md file on GitHub

   *Status: Completed*

---

### What Issues I Ran Into and How I Solved Them

**Claude Code**

- I searched Google on how to log in at Claude Code at Cursor IDE.
- When I tried to log in using the command: `claude`, an error shows at my terminal:

```
claude: The term 'claude' is not recognized as the name of a cmdlet, function, script file,
or operable program. Check the spelling of the name, or if a path was included, verify that
the path is correct and try again.
At line:1 char:1 + claude + ~~~~~ + CategoryInfo : ObjectNotFound: (claude:String) [],
CommandNotFoundException + FullyQualifiedErrorId : CommandNotFoundException
```

- Google said that "The term 'claude' is not recognized" means that the package is not yet installed. It provided me with this command: `npm install -g @anthropic-ai/claude-code`. This resolved the issue and I successfully logged in.

**Codex**

- I also searched Google on how to log in at Codex at Cursor IDE.
- When I tried to log in using the command: `codex`, an error shows at my terminal:

```
codex: The term 'codex' is not recognized as the name of a cmdlet, function, script file,
or operable program. Check the spelling of the name, or if a path was included, verify that
the path is correct and try again.
At line:1 char:1 + codex login + ~~~~~ + CategoryInfo : ObjectNotFound: (codex:String) [],
CommandNotFoundException + FullyQualifiedErrorId : CommandNotFoundException
```

- Google also said "The term 'codex' is not recognized" means that the package is not yet installed. It provided me with this command: `npm install -g @openai/codex`. This resolved the issue and I successfully logged in.

---

## Research: AI-Powered SEO Content Production

### Topic

**AI-Powered SEO Content Production for B2B SaaS**

This topic was chosen because it sits at the intersection of AI tools, content strategy, and measurable business outcomes — relevant skills for a junior marketing specialist role in a modern SaaS environment.

---

### What I Collected

| Type | Count |
|------|-------|
| Experts identified | 10 |
| LinkedIn posts collected | 15 |
| YouTube transcripts collected | 27 |
| Other | 2 |

All collected materials are organized in the `/research` folder:

- `/research/sources.md` — full list of experts with links and annotations
- `/research/linkedin-posts/` — posts organized by author
- `/research/youtube-transcripts/` — transcripts organized by channel
- `/research/other/` — additional materials (newsletters, articles)

---

### The 10 Experts and Why I Chose Them

| # | Name | Role | Why I Chose Them |
|---|------|------|-----------------|
| 1 | **Tim Soulo** | CMO, Ahrefs | Published a 1B+ data point study on AI search optimization (June 2026). Data-driven practitioner. |
| 2 | **Michał Suski** | Co-founder, Surfer SEO | Built an AI SEO tool from the ground up. Teaches workflows from direct product experience. |
| 3 | **Kyle Roof** | Independent SEO | Known for scientific split-testing of SEO factors. Process-oriented and measurable. |
| 4 | **Eli Schwartz** | Author, Product-Led SEO | Consults B2B SaaS companies on SEO. Focuses on intent-driven content over keyword chasing. |
| 5 | **Ryan Law** | Director of Content Marketing, Ahrefs | Publishes tactical content strategy frameworks specifically for B2B SaaS companies. |
| 6 | **Kevin Indig** | Independent, Ex-Shopify/G2 | Posts AI + SEO frameworks from enterprise-level experience. Runs a newsletter on SaaS growth. |
| 7 | **Aleyda Solis** | Founder, Orainti | International SEO consultant. Frequently covers AI tools in real client workflows. |
| 8 | **Bernard Huang** | Co-founder, Clearscope | Built an AI content grading tool. Publishes real content production workflows. |
| 9 | **Koray Tuğberk GÜBÜR** | Independent SEO | Deep technical SEO with focus on semantic content architecture and AI-assisted production. |
| 10 | **Lily Ray** | VP of SEO Strategy, Amsive | Known for E-E-A-T and AI content quality research. Studies how Google and AI systems evaluate content. |

---

### Selection Criteria

Experts were selected based on:

- **Practitioner-first** — they actively build or run AI SEO workflows, not just write about them
- **B2B SaaS relevance** — their content applies directly to SaaS content production
- **Recent activity** — all were publishing content in 2025–2026
- **Platform diversity** — mix of LinkedIn, YouTube, and newsletter sources

---

I also added scripts for transcripting YouTube videos and blog websites.
- **YouTube Transcript API** — youtube-transcript-api
- **Blog Website Transcript API** — trafilatura
