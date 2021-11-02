Feature: Detection and saving of different file types
    Scenario: Synchronise .mp4 files
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A .mp4 file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

   Scenario: Synchronise .avi files
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A .avi file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

    Scenario: Synchronise .mov files
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A .mov file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

    Scenario: Synchronise .jpg files
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A .jpg file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

    Scenario: Synchronise .tiff files
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A .tiff file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

    Scenario: Synchronise .png files
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A .png file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

    Scenario: Synchronise .mp3 files
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A .mp3 file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

    Scenario: Synchronise .wav files
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A .wav file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined
    
    Scenario: Synchronise .pdf files
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A .pdf file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

    Scenario: Synchronise .docx files
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A .docx file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined

    Scenario: Synchronise .xlsx files
        Given Source-destination folders are created
        Given Client and server are ran concurrently
        When A .xlsx file is saved in the client directory
        Then The files are synchronised in the server folder
        Then Concurrent threads are joined
