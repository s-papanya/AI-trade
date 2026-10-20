# AI-trade

Python auto-trading starter with automatic relearn and optimization.

## What it does
- Runs an automated trading loop from market prices (`auto_trade`)
- Tracks realized PnL from buy/sell actions
- Automatically relearns strategy on a schedule (`auto_relearn`)
- Optimizes thresholds after loss conditions (`optimize_strategy`)

## Quick run
```python
from ai_trade import AutoTradingBot

bot = AutoTradingBot()
decisions = bot.auto_trade([100, 101.5, 100.8, 99.2, 100.1])
print([d.action for d in decisions])
```

## Test
```bash
python -m unittest discover -s tests -v
```
