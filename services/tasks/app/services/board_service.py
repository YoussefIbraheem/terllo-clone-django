from typing import List, Optional
from app.models.board import Board
from app.schemas.board_schema import BoardCreate, BoardUpdate, BoardResponse
from app.db.database import get_db_session


def get_board_by_project(
    project_id: int, limit: int = 50, offset: int = 0
) -> List[BoardResponse]:

    with get_db_session() as db:
        db_boards = (
            db.query(Board)
            .filter(Board.project_id == project_id)
            .limit(limit)
            .offset(limit)
            .all()
        )

        return [BoardResponse.model_dump(board) for board in db_boards]


def get_board_by_id(board_id: int) -> Optional[BoardResponse]:

    with get_db_session() as db:
        db_board = db.query(Board).filter(Board.id == board_id).first()

        if not db_board:
            return None

        return BoardResponse.model_dump(db_board)


def create_board(board_data: BoardCreate) -> BoardResponse:

    with get_db_session() as db:
        db_board = Board(
            name=board_data.name,
            description=board_data.description,
            project_id=board_data.project_id,
            columns=board_data.columns,
        )

        db.add(db_board)
        db.flush()
        db.refresh(db_board)

        return BoardResponse.model_dump(db_board)


def update_board(board_id: int, board_data: BoardUpdate) -> Optional[BoardResponse]:

    with get_db_session() as db:
        db_board = db.query(Board).filter(Board.id == board_id).first()

        if not db_board:
            return None

        if board_data.name is not None:
            db_board.name = board_data.name

        if board_data.description is not None:
            db_board.description = board_data.description

        if board_data.columns is not None:
            db_board.columns = board_data.columns

        db.flush()
        db.refresh(db_board)

        return BoardResponse.model_dump(db_board)


def delete_board(board_id: int) -> bool:

    with get_db_session() as db:

        db_board = db.query(Board).filter(Board.id == board_id).first()

        if not db_board:
            return False

        db_board.delete()
        db.flush()

        return True
