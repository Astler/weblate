# Weblate Community UI, first implementation slice.
# Exact upstream Docker release tag (not rolling latest/monthly tag).
# The upstream source templates were inspected at weblate-2026.10.1.
# Runtime compatibility remains unverified without Docker/browser execution.
ARG WEBLATE_BASE=weblate/weblate:2026.10.1.2
FROM ${WEBLATE_BASE}

USER root
COPY overlay/ /opt/community-ui/overlay/
RUN set -eu; \
    pkg="$(/app/venv/bin/python -c 'import importlib.util; print(next(iter(importlib.util.find_spec("weblate").submodule_search_locations)))')"; \
    test -f "$pkg/templates/snippets/meta-css.html"; \
    test -d "$pkg/static"; \
    cp -R /opt/community-ui/overlay/templates/. "$pkg/templates/"; \
    cp -R /opt/community-ui/overlay/static/. "$pkg/static/"; \
    chmod -R a+rX "$pkg/static/community-ui"; \
    rm -rf /opt/community-ui
USER 1000
# Preserve all of the upstream entrypoint, healthcheck, cache/data volumes and CMD.
