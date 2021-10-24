Feature: Synchronise by adding new item
    Scenario: Synchronise single tiered directory
        Given Client and server are initialised
        When A file is saved in the client directory
        Then The files are synchronised in the server folder

    Scenario: Synchronise multi tiered directory
        Given Client and server are initialised
        When A file is saved within a folder of the client directory
        Then The files are synchronised in the server folder

    Scenario: Synchronise copied file
        Given Client and server are initialised
        When A file is saved in the client directory
        When The file is copied and pasted in the client directory
        Then The files are synchronised in the server folder
