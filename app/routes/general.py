from fastapi import APIRouter, Depends

from app.services.cache import RedisCache

router = APIRouter()


@router.post("/clear-cache", status_code=200)
async def clear_cache(redis_service: RedisCache = Depends()):
	await redis_service.clear_cache()
	return {"message": "Redis cache cleared successfully"}
