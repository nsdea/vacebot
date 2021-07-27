# VaceMC
The (German) Discord Bot for the *VaceMC.de* Minecraft Server Network

# Details
## Hosting
### Recommended Python Version
Tested:
- 3.7.9
- 3.8
- 3.8.10

(all of them *should* work)

### Recommended Operating System
Tested:
- Windows 10
- Ubuntu 21
- Debian 10

# Installation
I'm not going to explain it in detail, because setting this thing up is not a thing that is meant to be done more than 1 single time.

Make sure to read "Details" first!

Grab yourself a coffe (or green tea, or cacao), because this can take ages, depending on how much experience you have with tech. 

## Set up Minecraft server plugins
The bot can display information about your Minecraft server.
But you need to set some plugins up first.

- https://www.spigotmc.org/resources/servertap.79031/
    - **In the config:**
        - set `useKeyAuth: true`
        - set `key: think_of_a_good_password_and_set_it_in_here`

- quoting [servertap.io](https://servertap.io/), a "Vault-compatible economy plugin"

### Important data
This is secret data which you should save somewhere for later use.

- **Server IP**
    - example: `12.345.67.890`
    - you'll have to find it out, maybe see on your hoster's dashboard
    - `127.0.0.1` *should* also work

- **Servertap Port**
    - default: `4567`
    - it can be changed in the config

- **Servertap Key**
    - the header key needed to access server data
    - can be found in the config

## Set up `.env`:
`.env` is the file in which secret stuff is happening.
Never give anyone or anything access to this file! If you do so, your Discord server & bot and your Minecraft server including all systems can easily be destroyed!

Just rename `dot_env_template.txt` to `.env` and replace the variables beginning at line 101 with your values.