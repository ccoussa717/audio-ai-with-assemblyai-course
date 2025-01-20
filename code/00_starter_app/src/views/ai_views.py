import fastapi
import fastapi_chameleon
import bson
from starlette.requests import Request
from bson import ObjectId
from db .job import JobActions
from viewmodels.ai.start_job_viewmodel import StartJobViewModel
from viewmodels.shared.viewmodel_base import ViewModelBase
from services import background_service

router = fastapi.APIRouter()


@router.get('/ai/start/{action}/{podcast_id}/episode/{episode_number}')
async def start_job(
    request: Request, 
    action: str,
    podcast_id: str, 
    episode_number: int
):
    try:
        job_action = JobActions[action.lower()]  # Convert to lowercase to match enum
        vm = StartJobViewModel(request, podcast_id, episode_number, job_action)
        job = await background_service.create_background_job(job_action, podcast_id, episode_number)
        
        print(f"Job created: {job.id}")
        return {
            "action": action, 
            "podcast_id": podcast_id, 
            "episode_id": episode_number, 
            "jobid": str(job.id)
        }
    except KeyError:
        raise fastapi.HTTPException(
            status_code=400,
            detail=f"Invalid action. Must be one of: {[a.name.lower() for a in JobActions]}"
        )

@router.get('/ai/check-status/{job_id}')
async def check_job_status(job_id: str):
    finished = await background_service.get_job_status(bson.ObjectId(job_id))
    print(f"Job status: {finished}")
    return {"status": finished}
