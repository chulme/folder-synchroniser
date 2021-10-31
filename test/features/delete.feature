Feature: Detection and removal of an existing item
    Scenario: Synchronise directories when a file is removed
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A synchronised file is removed from the client directory
        Then The files is deleted in the server folder
        Then Concurrent threads are joined
