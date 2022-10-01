# Installation #

The Python script is platform independent and requires a Python 3.10 interpreter or higher.
It may be possible to run the script on an older version, though this has not yet been tested
and may cause unwanted or unusual behavior. The script also requires a valid youtube-dl executable
which has to be present in the PATH environment. It is also recommended to have a valid ffmpeg executable
in the PATH environment, as media conversion may fail otherwise.

# User Manual #

### Index Files ###

To get started, you have to create a new download index. A download index is basically nothing more than a simple text file which contains
the URLs that you wish to download, alongside certain instructions which affect where your files are saved etc.; The syntax is as follows:

```
[ROOT Music]

[DIR Beethoven]
fOk8Tm815lE >> Ludwig Van Beethoven - 5th Symphony in C Minor

[DIR Mozart]
k1-TrAvp_xs >> Wolfgang Amadeus Mozart - Lacrimosa
```

This patricular example would first change into the directory `Music`, as set by the `[ROOT Music]` instruction. Below this, we have the instruction `[DIR Beethoven]`,
which will first try to create the directory `Beethoven` in case it doesn't exist yet and after that enter the directory. Following this, we have our first download
instruction. Now, the full URL for our desired video would be `https://www.youtube.com/watch?v=fOk8Tm815lE`, but the script will autofill most of this for us, so we only
have to enter the video ID there. After the ID follows a whitespace and a `>>` arrow, which is pointing towards the file name where we want to save our video. As before,
most of it is autofilled for us, so we don't have to bother with any file extensions. After the downloads for this directory have finished, we return to the root directory
of our index, `Music`, and change to the next directory in the index. This process will be repeated until the end of the index is reached and all files are downloaded.
Now, if we want to add another file to our collection without having to download all the other files again, we can simply do so by commenting out all files we have already
downloaded. There are two types of comments: The line and the block comment. Usually, you would want to use a block comment to directly comment out multiple lines at once.
This would work as follows:

```
[ROOT Music]

/*[DIR Beethoven]
fOk8Tm815lE >> Ludwig Van Beethoven - 5th Symphony in C Minor

[DIR Mozart]
k1-TrAvp_xs >> Wolfgang Amadeus Mozart - Lacrimosa*/

[DIR Touhou]
vS_a8Edde8k >> Night of Nights
UkgK8eUdpAo >> Bad Apple!!
```

Now, everything which is enclosed in the `/* */` symbols is ignored by the downloader. Be carefull to always put the symbols at the beginning and the end of the line or
elsewise the parser might overlook them.

### Script ###

Now that we have created our index file, we can open it in our script. You may either open it directly in the directory where your index is located, or you may also use
the `?cd` command to navigate through your folder structure. Whatever option you choose, as soon as you are in the directory where your index file lies, you can simply
open it by entering the file name into the prompt. You will be asked if the index that has been parsed by the script is correct and does not contain any errors, and if
you want to continue downloading the files in the index. If you don't find any issues, you can simply hit `Y` on your keyboard and the script will start downloading.
Depending on the size of your index, this may take a while and consume a large amount of ressources, so you may sit back for a few minutes and let the program finish
it's job. After the script displays that all downloads have finished, you can exit the window by simply hitting the X on the top or by entering `?exit` into the prompt.
