Feature: Synchronise by adding new item
    Scenario: Synchronise single tiered directory
        Given Client and server are ran concurrently
        When A file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

    Scenario: Synchronise multi tiered directory
        Given Client and server are ran concurrently
        When A file is saved within a folder of the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

    Scenario: Synchronise copied file
        Given Client and server are ran concurrently
        When A file is saved in the client directory
        When The file is copied and pasted in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined
