# Note to the developers

## Description of the architecture
* multiplanner
* presentation
* User <https://docs.djangoproject.com/fr/2.1/ref/contrib/auth/>
* username (mandatory)
* first_name
* last_name
* email
* password
* user_merpissions
* is_staff
* ...
* relationships
* Friendships
* user
* friend_list
* invited_list
* SecreteMark
* user
* marked_user
* mark
* groups
* Group
* name
* members
* transactions
* accounting
* SharedAccount
* name
* members
* Transaction
* motive
* date
* payer
* amount
* beneficiaries
* agenda
* TimeRange
* date
* duration
* Event
* date
* place
* creator
* attendees
* invited
* transactions
* MeetingRules
* minimum_delay
* maximum_delay
* duration
* possible_time_ranges
* creator
* administrators

## Explainations
A shared account is for a group of people that pay together.

It is possible to create multiple groups with exactly the same users. Should the users choose the same name for the groups, they would have difficulty differentiating them, but it's their problem after all

Friendships are symmetrical. If status = 1, then there are two entries: (User1 User2 and User2 User1). Else, there is only one entry and User1 is the one who asked for the friendship.

Each event is linked to exactly one Group, the Group of attendees. Each Group of attendees correspond to exactly one event.

When a User joins an Event, each User who already made a transaction in the group
