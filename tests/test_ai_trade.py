import unittest

from ai_trade import AutoTradingBot, StrategyConfig


class AutoTradingBotTests(unittest.TestCase):
    def test_auto_trade_generates_buy_and_sell(self):
        bot = AutoTradingBot(config=StrategyConfig(buy_threshold=0.01, sell_threshold=-0.01, relearn_interval=10))

        decisions = bot.auto_trade([100, 102, 101, 99])

        self.assertEqual([d.action for d in decisions], ["BUY", "HOLD", "SELL"])
        self.assertEqual(bot.position, 0)
        self.assertLess(bot.cash_pnl, 0)

    def test_auto_relearn_triggers_optimization(self):
        bot = AutoTradingBot(
            config=StrategyConfig(
                buy_threshold=0.02,
                sell_threshold=-0.02,
                relearn_interval=3,
                loss_limit=-0.01,
            )
        )

        bot.auto_trade([100, 98, 96, 94])

        self.assertEqual(bot.relearn_count, 1)
        self.assertLess(bot.config.buy_threshold, 0.02)
        self.assertGreater(bot.config.sell_threshold, -0.02)


if __name__ == "__main__":
    unittest.main()
