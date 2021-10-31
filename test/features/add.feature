Feature: Detection and saving of new files
    Scenario: Synchronise single tiered directory
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

   Scenario: Synchronise multi tiered directory
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A file is saved within a folder of the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

    Scenario: Synchronise copied file
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A file is saved in the client directory
        When The file is copied and pasted in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined