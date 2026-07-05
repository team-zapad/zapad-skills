#!/bin/bash
# ponytail: per-file check only, not project-wide — the real gate is
# `new-feature` skill's step 11 (run Pint/Larastan/tests for the whole
# domain before calling a feature done). This just catches drift early.

FILE_PATH=$(jq -r '.tool_input.file_path // empty' 2>/dev/null)
[[ "$FILE_PATH" == *.php && -f "$FILE_PATH" ]] || exit 0

cd "${CLAUDE_PROJECT_DIR}" 2>/dev/null || exit 0

if [[ -x vendor/bin/pint ]]; then
  vendor/bin/pint "$FILE_PATH" >/dev/null 2>&1
fi

# Controller <-> Action mirror (project-structure "golden rule": Actions/{Domain}
# mirrors Controllers/{Domain} 1:1). Checks the mirrored *domain folder* exists,
# not an exact filename — the controller and action verbs legitimately differ
# (StoreProductQuestionnaireController <-> SaveProductQuestionnaire). Warn-only:
# never blocks, since an action-less route-model-bound controller is valid.
case "$FILE_PATH" in
  */app/Http/Controllers/*Controller.php)
    REL=${FILE_PATH##*/app/Http/Controllers/}; MIRROR_ROOT="app/Actions"; MIRROR_KIND="Action" ;;
  */app/Actions/*.php)
    REL=${FILE_PATH##*/app/Actions/}; MIRROR_ROOT="app/Http/Controllers"; MIRROR_KIND="Controller" ;;
  *)
    REL="" ;;
esac
if [[ -n "$REL" && "$REL" == */* ]]; then
  DOMAIN_DIR=${REL%/*}
  if ! ls "${MIRROR_ROOT}/${DOMAIN_DIR}"/*.php >/dev/null 2>&1; then
    echo "warning: ${REL} has no matching ${MIRROR_KIND} in ${MIRROR_ROOT}/${DOMAIN_DIR}/ — project-structure golden rule: Actions/{Domain} mirrors Controllers/{Domain} 1:1." >&2
  fi
fi

if [[ -x vendor/bin/phpstan ]]; then
  ERRORS=$(vendor/bin/phpstan analyse "$FILE_PATH" --no-progress --error-format=raw 2>&1)
  if [[ $? -ne 0 ]]; then
    echo "$ERRORS" >&2
    exit 2
  fi
fi

exit 0
