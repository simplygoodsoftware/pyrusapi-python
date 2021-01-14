# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.30.0] - 2021-01-14
### Added
- get/add/update roles
- get profile

## [1.29.0] - 2020-11-16
### Added
- 'DepartmentId' and 'DepartmentName' properties in entity of 'Person' in 'contacts' response

## [1.28.0] - 2020-11-09
### Added
- 'DeletedOrClosed' property in GetForm response

## [1.27.0] - 2020-10-27
### Added
- support for reading and writing subscribers in task comments

## [1.26.1] - 2020-06-26
### Changed
- bugfix

## [1.26.0] - 2020-06-26
### Added
- new external source channels

## [1.25.0] - 2020-04-17
### Added
- support for reading and writing spent time in task comments

## [1.24.0] - 2020-04-16
### Added
- support for attaching files by id or by url

## [1.23.0] - 2019-10-24
### Added
- support for reading and writing multiple values in catalog field
- root_id for files with version

## [1.22.0] - 2019-09-04
### Added
- allow to write value to catalog field by id or by name

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
