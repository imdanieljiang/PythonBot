# PythonBot

## A side-project Discord bot created for my frequent usage of Discord

### Please install the required dependencies in the requirements.txt file

### Current features:
- Pulls from Reddit's using the Python Reddit API Wrapper (PRAW) using async functions
  - Grabs the hottest 'n' number of posts from any 's' subreddit
  - ![Screen Shot 2021-11-17 at 1 03 15 AM](https://user-images.githubusercontent.com/83325543/142169963-4a5ae4bf-8ceb-492d-9096-58f3b99403d7.png)
- Customizable server specific bot command prefix
  - Members with administrator permissions can change the bot command prefix
  - ![Screen Shot 2021-11-17 at 1 06 13 AM](https://user-images.githubusercontent.com/83325543/142170604-1657b5f7-852d-4eda-a1e3-371881b3b377.png)
  - The bot command prefix can be unique to each server
- Displays server rules
  - Displays all rules
  - Displays specific rules
- Command that greets users
- Moderation commands
  - Muting/unmuting members
  - Kicking members
  - Banning/unbanning members
- Auto-moderation
  - Message is automatically deleted if it includes a filtered word
- Creates embeded polls
  - Currently only allows two options
- Displays user information
- Error handling
  - Non-existent commands and missing arguments will be handled
