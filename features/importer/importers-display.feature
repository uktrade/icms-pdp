Feature: Importer Display

    @importer @display @importer-display
    Scenario: User with refdata permission should be able to view importer in the importer list
        Given importer "Elm Street Imports" exists
        Given "Roy" is logged in
        And "Roy" has permission "reference_data_access"
        When "Roy" navigates to "importer-list"
        Then importer "Elm Street Imports" is in the list

    @importer @display @importer-display
    Scenario: User should see importer details when importer name is clicked
        Given import organisation "Elm Street Imports" exists
        And "John" is logged in
        And "John" has permission "reference_data_access"
        When "John" navigates to "importer-list"
        And  clicks on importer name "Elm Street Imports"
        Then "importer-view" page for importer "Elm Street Imports" is displayed
        And context header reads "View Importer - Elm Street Imports"
        And importer name reads "Elm Street Imports"

    @importer @display @importer-display
    Scenario: User should be able to navigate back
        Given importer "Elm Street Imports" exists
        And "Ashley" is logged in
        And "Ashley" has permission "reference_data_access"
        When "Ashley" views importer "Elm Street Imports"
        And  clicks on the back link
        Then "importer-list" page is displayed

    @importer @display @importer-display
    Scenario: User should see correct importer name
        Given import organisation "Elm Street Imports" exists
        And "bren" is logged in
        And "bren" has permission "reference_data_access"
        When "bren" views importer "Elm Street Imports"
        Then importer details read as follows
            | Field    | Value              |
            | Type     | Organisation       |
            | Name     | Elm Street Imports |
            | Comments |                    |

    @importer @display @importer-display
    Scenario: User should see correct importer region origin
        Given non-European importer "US Imports" exists
        And "bren" is logged in
        And "bren" has permission "reference_data_access"
        When "bren" views importer "US Imports"
        Then importer details read as follows
            | Field         | Value        |
            | Name          | US Imports   |
            | Region origin | Non-European |
            | Comments      |              |

    @importer @display @importer-display
    Scenario: User should see correct importer offices
        Given importer "Hey Ltd" exists
        And importer "Hey Ltd" has an office with address "1428 Elm Street" and postcode "43001"
        And "bren" is logged in
        And "bren" has permission "reference_data_access"
        When "bren" views importer "Hey Ltd"
        Then importer offices read as follows
            | Row | Field     | Value           |
            | 1   | Address   | 1428 Elm Street |
            | 1   | Post Code | 43001           |
            | 1   | ROI       | None            |
        And no archived importer office is displayed

    @importer @display @importer-display
    Scenario: User should see correct importer agents
        Given import organisation "Hey Ltd" exists
        And import organisation "Subcorp" exists
        And importer "Subcorp" has an office with address "4 Beverly Hills" and postcode "90210"
        And "Subcorp" is an agent of "Hey Ltd"
        And user "Jane-user" exists with title "Ms" and first name "Jane" and last name "Doe"
        And individual importer "Jane-importer" exists with user "Jane-user"
        And importer "Jane-importer" has an office with address "1428 Elm Street" and postcode "43001"
        And "Jane-importer" is an agent of "Hey Ltd"
        And "Ashley" is logged in
        And "Ashley" has permission "reference_data_access"
        When "Ashley" views importer "Hey Ltd"
        Then importer agents read as follows
            | Row | Field                                | Value                    |
            | 1   | Importer Name / Importer Entity Type | Subcorp\s+Organisation   |
            | 1   | Agent Type                           | Care Of Importer         |
            | 1   | Address                              | 4 Beverly Hills\s+90210  |
            | 2   | Importer Name / Importer Entity Type | Ms Jane Doe\s+Individual |
            | 2   | Agent Type                           | Care Of Importer         |
            | 2   | Address                              | 1428 Elm Street\s+43001  |
        And no archived importer agents are displayed

    @importer @display @importer-display
    Scenario: User should see correct contacts
        Given importer "Hey Ltd" exists
        And user "thecat" exists
        And "thecat" is a contact of importer "Hey Ltd"
        And "bren" is logged in
        And "bren" has permission "reference_data_access"
        When "bren" views importer "Hey Ltd"
        Then importer contacts table read as follows
            | Header                     | Contact            |
            | Central Contact Details    | thecat@example.com |
            | View Applications/Licences |                    |
            | Edit Applications          |                    |
            | Vary Applications/Licences |                    |

    @importer @display @importer-display
    Scenario: User should see no contact
        Given importer "Hey Ltd" exists
        And "bren" is logged in
        And "bren" has permission "reference_data_access"
        When "bren" views importer "Hey Ltd"
        Then text "There isn't anyone in this team" is visible
