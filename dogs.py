import asyncio
import aiohttp

async def get_task(user_id, reference):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.onetime.dog/tasks?user_id={user_id}&reference={reference}") as response:
                return await response.json()
    except Exception as err:
        print(err)
        return None

async def verify_task(user_id, reference):
    try:
        task = await get_task(user_id, reference)
        for slug in task:
            config = {
                "url": f"https://api.onetime.dog/tasks/verify?task={slug['slug']}&user_id={user_id}&reference={reference}",
                "method": "POST",
                "headers": {
                    "accept": "application/json",
                    "accept-language": "en-US,en;q=0.9",
                    "cache-control": "no-cache",
                    "content-type": "text/plain;charset=UTF-8",
                    "pragma": "no-cache",
                    "priority": "u=1, i",
                    "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126", "Microsoft Edge WebView2";v="126"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "Referer": "https://onetime.dog/",
                    "Referrer-Policy": "strict-origin-when-cross-origin",
                },
            }

            if slug['slug'] != "invite-frens":
                async with aiohttp.ClientSession() as session:
                    async with session.post(config['url'], headers=config['headers']) as response:
                        response_data = await response.json()
                        if response_data['success']:
                            print(f"Completed task {slug['slug']}")
                        else:
                            print(slug['slug'], response_data['error_code'])
                await asyncio.sleep(5)
                total = await get_rewards_user(user_id)
                print(f"Balance: {total}")
    except Exception as err:
        print(err)

async def get_rewards_user(user_id):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.onetime.dog/rewards?user_id={user_id}") as response:
                data = await response.json()
                return data['total']
    except Exception as err:
        print(err.message)
        return None

async def main():
    try:
        with open('data.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                user_id, reference = line.strip().split('|')
                await verify_task(user_id, reference)
    except Exception as err:
        print(f"Error reading data.txt: {err}")

if __name__ == "__main__":
    asyncio.run(main())