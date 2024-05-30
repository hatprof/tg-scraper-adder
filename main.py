from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import asyncio

async def login_and_save(api_id, api_hash, phone_number):
    client = TelegramClient('session_name', api_id, api_hash)
    await client.start(phone_number)
    # You can save the session here if needed
    return client

async def scrape_usernames(client, group_username):
    group_entity = await client.get_entity(group_username)
    participants = await client(GetParticipantsRequest(
        group_entity,
        filter=ChannelParticipantsSearch(''),
        offset=0,
        limit=100,
        hash=0
    ))
    usernames = []
    for user in participants.users:
        if user.username:
            usernames.append(user.username)
    return usernames

async def add_to_group(client, target_group_username, usernames):
    target_entity = await client.get_entity(target_group_username)
    for username in usernames:
        try:
            await client(InviteToChannelRequest(target_entity, [username]))
        except Exception as e:
            print(f"Failed to add {username} to the group: {e}")

async def main():
    # Your Telegram API credentials
    api_id = 'your_api_id'
    api_hash = 'your_api_hash'
    phone_number = 'your_phone_number'

    # Login and save the session
    client = await login_and_save(api_id, api_hash, phone_number)

    # Group to scrape usernames from
    group_username = 'group_username'

    # Scrape usernames from the group
    scraped_usernames = await scrape_usernames(client, group_username)

    # Group to add scraped usernames to
    target_group_username = 'target_group_username'

    # Add scraped usernames to the target group
    await add_to_group(client, target_group_username, scraped_usernames)

    await client.disconnect()

asyncio.run(main())

//tool made by codeprofessor
