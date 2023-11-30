### About
Using Django Channels for Real-Time chat. Also, this project has an admin chat to manage client's messages and manager/agent can reply to clients.

### Features
- Managing users and rooms in chat admin
   - The ability to add a user with 2 roles [as an agent or manager]. And ability to edit and delete the users. Only managers can add, edit and delete users.
   - Only managers can delete the rooms. Agents can only join the chat room in chat admin. Managers can join and delete chat rooms.

- Each Room has 3 status: Closed, Active and Waiting
   - When client left the chat, Room status going to closed.
   - When manager/agent join the chat, Room status going to active.
   - When client join the chat and manager/agent doesn't open the chat, Room status going to waiting.
 
- Custom user manager for creating a user
- Is typing... ability
- Send message by enter
