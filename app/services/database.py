"""
MongoDB database service for storing and retrieving analysis results.
Manages database connection and CRUD operations.
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson.objectid import ObjectId
import os

try:
    from motor.motor_asyncio import AsyncClient
except ImportError:
    AsyncClient = None

logger = logging.getLogger(__name__)

# MongoDB connection string
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "ChecknNext"
COLLECTION_NAME = "analyses"

# Global database connection
client: Optional[Any] = None
db: Optional[Any] = None
analyses_collection: Optional[Any] = None


async def connect_to_mongo():
    """
    Establish connection to MongoDB using Motor (async driver).
    Called during application startup.
    """
    global client, db, analyses_collection
    
    if AsyncClient is None:
        logger.warning("⚠️ Motor not available, MongoDB disabled")
        return
    
    try:
        logger.info(f"🔗 Connecting to MongoDB at {MONGODB_URL}...")
        client = AsyncClient(MONGODB_URL)
        
        # Verify connection
        await client.admin.command('ping')
        logger.info("✅ MongoDB connection successful")
        
        # Initialize database and collection
        db = client[DATABASE_NAME]
        analyses_collection = db[COLLECTION_NAME]
        
        # Create indexes for better query performance
        await analyses_collection.create_index("created_at")
        logger.info("✅ Database indexes created")
        
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
        raise


async def close_mongo_connection():
    """
    Close MongoDB connection.
    Called during application shutdown.
    """
    global client
    
    try:
        if client:
            client.close()
            logger.info("🔌 MongoDB connection closed")
    except Exception as e:
        logger.error(f"❌ Error closing MongoDB connection: {str(e)}")


async def save_analysis_result(
    match_percentage: int,
    missing_skills: List[str],
    improvement_suggestions: List[str],
    resume_length: int,
    jd_length: int
) -> str:
    """
    Save analysis result to MongoDB.
    
    Args:
        match_percentage: Match score (0-100)
        missing_skills: List of missing skills
        improvement_suggestions: List of suggestions
        resume_length: Character count of resume
        jd_length: Character count of job description
        
    Returns:
        str: MongoDB document ID as string
    """
    try:
        now = datetime.utcnow()
        
        document = {
            "match_percentage": match_percentage,
            "missing_skills": missing_skills,
            "improvement_suggestions": improvement_suggestions,
            "resume_length": resume_length,
            "jd_length": jd_length,
            "created_at": now,
            "updated_at": now
        }
        
        result = await analyses_collection.insert_one(document)
        logger.info(f"✅ Analysis saved with ID: {result.inserted_id}")
        
        return str(result.inserted_id)
        
    except Exception as e:
        logger.error(f"❌ Error saving analysis result: {str(e)}")
        raise


async def get_analysis_by_id(analysis_id: str) -> Optional[Dict]:
    """
    Retrieve a specific analysis result by ID.
    
    Args:
        analysis_id: MongoDB document ID
        
    Returns:
        Dict: Analysis result or None if not found
    """
    try:
        result = await analyses_collection.find_one(
            {"_id": ObjectId(analysis_id)}
        )
        
        if result:
            result["analysis_id"] = str(result.pop("_id"))
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Error retrieving analysis: {str(e)}")
        raise


async def get_all_analyses(limit: int = 50, skip: int = 0) -> List[Dict]:
    """
    Retrieve all analysis results with pagination.
    
    Args:
        limit: Maximum number of results
        skip: Number of results to skip
        
    Returns:
        List[Dict]: List of analysis results
    """
    try:
        cursor = analyses_collection.find().sort("created_at", -1).skip(skip).limit(limit)
        results = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for result in results:
            result["analysis_id"] = str(result.pop("_id"))
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Error retrieving analyses: {str(e)}")
        raise


async def delete_analysis(analysis_id: str) -> bool:
    """
    Delete an analysis result by ID.
    
    Args:
        analysis_id: MongoDB document ID
        
    Returns:
        bool: True if deleted, False if not found
    """
    try:
        result = await analyses_collection.delete_one(
            {"_id": ObjectId(analysis_id)}
        )
        
        if result.deleted_count > 0:
            logger.info(f"✅ Analysis deleted: {analysis_id}")
            return True
        
        logger.warning(f"⚠️ Analysis not found: {analysis_id}")
        return False
        
    except Exception as e:
        logger.error(f"❌ Error deleting analysis: {str(e)}")
        raise


async def get_statistics() -> Dict:
    """
    Get database statistics (total analyses, average match percentage, etc).
    
    Returns:
        Dict: Statistics about analyses
    """
    try:
        total = await analyses_collection.count_documents({})
        
        # Calculate average match percentage
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "avg_match": {"$avg": "$match_percentage"},
                    "min_match": {"$min": "$match_percentage"},
                    "max_match": {"$max": "$match_percentage"}
                }
            }
        ]
        
        stats_result = await analyses_collection.aggregate(pipeline).to_list(1)
        
        if stats_result:
            stats = stats_result[0]
            return {
                "total_analyses": total,
                "average_match_percentage": round(stats.get("avg_match", 0), 2),
                "min_match_percentage": stats.get("min_match", 0),
                "max_match_percentage": stats.get("max_match", 0)
            }
        
        return {
            "total_analyses": total,
            "average_match_percentage": 0,
            "min_match_percentage": 0,
            "max_match_percentage": 0
        }
        
    except Exception as e:
        logger.error(f"❌ Error getting statistics: {str(e)}")
        raise
