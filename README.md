# PythonBot

## A side-project Discord bot created for my frequent usage of Discord

### Please install the required dependencies in the requirements.txt file

### Current features:
- Pulls from Reddit's using the Python Reddit API Wrapper (PRAW) using async functions
  - Grabs the hottest 'n' number of posts from any 's' subreddit
    > ![Screen Shot 2021-11-17 at 1 03 15 AM](https://user-images.githubusercontent.com/83325543/142169963-4a5ae4bf-8ceb-492d-9096-58f3b99403d7.png)
- Customizable server specific bot command prefix
  - Members with administrator permissions can change the bot command prefix
    > ![Screen Shot 2021-11-17 at 1 06 13 AM](https://user-images.githubusercontent.com/83325543/142170604-1657b5f7-852d-4eda-a1e3-371881b3b377.png)
  - The bot command prefix can be unique to each server
- Displays all server rules
    > ![Screen Shot 2021-11-17 at 1 06 42 AM](https://user-images.githubusercontent.com/83325543/142170810-3b8c095e-b5d9-4c33-930a-205baf49288b.png)
  - Displays specific rules
    > ![Screen Shot 2021-11-17 at 1 10 28 AM](https://user-images.githubusercontent.com/83325543/142171026-f3519337-74b8-479b-bf67-ea513c55423f.png)
- Command that greets users
- Moderation commands
  - Muting/unmuting members
  - Kicking members
  - Banning/unbanning members
- Auto-moderation
  - Message is automatically deleted if it includes a filtered word
- Creates embedded polls (up to ten possible options)
    > ![Screen Shot 2021-11-17 at 1 07 55 AM](https://user-images.githubusercontent.com/83325543/142171254-e9412ed8-9487-49eb-8de9-e97887fd269c.png)
- Displays user information
- Error handling
  - Non-existent commands and missing arguments will be handled
