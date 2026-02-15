## [1.7.0] - 2024-02-12

### Added
- **Smart Token Estimation**: Added approximate token count (~4 chars/token) and file size percentage next to every file and folder in the tree view.
- **Recursive Directory Stats**: Parent folders now show the cumulative size and token count of their contents.
- **Enhanced Tree Visualization**: Replaced simple indentation with proper ASCII tree branches (`├──`, `└──`, `│`) for better readability.
- **CLI Links**: Added links to Documentation, Repository, and Issues in the `--help` output.

### Changed
- **React/JS Optimization**: Automatically ignores `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, and mobile build folders (`ios/`, `android/`) to save tokens.
- **Self-Exclusion Logic**: DeepBase now strictly ignores any existing file named `llm_context.md` (or the specified output name) in the target directory to prevent data duplication.

### Fixed
- Fixed an issue where previous context files were included in the analysis, doubling the token count.