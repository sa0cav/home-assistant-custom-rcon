# Home Assistant Custom RCON Integration

This is a custom integration for Home Assistant that allows you to connect to RCON-enabled CS2 and Minecraft servers, expose server data or control commands as Home Assistant entities.

## Features

- Send RCON commands as Home Assistant services  
- Display server status or data as sensors for CS2 
- Use buttons to trigger RCON commands  

## Installation

1. Copy the `custom_components/rcon` directory into your Home Assistant `config/custom_components` folder.  
2. Restart Home Assistant.  
3. Go to **Settings → Devices & Services → Integrations** and click **Add Integration**.  
4. Search for and select **RCON**.  
5. Fill in your server details (IP, port, password, game).

## Configuration

All setup is done via the Home Assistant UI (config flow).

### CS2 Raw Log Configuration

To power the CS2 event sensors and the Raw Log sensor, forward your server’s log lines into Home Assistant.  
Add the following to your `server.cfg`:

```
sv_logfile 1
log on
logaddress_add_http "http://<HOME_ASSISTANT_IP>:8123/api/rcon/log"
```

- Replace `<HOME_ASSISTANT_IP>` with the IP or hostname of your Home Assistant server.
- This will POST each log line from CS2 to your integration's HTTP endpoint.

After restarting your CS2 server, Home Assistant will receive every log line and fire an internal `rcon_log` event.  
The integration’s sensors listen for that event, parse the data (kills, chat, rounds, bomb status, etc.), and update automatically.

## Available Files

- `__init__.py` → Sets up services & HTTP log receiver  
- `config_flow.py` → Handles the integration’s configuration UI  
- `const.py` → Stores constants and loads command presets  
- `sensor.py` → Defines sensors for RCON or CS2 log events  
- `button.py` → Defines buttons for predefined RCON commands  
- `commands.yaml` → Lists default commands per game  
- `services.yaml` → Defines the `rcon.send_command` service  
- `manifest.json` → Integration metadata (used by Home Assistant)  
- `hacs.json` → Metadata for HACS (Home Assistant Community Store)  

## Example Usage

```yaml
service: rcon.send_command
data:
  server: my_server
  command: "say Hello from Home Assistant!"
```

## Notes

- Ensure your game server allows RCON connections from your Home Assistant instance.  
- Excessive or rapid RCON usage may affect server performance.  

## License

MIT License
