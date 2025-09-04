# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Initial setup of the project.
- Added CLI for automating daily permit tasks.

## [0.1.7] - 2025-09-03

### Added
- Option `--wait-seconds` or `-w` for seconds to implicitly wait for an HTML element to be found.

### Changed
- The default seconds to implicitly wait is increased from `1` to `2` seconds.

## [0.1.5] - 2024-01-27

### Added
- Option `--today` or `-t` to purchase parking permit for today's date.

## [0.1.3] - 2024-11-23

### Added
- Option `--version` or `-v` to print CLI version

### Changed
- Update `dataclass-wizard` dependency to `v0.29.0`
- Add new custom nested path support in `dataclass-wizard`!

## [0.1.1] - 2024-11-07

### Changed
- Don't zero pad the day of month on calendar selection,
  because otherwise Selenium seems to crash.

### Fixed
- Fixed issue with calendar day selection, when date (day of month) was a single digit.

## [0.1.0] - 2024-10-16
### Added
- Basic functionality for daily permit automation.
- Add CLI tool and commands:
  - `gmu c` to configure and get set up.
  - `gmu sc` to show config.
  - `gmu dp` for purchasing daily permits.

### Changed
- Refactored code for better readability.

### Fixed
- Fixed issue with date parsing in permit generation.

