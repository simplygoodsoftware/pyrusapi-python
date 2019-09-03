# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.21.0] - 2019-09-03
### Added
- support sending comments to external channel (email)

## [1.19.0] - 2019-05-16
### Added
- This CHANGELOG file.
- Return decimal_places for form field number.
- added scheduling task to date with utc time.
- fill step number for form task approvals

### Changed
- Fixed FormField serialization. You can now copy all fields from TaskResponse change some of them and pass to the TaskCommentRequest.
- Fixed parsing filename from Content-Disposition header on file download.
- Fixed creation_date field value.
