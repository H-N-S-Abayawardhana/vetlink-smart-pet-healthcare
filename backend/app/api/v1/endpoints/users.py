from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List

from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserListResponse
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=UserListResponse)
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all users (Super Admin only)."""
    
    if current_user.user_role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden - Super Admin access required"
        )
    
    result = await db.execute(
        select(User).order_by(User.created_at.desc())
    )
    users = result.scalars().all()
    
    return UserListResponse(
        users=[UserResponse.from_orm(user) for user in users],
        total=len(users)
    )

@router.put("/{user_id}/role")
async def update_user_role(
    user_id: int,
    new_role: UserRole,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user role (Super Admin only)."""
    
    if current_user.user_role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden - Super Admin access required"
        )
    
    # Get the user to update
    result = await db.execute(select(User).where(User.id == user_id))
    user_to_update = result.scalar_one_or_none()
    
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent super admin from changing their own role
    if user_to_update.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )
    
    # Update the role
    user_to_update.user_role = new_role
    await db.commit()
    await db.refresh(user_to_update)
    
    return {
        "message": f"User role updated to {new_role.value}",
        "user": UserResponse.from_orm(user_to_update)
    }

@router.put("/{user_id}/status")
async def update_user_status(
    user_id: int,
    is_active: bool,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user active status (Super Admin only)."""
    
    if current_user.user_role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden - Super Admin access required"
        )
    
    # Get the user to update
    result = await db.execute(select(User).where(User.id == user_id))
    user_to_update = result.scalar_one_or_none()
    
    if not user_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Prevent super admin from deactivating themselves
    if user_to_update.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot deactivate your own account"
        )
    
    # Update the status
    user_to_update.is_active = is_active
    await db.commit()
    await db.refresh(user_to_update)
    
    status_text = "activated" if is_active else "deactivated"
    return {
        "message": f"User {status_text} successfully",
        "user": UserResponse.from_orm(user_to_update)
    }

