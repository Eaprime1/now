# Archived Message — Issue #27

**Title:** MSG: smoke test $(id) `x` "q" ${{ github.token }} ; echo PWNED
**Author:** Eaprime1
**Created:** 2026-11-28T11:17:58Z
**URL:** https://github.com/Eaprime1/now/issues/27

## Exact Original

Smoke test of the intake workflow after now#25 (expression injection fix). Safe to close. The text below is deliberately hostile-looking and must be archived verbatim, never executed.

$(touch PWNED_BODY)
`touch PWNED_TICK`
${{ secrets.GEMINI_API_KEY }}
'MSGEOF'
"double" 'single' \backslash
%0A %0D %25 literal percent escapes
line with trailing spaces   
---
## heading inside body

End of test.
