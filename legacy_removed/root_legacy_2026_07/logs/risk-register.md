# Risk Register

Use this file for risks that should stay visible across AI workflow sessions.

| Date | Risk | Impact | Control | Status |
| --- | --- | --- | --- | --- |
| 2026-07-06 | `templates/` conflicts with existing Obsidian `Templates/` on Windows. | Adding repo templates there could modify vault template content. | Do not write there until Zhuan chooses a separate path or approves vault edits. | Open |
| 2026-07-06 | Agents may accidentally touch `D:\Zhuan_Vault` or Obsidian files. | Data loss, unwanted note edits, or privacy exposure. | Keep vault policy explicit in docs and prompts. | Open |
