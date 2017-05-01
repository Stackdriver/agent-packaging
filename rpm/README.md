agent-rpm
=========

Packaging for the Stackdriver agent on RPM based distributions.  The box used for
building is expected to be set up by the rpmbuild puppet class which includes the
basics that you need on the host.

Once that's done, you can do builds using the makefile targets to do local testing
of your build changes.  Once you're ready, you can commit the changes and update
collectd.spec with an updated release field and changelog entry and then go and do
a "real" build in jenkins which will update the repo on testrepo.stackdriver.com

Once you've tested those packages, you can use the 'stack publish_repo' command to
publish the changes to the primary repo.