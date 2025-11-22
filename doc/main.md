# User Journey

1. User opens the app
2. User types the values of v1, v2 and v3, adds new rows and cols when needed.
3. user clicks calculate
  - User triggers is_calculated, it won't show new window when its already calculated
  - Note: when users type something different in the fields, the is_calculated will be reset
4. It'll show the final output

Errors:
1. ValueError(when user types not number in any or all the fields)
