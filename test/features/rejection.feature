Feature: The client rejects significantly large files
    Scenario: The client is given a large file, but it is too large to send.
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A large file is saved in the client directory
        Then The file is not synchronised with the server
        Then Concurrent threads are joined
