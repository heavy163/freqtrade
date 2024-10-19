import datetime as dtm
from datetime import datetime
from typing import Any, Union

import pandas as pd
from sqlalchemy import desc
from sqlalchemy.orm.properties import MappedColumn
from sqlalchemy.orm.query import Query

from freqtrade.persistence.base import ModelBase, SessionType


def read_table(
    session: SessionType,
    table: ModelBase,
    start_date: datetime = None,
    end_date: datetime = None,
    filters=None,
    datetime_col: MappedColumn = None,
    return_dataframe = True,
) -> pd.DataFrame:
    query: Query = session.query(table)
    if start_date is not None:
        query = query.filter(datetime_col >= start_date)
    if end_date is not None:
        query = query.filter(datetime_col <= end_date)
    if filters is not None:
        if not isinstance(filters, list):
            filters = [filters]
        for f in filters:
            query = query.filter(f)
    if return_dataframe:
        return pd.read_sql(query.statement, session.connection())
    else:
        return query.all()


def get_latest_record(
    session: SessionType,
    table: ModelBase,
    datetime_col: MappedColumn = None,
    filters=None,
    return_dataframe=False,
) -> Union[pd.DataFrame, Any]:
    query: Query = session.query(table)
    if filters is not None:
        if not isinstance(filters, list):
            filters = [filters]
        for f in filters:
            query = query.filter(f)
    query = query.order_by(desc(datetime_col)).limit(1)
    if return_dataframe:
        return pd.read_sql(query.statement, session.connection())
    else:
        return query.one_or_none()


def get_latest_record_time(
    session: SessionType,
    table: ModelBase,
    datetime_col: MappedColumn = None,
    filters=None,
) -> datetime:
    record = get_latest_record(
        session, table, datetime_col=datetime_col, filters=filters, return_dataframe=False
    )
    if record is not None:
        return getattr(record, datetime_col.name)
    return None


def save_to_db(
    session: SessionType,
    table: ModelBase,
    df: pd.DataFrame,
    last_record_filters=None,
    datetime_col: MappedColumn = None,
    unique_cols=None,
):
    if unique_cols is not None:
        df.drop_duplicates(subset=unique_cols, inplace=True)
    lastet_record_time = get_latest_record_time(
        session, table, datetime_col=datetime_col, filters=last_record_filters
    )
    origin_len = len(df)
    if lastet_record_time is not None:
        tz = None
        try:
            tz = getattr(df.dtypes[datetime_col.name], "tz")  # noqa: B009
        except Exception:  # noqa: S110
            pass
        if tz is not None and lastet_record_time.tzinfo is not None:
            lastet_record_time = lastet_record_time.astimezone(tz)
        elif tz is not None and lastet_record_time.tzinfo is None:
            lastet_record_time = lastet_record_time.replace(tzinfo=dtm.timezone.utc).astimezone(tz)
        elif tz is None and lastet_record_time.tzinfo is not None:
            lastet_record_time = lastet_record_time.astimezone(dtm.timezone.utc).replace(
                tzinfo=None
            )
        df[datetime_col.name] = df[datetime_col.name].dt.floor(freq="1s")
        df = df[df[datetime_col.name] > lastet_record_time]
    if len(df) == 0:
        print(f"dataframe is empty after filter by latest record, original len {origin_len}")
        rows = 0
    else:
        rows = df.to_sql(table.__tablename__, session.connection(), index=False, if_exists="append")
        session.commit()
        print(f"total {rows} saved {len(df)} into table {table.__tablename__}")
    return rows
