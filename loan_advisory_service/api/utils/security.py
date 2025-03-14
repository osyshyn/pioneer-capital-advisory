from fastapi import Depends
from fastapi.security import HTTPBearer

bearer = Depends(HTTPBearer())
