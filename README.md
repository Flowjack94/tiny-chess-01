# tiny-chess-01

A compact chess engine in at most 4,096 bytes of Python. It plays the
house gauntlet through the env at MAKEFUN_ENV_URL: alpha-beta search to a
fixed node budget with quiescence, MVV-LVA move ordering and a
material + piece-square evaluation. Deterministic: fixed node count,
no clock, no randomness.
