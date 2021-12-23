# Models for KABOOM

NOTE: All records have an ID number

## Comics

**Staff Positions**
- `position`: CharField, required, unique

**Publisher**
- `name`: CharField, required
- `logo`: URLField
- `website`: URLField

**Staff**
- `name`: CharField, required
- `position`: ForeignKey(StaffPositions)
- `image`: URLField
- `date_of_birth`: DateField
- `date_of_death`: DateField
- `biography`: TextField

**Character**
- `name`: CharField, required
- `alias`: CharField
- `image`: URLField
- `biography`: TextField

**Series**
- `series_name`: CharField, required
- `publisher`: ForeignKey(Publisher)
- `summary`: TextField
- `year_started`: IntegerField(1000-9999)
- `status`: CharField, required
- `cover_image`: URLField
- `background_image`: URLField

**Format**
- `name`: CharField, required, unique

**Issue**
- `issue_number_absolute`: IntegerField, required
- `issue_number`: IntegerField, required
- `series`: ForeignKey(Series), required
- `summary`: TextField
- `characters`: ManyToManyField(Characters)
- `staff`: ManyToManyField(Staff)
- `format`: ForeignKey(Format)
- `release_date`: DateField, required
- `cover_image`: URLField

## Cartoons

**Voice Actor**
- `name`: CharField, required
- `image`: URLField
- `date_of_birth`: DateField
- `date_of_death`: DateField
- `biography`: TextField

**Network**
- `name`: CharField, required
- `website`: URLField
- `logo`: URLField

**Genre**
- `genre`: CharField, required, unique

**Series**
- `name`: CharField, required
- `network`: ForeignKey(Network)
- `genres`
- `summary`
- `season_count`
- `genres`
- `genres`