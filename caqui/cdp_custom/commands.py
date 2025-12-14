import websockets
import json
import asyncio

async def click_element(element_id):
    async with websockets.connect("ws://localhost:9222/devtools/page/2") as ws:
        # Execute JS inside the page
        script = f"""
        (function() {{
            const el = document.querySelector('[id="{element_id}"]');
            if (el) el.click();
        }})();
        """

        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": script}
        }))

        return await ws.recv()

async def navigate(url):
    async with websockets.connect("ws://localhost:9222/devtools/page/1") as ws:
        # Execute JS inside the page
        script = f"""
        window.location.href = {url};
        """

        await ws.send(json.dumps({
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {"expression": script}
        }))

        return await ws.recv()


# asyncio.run(click_element("965b1b69-3204-4b78-9860-c78b90dc8583"))
