import fastapi
import fastapi_chameleon
from starlette.requests import Request
from db .job import JobActions

from viewmodels.shared.viewmodel_base import ViewModelBase

router = fastapi.APIRouter()


@router.get('/ai/start/{action}/{podcast_id}/episode/{episode_id}')
def start_job(action: JobActions, podcast_id: str, episode_id: int ):
    return{"action": action, "podcast_id": podcast_id, "episode_id": episode_id}

@router.get('/check_status')
def check_job_status():
    pass