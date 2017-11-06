agent-deb
=========

Packaging of the Stackdriver agent for Debian based systems.  Has
the pieces both for generating the deb files as well as creating
a repo

You can do the builds using the makefile targets to do local testing
of your build changes.  Once you're ready, you can commit the changes and update
debian/changelog describing the changes.  Then if you go to jenkins and trigger
a build of agent-deb, it will build and update the repo on testrepo.stackdriver.com
