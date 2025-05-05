
# Home Assistant Custom RCON Integration

This is a custom integration for Home Assistant that allows you to connect to RCON-enabled servers (like Minecraft or other game servers) and expose server data or control commands as Home Assistant entities.

## Features

- Send RCON commands as Home Assistant services
- Display server status or data as sensors
- Use buttons to trigger RCON commands

## Installation

1. Copy the `custom_components/rcon` directory into your Home Assistant `config/custom_components` folder.
2. Restart Home Assistant.
3. Go to **Settings → Devices & Services → Integrations** and add **RCON**.
4. Fill in your server details (IP, port, password).

## Configuration

This integration uses a config flow, so all setup is done via the Home Assistant UI.

## Available Files

- `__init__.py` → Sets up the integration.
- `config_flow.py` → Handles the configuration flow in the UI.
- `const.py` → Stores constants.
- `sensor.py` → Defines sensors pulling RCON data.
- `button.py` → Defines buttons to send RCON commands.
- `commands.yaml` → Defines available commands.
- `services.yaml` → Describes available Home Assistant services.
- `manifest.json` → Metadata for the integration.

## Example Usage

```yaml
service: rcon.send_command
data:
  command: "say Hello from Home Assistant!"
```

## Notes

- Ensure your server allows RCON connections from your Home Assistant instance.
- Use responsibly; excessive RCON commands can affect server performance.

## License

Non-Commercial License
