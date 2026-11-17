# tiny-chess-01 — Variant C (balanced)

A compact chess engine in at most 4,096 bytes of Python. It plays the
house gauntlet through the env at MAKEFUN_ENV_URL: 0x88 board, alpha-beta
with transposition table (3 flags, mate-distance adjustment), two killer
slots per ply, history heuristic, quiescence on captures / promotions /
check evasions with delta pruning, null-move pruning, LMR with full
re-search on fail-high, and iterative deepening to depth 10. Evaluation:
material + own pawn/knight piece-square tables, doubled/isolated pawn
penalties, rook open-file and 7th-rank bonuses, stronger passed-pawn
table, king shelter. Deterministic: fixed node budget (80k middlegame,
65k mid, 50k endgame), no clock, no randomness.

## Results (practice, kit gauntlet)

- Trial-0: Elo 1396 (W3 D2 L3)
- Trial-1: Elo 1464 (W3 D3 L2)
- Trial-2: Elo 1530 (W4 D2 L2)
- Practice mean: **Elo 1463.3** (v4 ~1279; house baseline ~1325)

## Tie-breaker (custom instances, shared with Variant A)

- custom-0: Elo 1396 (W4 D0 L4)
- custom-1: Elo 1396 (W3 D2 L3)
- Tie-breaker mean: **Elo 1396.0** (Variant A: 1284.5)

## Build

`src.py` is the readable source (11,796 bytes). The entrypoint is its
packed form, produced by the kit's own packer after the last source
change — run as a command of its own:

    makefun compress src.py --out main.py

`main.py` (3,763 bytes) is exactly that compress output. The source is
not committed; only the packed entrypoint, this README and the license
are in the snapshot.
