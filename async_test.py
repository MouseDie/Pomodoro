import asyncio



async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("Hello 2")
    
    
async def main_1():
    print("Hello world 1")
    
    
event_loop = asyncio.get_event_loop()
tasks = [event_loop.create_task(main()), event_loop.create_task(main_1())]
wait_tasks = asyncio.wait(tasks)
event_loop.run_until_complete(wait_tasks)
event_loop.close()