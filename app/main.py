from fastapi import FastAPI
from app.handlers import routers


app = FastAPI()

for router in routers:
    app.include_router(router)
    
    
    
# для примера    
# class AsyncContManager():
#     def __init__(self):
#         self.a = 1
        
    
#     async def __aenter__(self):
#         return self
    
    
#     async def __aexit__(self, exc_type, exc, tb):
#         pass
    

# with AsyncContManager() as manager:
#     manager.a
    
    
    
# class AsyncIterator(object):
    
#     def __iter__(self):
#         return self
    
    
#     async def __anext__(self):
#         pass