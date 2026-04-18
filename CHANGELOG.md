# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [1.3.0] - 2026-04-19

### Added
- Enhanced README with better formatting, badges, and detailed usage instructions
- Improved pyproject.toml with comprehensive classifiers, optional dependencies, and tool configurations
- Added CHANGELOG.md to track project changes
- Added development dependencies (black, ruff, mypy) for code quality
- Added documentation and repository URLs to project metadata

### Changed
- Updated development status from "4 - Beta" to "5 - Production/Stable"
- Expanded keywords for better discoverability
- Improved regex pattern documentation in README
- Enhanced troubleshooting section with platform-specific clipboard instructions
- Updated usage examples with clearer explanations

### Fixed
- Fixed clipboard detection logic for better reliability
- Improved error handling for edge cases
- Enhanced cross-platform compatibility notes

## [1.2.0] - 2026-03-15

### Added
- Support for Wayland clipboard via wl-clipboard
- Improved regex pattern to handle more variations
- Added --version flag
- Added test_manual.py for manual smoke testing

### Changed
- Refactored code for better readability
- Updated installation instructions
- Improved summary output formatting

## [1.1.0] - 2026-02-01

### Added
- File input support (-f/--file)
- File output support (-o/--output)
- Screen output support (--screen)
- Additive flag system

### Changed
- Changed default behavior to clipboard-only for simplicity
- Updated documentation to reflect new features

## [1.0.0] - 2026-01-15

### Added
- Initial release
- Basic clipboard-to-clipboard functionality
- Regex-based Coursera boilerplate removal
- MIT license