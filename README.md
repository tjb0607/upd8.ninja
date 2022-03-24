# upd8.ninja

Interfaces with homestuck\_update\_bot to make the best upd8 checker possible.

## website

https://tjb0607.me/upd8

## API

Version 0.1 uses javascript function calls stored in a file called check.js to tell whether or not there's an update and when the next update will likely be.

check.js is modified by homestuck\_update\_bot when it finds an upd8, and will show the upd8's info for 10 minutes until it's reverted back to the usual shownoupd8.

The syntax is as follows:

    shownoupd8([approx next upd8 time in seconds since UNIX epoch]);

or if there has been an upd8 in the last 10 minutes:

    showupd8(<page number>, <page title (escaped for HTML)>, <number of pages in the upd8>);

additionally, homestuck\_update\_bot stores the current latest page number in a file called 'latestpage.txt'. This isn't used by the webpage (yet), but is used by the popular MSPANotify Windows program.

## roadmap

* Ability to keep track of new pages across visits, or when the user's internet is down for over 10 minutes.

* (Version 0.2) Use json files instead of a js file directly executing code from a script, and also completely rework the system from one that changes a file for 10 minutes to one that locally keeps track of what the latest page number is, and then fetches the title of the first unread page when an upd8 is found.

* Better options, including ability to hide number of pages
