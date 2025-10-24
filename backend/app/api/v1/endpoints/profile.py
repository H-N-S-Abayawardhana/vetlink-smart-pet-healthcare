from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import EmailStr

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserUpdate, UserResponse
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.put("/update", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile."""
    
    # Check if username or email already exists for other users
    if user_update.username or user_update.email:
        conditions = []
        params = []
        
        if user_update.username:
            conditions.append(User.username == user_update.username)
        if user_update.email:
            conditions.append(User.email == user_update.email)
        
        if conditions:
            from sqlalchemy import or_
            result = await db.execute(
                select(User).where(
                    and_(
                        or_(*conditions),
                        User.id != current_user.id
                    )
                )
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username or email already exists"
                )
    
    # Update user profile
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user

