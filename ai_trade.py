from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List


@dataclass
class TradeDecision:
    action: str
    price: float


@dataclass
class StrategyConfig:
    buy_threshold: float = 0.01
    sell_threshold: float = -0.01
    relearn_interval: int = 5
    loss_limit: float = -0.02


@dataclass
class AutoTradingBot:
    config: StrategyConfig = field(default_factory=StrategyConfig)
    position: int = 0
    entry_price: float = 0.0
    cash_pnl: float = 0.0
    relearn_count: int = 0
    _returns_window: List[float] = field(default_factory=list)

    def auto_trade(self, prices: Iterable[float]) -> List[TradeDecision]:
        """Execute an automated trading loop for incoming market prices."""
        price_list = list(prices)
        if len(price_list) < 2:
            return []

        decisions: List[TradeDecision] = []
        for previous, current in zip(price_list, price_list[1:]):
            market_return = (current - previous) / previous
            self._returns_window.append(market_return)

            action = self._decide_action(market_return)
            if action == "BUY" and self.position == 0:
                self.position = 1
                self.entry_price = current
            elif action == "SELL" and self.position == 1:
                self.cash_pnl += (current - self.entry_price) / self.entry_price
                self.position = 0
                self.entry_price = 0.0

            decisions.append(TradeDecision(action=action, price=current))

            if len(self._returns_window) % self.config.relearn_interval == 0:
                self.auto_relearn()

        return decisions

    def auto_relearn(self) -> None:
        """Relearn strategy settings when recent performance degrades."""
        if not self._returns_window:
            return

        recent_performance = sum(self._returns_window[-self.config.relearn_interval :]) / min(
            len(self._returns_window), self.config.relearn_interval
        )

        if recent_performance <= self.config.loss_limit:
            self.optimize_strategy(recent_performance)
            self.relearn_count += 1

    def optimize_strategy(self, recent_performance: float) -> None:
        """Optimize thresholds to make the strategy more conservative after losses."""
        adjustment = min(0.005, abs(recent_performance) / 2)
        self.config.buy_threshold = max(0.001, self.config.buy_threshold - adjustment)
        self.config.sell_threshold = min(-0.001, self.config.sell_threshold + adjustment)

    def _decide_action(self, market_return: float) -> str:
        if market_return >= self.config.buy_threshold:
            return "BUY"
        if market_return <= self.config.sell_threshold:
            return "SELL"
        return "HOLD"
