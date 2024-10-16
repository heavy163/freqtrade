import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends

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
    model: str, model_name: str = None, pair: str = None, rpc: RPC = Depends(get_rpc)
):
    """Insert predictions"""
    return rpc.get_latest_prediction(model, model_name, pair)


@router.post("/predictions", response_model=CommonResponse, tags=["prediction"])
def add_prediction(predictions: list[FtPredictionSchema], rpc: RPC = Depends(get_rpc)):
    """Insert predictions"""
    data_array = [p.to_row() for p in predictions]
    data_df = pd.DataFrame(data=data_array, columns=FtPredictionSchema.data_columns())
    rows = rpc._insert_predictions(data_df)
    return {"code": 0, "messaged": "ok", "data": f"{rows}"}


@router.get("/positions", response_model=list[FtPostionSchema], tags=["position"])
def get_current_positions(
    strategy: Optional[str] = None,
    strategy_id: Optional[int] = None,
    start: Optional[datetime] = None,
    end: Optional[str] = None,
    rpc: RPC = Depends(get_rpc),
):
    """Get Current Poistions"""
    return rpc._get_current_positions(strategy, strategy_id)


@router.get("/position/records", response_model=list[FtPostionSchema], tags=["position"])
def get_position_records(
    strategy: Optional[str] = None,
    strategy_id: Optional[int] = None,
    start: Optional[datetime] = None,
    end: Optional[str] = None,
    rpc: RPC = Depends(get_rpc),
):
    """Get Poistion Records"""
    return rpc._get_position_records(strategy, strategy_id, start, end)


@router.get("/position/record/latest", response_model=list[FtPostionSchema], tags=["position"])
def get_latest_position_record(
    strategy: Optional[str] = None,
    strategy_id: Optional[int] = None,
    pair: Optional[str] = None,
    rpc: RPC = Depends(get_rpc),
):
    """Get latest position records"""
    return rpc.get_latest_position_record(strategy, strategy_id, pair)
