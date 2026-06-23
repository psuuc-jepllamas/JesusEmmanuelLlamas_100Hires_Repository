--**My task summary**--

• **What tools I installed**:

I installed the following:

- Cursor IDE
- Claude Code add-on in Cursor
- Codex add-on in Cursor

• **What steps I completed**:

1. Install Cursor IDE — [https://cursor.com/](https://cursor.com/)

-*Status: Completed*-

2. Add the Claude Code add-on in Cursor (Extensions → search "Claude Code") and log in to it.

-*Status: Completed*-

3. Add the Codex add-on in Cursor (Extensions → search "Codex") and log in to it.

-*Status: Completed*-

4. Create a public GitHub repository (if you don't have a GitHub account yet, create one at [https://github.com/](https://github.com/))

*Status: Completed

5. Open the repository in Cursor

-*Status: Completed*-

6. Create a README.md file that describes:

— What tools you installed

— What steps you completed

— What issues you ran into and how you solved them

-*Status: Completed*-

7. Commit and push to GitHub

-*Status: Completed*-

8. Reply to this email with the link to your README.md file on GitHub

-*Status: Completed*-

• **What issues you ran into and how I solved them**:

**Claude Code**

- I searched Google on how to log in at Claude Code at Cursor IDE.
- When I tried to log in using the command: claude, an error shows at my terminal:

claude: The term 'claude' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
At line:1 char:1 + claude + ~~~~~ + CategoryInfo : ObjectNotFound: (claude: String) [], CommandNotFoundException + FullyQualifiedErrorId : CommandNotFoundException

- Google said that "The term 'claude' is not recognized" this means that a package named claude is not yet installed in my computer. It provided me with this command: npm install -g @anthropic-ai/claude-code. This resolved the issue and I successfully logged in.

**Codex**

- I also searched Google on how to log in at Codex at Cursor IDE.
- When I tried to log in using the command: codex, an error shows at my terminal:

codex: The term 'codex' is not recognized as the name of a cmdlet, function, script file, or operable program. Check the spelling of the name, or if a pain was included, verify that the path is correct and try again.
At line:1 char:1 + codex login + ~~~~~ + CategoryInfo : ObjectNotFound: (codex:String) [], CommandNotFoundException + FullyQualifiedErrorId : CommandNotFoundException

- Google also said "The term 'codex' is not recognized" this means that a package named codex is not yet installed in my computer. It provided me with this command: npm install -g @openai/codex. This resolved the issue and I successfully logged in.
