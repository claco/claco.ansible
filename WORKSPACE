workspace(name = "claco_ansible")

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

http_archive(
  name = "io_bazel_rules_docker",
  sha256 = "dc97fccceacd4c6be14e800b2a00693d5e8d07f69ee187babfd04a80a9f8e250",
  strip_prefix = "rules_docker-0.14.1",
  urls = ["https://github.com/bazelbuild/rules_docker/releases/download/v0.14.1/rules_docker-v0.14.1.tar.gz"],
)

git_repository(
  name = "distroless",
  remote = "https://github.com/GoogleContainerTools/distroless",
  commit = "fd0d99e8c54d7d7b2f3dd29f5093d030d192cbbc",
  shallow_since = "1582213526 -0500"
)

load(
    "@distroless//package_manager:package_manager.bzl",
    "package_manager_repositories",
    "dpkg_src",
    "dpkg_list"
)

package_manager_repositories()

dpkg_src(
  name = "debian_base",
  arch = "amd64",
  distro = "buster",
  sha256 = "889681a6f709a3872833643a2ab28aa5bf4839ec5a8994cd4382f179a6521c63",
  snapshot = "20200308T150748Z",
  url = "http://snapshot.debian.org/archive"
)

dpkg_list(
  name = "package_bundle",
  packages = [
    "ansible",
    "ansible-lint",
    "python3-jinja2",
    "python3-markupsafe",
    "python3-pathspec",
    "python3-pkg-resources",
    "python3-ruamel.yaml",
    "python3-setuptools",
    "python3-six",
    "python3-yaml",
    "yamllint"
  ],
  sources = [
    "@debian_base//file:Packages.json"
  ]
)

load("@io_bazel_rules_docker//repositories:repositories.bzl", container_repositories = "repositories")

container_repositories()

load("@io_bazel_rules_docker//repositories:deps.bzl", container_deps = "deps")

container_deps()

load("@io_bazel_rules_docker//container:container.bzl", "container_pull")

container_pull(
  name = "python_base",
  registry = "gcr.io",
  repository = "distroless/python3",
  digest = "sha256:ea01cb37b865764175854e62f286920fbbf7945e3933a6a5a4f248755619132c"
)
