"""
This module contains the class to persist trades into SQLite
"""

from datetime import datetime
from typing import ClassVar, Optional

from sqlalchemy import (
    Float,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from freqtrade.persistence.base import ModelBase, SessionType


class FtPrediction(ModelBase):
    """
    Trade database model.
    Also handles updating and querying trades

    Note: Fields must be aligned with LocalPrediction class
    """

    __tablename__ = "ft_predictions"
    session: ClassVar[SessionType]

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # type: ignore
    close_time: Mapped[datetime] = mapped_column()
    pair: Mapped[str] = mapped_column(String(25), nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(64))
    model_name: Mapped[str] = mapped_column(String(128))
    train_start: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    train_end: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    rank_start: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    rank_end: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    rank_ls_rtn: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    rank_sharpe: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    y_pred: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def commit():
        FtPrediction.session.commit()

    @staticmethod
    def rollback():
        FtPrediction.session.rollback()


class FtPostion(ModelBase):
    """
    Trade database model.
    Also handles updating and querying trades

    Note: Fields must be aligned with LocalPrediction class
    """

    __tablename__ = "ft_position"
    session: ClassVar[SessionType]

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # type: ignore
    pair: Mapped[str] = mapped_column(String(25), nullable=False, index=True)
    strategy: Mapped[str] = mapped_column(String(32))
    strategy_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    side: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    stake_amount: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    filled_stake_amount: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    open_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    open_price: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    close_reason: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    close_price: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    group: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    refreshed_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    y_pred_scaled: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    refreshed_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    prediction_refreshed_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    latest_close: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    latest_high: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    latest_low: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    trade_id: Mapped[int] = mapped_column(Integer, nullable=True)
    trade_side: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    trade_leverage: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    trade_stake_amount: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    trade_value: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    unbalance_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    unbalance_state: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    warn_state: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def commit():
        FtPostion.session.commit()

    @staticmethod
    def rollback():
        FtPostion.session.rollback()

    def to_json(self):
        return {
            "id": self.id,
            "pair": self.pair,
            "strategy": self.strategy,
            "strategy_id": self.strategy_id,
            "side": self.side,
            "stake_amount": self.stake_amount,
            "filled_stake_amount": self.filled_stake_amount,
            "open_date": self.open_date,
            "open_price": self.open_price,
            "close_reason": self.close_reason,
            "close_price": self.close_price,
            "group": self.group,
            "status": self.status,
            "refreshed_date": self.refreshed_date,
            "y_pred_scaled": self.y_pred_scaled,
            "refreshed_count": self.refreshed_count,
            "prediction_refreshed_date": self.prediction_refreshed_date,
            "latest_close": self.latest_close,
            "latest_high": self.latest_high,
            "latest_low": self.latest_low,
            "trade_id": self.trade_id,
            "trade_side": self.trade_side,
            "trade_leverage": self.trade_leverage,
            "trade_stake_amount": self.trade_stake_amount,
            "trade_value": self.trade_value,
            "unbalance_time": self.unbalance_time,
            "unbalance_state": self.unbalance_state,
            "warn_state": self.warn_state,
        }

class FtPostionRecord(ModelBase):
    """
    Keep same struct with FtPosition, just backup records here.
    """

    __tablename__ = "ft_position_record"
    session: ClassVar[SessionType]

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # type: ignore
    pair: Mapped[str] = mapped_column(String(25), nullable=False, index=True)
    strategy: Mapped[str] = mapped_column(String(32))
    strategy_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, default=0)
    side: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    stake_amount: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    filled_stake_amount: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    open_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    open_price: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    close_reason: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    close_price: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    group: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    status: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    refreshed_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    y_pred_scaled: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    refreshed_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    prediction_refreshed_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    latest_close: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    latest_high: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    latest_low: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    trade_id: Mapped[int] = mapped_column(Integer, nullable=True)
    trade_side: Mapped[Optional[str]] = mapped_column(String(16), nullable=True)
    trade_leverage: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    trade_stake_amount: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    trade_value: Mapped[Optional[float]] = mapped_column(Float(), nullable=True)
    unbalance_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    unbalance_state: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)
    warn_state: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def commit():
        FtPostionRecord.session.commit()

    @staticmethod
    def rollback():
        FtPostionRecord.session.rollback()

    def to_json(self):
        return {
            "id": self.id,
            "pair": self.pair,
            "strategy": self.strategy,
            "strategy_id": self.strategy_id,
            "side": self.side,
            "stake_amount": self.stake_amount,
            "filled_stake_amount": self.filled_stake_amount,
            "open_date": self.open_date,
            "open_price": self.open_price,
            "close_reason": self.close_reason,
            "close_price": self.close_price,
            "group": self.group,
            "status": self.status,
            "refreshed_date": self.refreshed_date,
            "y_pred_scaled": self.y_pred_scaled,
            "refreshed_count": self.refreshed_count,
            "prediction_refreshed_date": self.prediction_refreshed_date,
            "latest_close": self.latest_close,
            "latest_high": self.latest_high,
            "latest_low": self.latest_low,
            "trade_id": self.trade_id,
            "trade_side": self.trade_side,
            "trade_leverage": self.trade_leverage,
            "trade_stake_amount": self.trade_stake_amount,
            "trade_value": self.trade_value,
            "unbalance_time": self.unbalance_time,
            "unbalance_state": self.unbalance_state,
            "warn_state": self.warn_state,
        }
