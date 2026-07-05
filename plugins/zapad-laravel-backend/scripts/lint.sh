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

if [[ -x vendor/bin/phpstan ]]; then
  ERRORS=$(vendor/bin/phpstan analyse "$FILE_PATH" --no-progress --error-format=raw 2>&1)
  if [[ $? -ne 0 ]]; then
    echo "$ERRORS" >&2
    exit 2
  fi
fi

exit 0
