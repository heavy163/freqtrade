import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends

from freqtrade.persistence.trade_model_ext import FtPostionRecord, FtPrediction, FtWalletRecord
from freqtrade.rpc import RPC
from freqtrade.rpc.api_server.api_schemas import (
    CommonResponse,
    FtPostionSchema,
    FtPredictionSchema,
)
from freqtrade.rpc.api_server.deps import get_rpc


logger = logging.getLogger(__name__)

# API version
# Pre-1.1, no version was provided
# Version increments should happen in "small" steps (1.1, 1.12, ...) unless big changes happen.
# 1.0: insert predictions and get position
API_VERSION = 1.0

# Private API, protected by authentication
router = APIRouter()


@router.get("/prediction/latest", response_model=list[FtPredictionSchema], tags=["prediction"])
def get_latest_prediction(
    model: str,
    model_name: Optional[str] = None,
    pair: Optional[str] = None,
    rpc: RPC = Depends(get_rpc),
):
    """Insert predictions"""
    result = rpc.get_latest_prediction(model, model_name, pair)
    FtPrediction.session.remove()
    return result


@router.post("/predictions", response_model=CommonResponse, tags=["prediction"])
def add_prediction(predictions: list[FtPredictionSchema], rpc: RPC = Depends(get_rpc)):
    """Insert predictions"""
    logger.info(f"Inserting {len(predictions)} predictions start")

    data_array = [p.to_row() for p in predictions]
    data_df = pd.DataFrame(data=data_array, columns=FtPredictionSchema.data_columns())

    logger.info(f"Inserting predictions dataframe len {len(data_df)}")

    rows = rpc._insert_predictions(data_df)
    FtPrediction.session.remove()

    logger.info(f"Inserting predictions result {rows}")
    return {"code": 0, "messaged": "ok", "data": f"{rows}"}


@router.get("/position/records", response_model=list[FtPostionSchema], tags=["position"])
def get_position_records(
    strategy: Optional[str] = None,
    strategy_id: Optional[int] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    rpc: RPC = Depends(get_rpc),
):
    """Get Poistion Records"""
    result = rpc._get_position_records(strategy, strategy_id, start, end)
    FtPostionRecord.session.remove()
    return result


@router.get("/position/record/latest", response_model=list[FtPostionSchema], tags=["position"])
def get_latest_position_record(
    strategy: Optional[str] = None,
    strategy_id: Optional[int] = None,
    pair: Optional[str] = None,
    rpc: RPC = Depends(get_rpc),
):
    """Get latest position records"""
    result = rpc.get_latest_position_record(strategy, strategy_id, pair)
    FtPostionRecord.session.remove()
    return result


@router.get("/strategy/data", tags=["strategy"])
def get_strategy_data(
    data_name: str,
    data_query_args: Optional[dict] = None,
    rpc: RPC = Depends(get_rpc),
):
    if data_query_args is None:
        data_query_args = {}
    return rpc.get_strategy_data(data_name, **data_query_args)
