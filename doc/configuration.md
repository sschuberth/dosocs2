## Configuration 

`dosocs2` is configured through plain text configuration files.

An explanation of the configuration options is found in the default
`dosocs2.conf` file. To generate a copy of this file, run
`dosocs2 newconfig`. It will write the default config to
`$XDG_CONFIG_HOME/dosocs2/dosocs2.conf`. Unless you have explicitly
defined `$XDG_CONFIG_HOME` in your environment, the new config file will
probably be at `~/.config/dosocs2/dosocs2.conf`.

### Resolution order

`dosocs2` will read configuration files in the following order:

- The in-memory default config (defined in `config.py`)
- `/etc/dosocs2.conf`
- `$XDG_CONFIG_HOME/dosocs2/dosocs2.conf` (if not defined,
  `$XDG_CONFIG_HOME` is equal to `$HOME/.config`)
- If an alternate config file is specified on the command line with `-f`,
  that one is used *instead of* the one in `$XDG_CONFIG_HOME`.

All existing config files in the resolution order are read if they exist,
and each one overrides any values from the previous one. Any value that
is undefined in a config file will default to its value in the config
file before it in the resolution order.

One can see the resolution order and the effective configuration using `dosocs2
configtest`. One may also pass the `-f` option to this command to see the
effects of specifying an alternate config file location.
