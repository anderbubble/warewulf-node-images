# Red Hat Enterprise Linux from the Universal Base Image (UBI)

The Red Hat Universal Base Image (UBI) is freely redistributable, but it only
includes the UBI repositories, which are a subset of RHEL. This example builds
a Warewulf node image from a UBI base while installing the full RHEL package
set, by reusing the build host's Red Hat subscription (from either the Red Hat
CDN or a Red Hat Satellite server).

On a host registered with `subscription-manager`, podman and buildah
automatically expose the host's subscription to the build, and the
subscription-manager dnf plugin (running in "container mode") generates
`/etc/yum.repos.d/redhat.repo` inside the build. The `Containerfile` then
removes the overlapping `ubi.repo`, pins `$releasever`, enables the subscribed
repositories, and installs the desired packages.

```
podman build . --tag rhel:9
```

If your host does not expose the subscription automatically, mount the relevant
files in (as in the [`rhel-9`](../rhel-9) example):

```
podman build \
    --volume=/etc/pki/entitlement:/run/secrets/etc-pki-entitlement:ro \
    --volume=/etc/rhsm:/run/secrets/rhsm:ro \
    --volume=/etc/yum.repos.d/redhat.repo:/run/secrets/redhat.repo:ro \
    . --tag rhel:9
```

For more information, see https://access.redhat.com/solutions/5870841.

## Release version

Set `--build-arg RELEASEVER=...` to match your subscription's release version.
This is set explicitly because the UBI image's own `$releasever` may differ
from the value used in the `baseurl` of `redhat.repo` (e.g. `9.4` vs `9`),
which would otherwise point dnf at the wrong repository URLs.

```
podman build . --build-arg RELEASEVER=9.4 --tag rhel:9.4
```

## Caveats

* This example uses the full `ubi` base image, which includes `dnf`. The
  `ubi-minimal` image ships only `microdnf`, so building from it would first
  require `microdnf install dnf`.

* If your repositories are "snapshots" (version-frozen, as with Red Hat
  Satellite), choose a UBI image whose own repositories are **older than or as
  current as** the snapshot. Otherwise packages already present in the UBI base
  may be downgraded during the build.
