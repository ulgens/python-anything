FROM docker/sandbox-templates:opencode@sha256:d2c2028650a7703338b124132a28e70c790f053435de2b3de8a76c4dc67736e2

USER root

# Install uv & Python
COPY --from=ghcr.io/astral-sh/uv:0.10.10@sha256:cbe0a44ba994e327b8fe7ed72beef1aaa7d2c4c795fd406d1dbf328bacb2f1c5 /uv /uvx /bin/

# FIXME:
#   3.14.3 install raises
#   > error: No download found for request: cpython-3.14.3-linux-aarch64-gnu
RUN uv python install 3.14.2

# Install ocx & plugins
RUN curl -fsSL https://ocx.kdco.dev/install.sh | sh
RUN ocx init
# RUN ocx add kdco/workspace --from https://registry.kdco.dev

# Plugins to check:
# - https://github.com/kdcokenny/opencode-workspace
# - https://github.com/vtemian/micode
# - https://github.com/vtemian/octto
# - https://github.com/spoons-and-mirrors/subtask2
# - https://github.com/backnotprop/plannotator/tree/main/apps/opencode-plugin
# - https://github.com/kdcokenny/opencode-notify
# - https://github.com/mohak34/opencode-notifier
# - https://github.com/panta82/opencode-notificator
# - https://github.com/JRedeker/opencode-morph-fast-apply

USER agent
