These directories contain Dockerfiles for the Stackdriver Monitoring agent build
containers on various OS distros. These build containers are based on the
respective Linux distro base images, so the Monitoring agent Linux package
builds can detect the distribution they are invoked in, and link against the
correct dependent libraries.  The containers provide hermetic environments for
the various distros supported by the agent, with preinstalled and preconfigured
dependencies to speed up the builds and make them reproducible.
