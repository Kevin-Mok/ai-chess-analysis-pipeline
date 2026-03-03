# README Prompt for Chess Highlights

Use this prompt with ChatGPT/Codex to generate or refresh your `README.md` from your highlight game files.

```text
You are writing a GitHub README for my chess highlights repository.

Goal:
- Create a clean, concise, personal README that showcases my best games and key moves.
- Keep the tone practical and confident (not cheesy).

Repository files to use:
- games/2026-02-27-fast-checkmate.pgn
- games/2026-03-03-comeback-vs-gaju33333.pgn
- media/2026-03-03-lichess-comeback.gif

Requirements:
1. Output valid Markdown only.
2. Start with title: "Chess Highlights".
3. Include sections:
   - Overview
   - Highlight Games
   - Key Moves and Turning Points
   - Study/Analysis Links
   - How to View the Games
4. In "Highlight Games", provide a table with:
   - Date
   - Opponent
   - Platform
   - Result
   - Why it matters (1 sentence)
5. In "Key Moves and Turning Points", include 2-4 concrete move references in algebraic notation from the PGNs (for example: "15. Qxe7#").
6. Reference the GIF as a visual highlight and include Markdown image syntax.
7. End with a short "Next goals" bullet list (3 bullets max).
8. Keep the README under 250 words.
9. Do not invent games or links; only use data present in the files.

Return only the final README markdown.
```

Optional follow-up prompt:

```text
Now generate a second README version optimized for recruiters: emphasize improvement, comeback resilience, and consistent study habits.
```
